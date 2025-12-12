def classify_image(img):
    img = img.resize((160, 160))
    arr = np.array(img).astype(np.float32)

    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    r_mean, g_mean, b_mean = r.mean(), g.mean(), b.mean()

    hsv = np.array(img.convert("HSV")).astype(np.float32)
    h, s, v = hsv[:,:,0], hsv[:,:,1], hsv[:,:,2]

    total = arr.shape[0] * arr.shape[1]

    # Masks
    yellow = (r > 150) & (g > 130) & (b < 110)
    green = (g > r) & (g > b) & (g > 120)
    blue = (b > 150) & (b > r + 15)
    gray = (np.abs(r-g)<15) & (np.abs(g-b)<15) & ((r+g+b)/3 > 110)

    yellow_frac = yellow.sum() / total
    green_frac = green.sum() / total
    blue_frac = blue.sum() / total
    gray_frac = gray.sum() / total

    variation = arr.std()
    bright_frac = (v > 230).sum() / total
    sat_frac = (s > 180).sum() / total

    # ---------------------------------------------------------
    # CLASSIFICATION RULES (order matters!)
    # ---------------------------------------------------------

    # 1) BIODEGRADABLE
    if yellow_frac > 0.03 or green_frac > 0.04:
        confidence = min(100, int(80 + (yellow_frac + green_frac) * 150))
        return "Biodegradable Waste", confidence
    if r_mean > 120 and g_mean > 90 and b_mean < 100:
        return "Biodegradable Waste", 85

    # 2) RECYCLABLE
    if blue_frac > 0.06 or gray_frac > 0.05:
        confidence = min(100, int(75 + (blue_frac + gray_frac) * 180))
        return "Recyclable Waste", confidence

    # 3) NON-BIO (only if shiny/very varied)
    if (variation > 100) or (bright_frac > 0.20 and sat_frac > 0.25):
        confidence = min(100, int(85 + variation / 3))
        return "Non-Biodegradable Waste", confidence

    # Default fallback
    return "Biodegradable Waste", 75
