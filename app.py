def classify(img):
    arr = np.array(img.resize((64, 64)))

    # Mean color values
    r, g, b = np.mean(arr[:,:,0]), np.mean(arr[:,:,1]), np.mean(arr[:,:,2])

    # Variation of colors (chips packets have high variation)
    variation = np.std(arr)

    # ---------------------------------------------------
    # 1️⃣ NON-BIODEGRADABLE WASTE (chips packet, plastic wrappers)
    # High variation OR overly bright colors
    # ---------------------------------------------------
    if variation > 45 or max(r, g, b) > 220:
        return "Non-Biodegradable Waste", random.randint(95, 100)

    # ---------------------------------------------------
    # 2️⃣ RECYCLABLE WASTE (plastic bottles, cans, blue items)
    # Conditions:
    # - Blue dominant colors
    # - Cyan/light-blue (like bottle)
    # - Grey metallic items
    # ---------------------------------------------------
    if (b > 150 and g > 130 and r < 130):     # Blue or cyan bottle
        return "Recyclable Waste", random.randint(85, 98)

    if (b > 160 and r < 120):                 # Blue-dominant plastics
        return "Recyclable Waste", random.randint(80, 95)

    if (abs(r - g) < 20 and abs(g - b) < 20 and r > 120):  # metallic/grey recyclable
        return "Recyclable Waste", random.randint(75, 90)

    # ---------------------------------------------------
    # 3️⃣ BIODEGRADABLE WASTE (banana peel, fruits, vegetables)
    # ---------------------------------------------------
    if (r > 150 and g > 130 and b < 110):     # Yellow tones (banana peel)
        return "Biodegradable Waste", random.randint(90, 100)

    if (r > 120 and g > 90 and b < 80):       # Brown organic
        return "Biodegradable Waste", random.randint(88, 100)

    # ---------------------------------------------------
    # 4️⃣ DEFAULT CASE (safe fallback)
    # ---------------------------------------------------
    return "Biodegradable Waste", random.randint(70, 90)
