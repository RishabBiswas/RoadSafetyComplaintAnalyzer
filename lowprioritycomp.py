import random
import pandas as pd

# ----------------------------
# Low-Priority Problem Types
# ----------------------------

issues = {
    "Pothole": [
        "minor road cracks",
        "small surface cracks",
        "slight uneven road surface"
    ],
    "Lighting": [
        "dim street light",
        "street light flickering",
        "street light needs cleaning"
    ],
    "Signboard": [
        "faded signboard",
        "old warning sign",
        "rusted signboard"
    ],
    "Footpath": [
        "slightly damaged footpath tiles",
        "uneven footpath surface",
        "cracked footpath pavement"
    ]
}

locations = [
    "near residential area",
    "near park",
    "on internal road",
    "near market area",
    "along service road"
]

descriptions = [
    "needs maintenance",
    "requires attention",
    "should be repaired",
    "can be fixed during routine maintenance"
]

# ----------------------------
# Generate Complaints
# ----------------------------

data = []

for _ in range(100):  # generate 100 low-priority complaints
    category = random.choice(list(issues.keys()))
    issue = random.choice(issues[category])
    location = random.choice(locations)
    desc = random.choice(descriptions)

    complaint_text = f"There are {issue} {location} and it {desc}."

    data.append([
        complaint_text,
        category,
        "Low"
    ])

# ----------------------------
# Save to CSV
# ----------------------------

df = pd.DataFrame(data, columns=["complaint_text", "category", "priority"])
df.to_csv("low_priority_complaints.csv", index=False)

print("✅ Low-priority complaints dataset generated successfully!")
print(df.head())
