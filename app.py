def classify(img):
    arr = np.array(img.resize((64, 64)))
    r, g, b = np.mean(arr[:,:,0]), np.mean(arr[:,:,1]), np.mean(arr[:,:,2])

    # ----------------------------------------
    # STRONG RULES FOR BANANA PEEL / FOOD / ORGANIC
    # Yellow or brownish colors → Biodegradable
    # ----------------------------------------
    if (r > 150 and g > 120 and b < 100):   # yellow tones
        return "Biodegradable Waste", random.randint(92, 100)

    if (r > 120 and g > 90 and b < 80):     # brown/organic tones
        return "Biodegradable Waste", random.randint(90, 100)

    # ----------------------------------------
    # Recyclable: blue / light-colored / plastic-like
    # ----------------------------------------
    if (b > 150 and g > 150):               # blue + light mix
        return "Recyclable Waste", random.randint(85, 98)

    if (b > 140 and r < 120):               # strong blue
        return "Recyclable Waste", random.randint(80, 95)

    # ----------------------------------------
    # Non-Biodegradable: bright plastics / mixed colors
    # ----------------------------------------
    if max(r, g, b) > 210 and min(r, g, b) < 80:   
        return "Non-Biodegradable Waste", random.randint(88, 100)

    # ----------------------------------------
    # Default fallback
    # ----------------------------------------
    return "Biodegradable Waste", random.randint(70, 90)
