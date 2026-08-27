import random
import pandas as pd

issues = ["deep pothole", "broken traffic signal", "street light not working",
          "missing signboard", "damaged footpath"]

locations = ["near school", "at main junction", "in residential area",
             "near hospital", "on highway"]

problems = ["causing accidents", "creating safety risks",
            "leading to traffic congestion", "endangering pedestrians"]

data = []

for _ in range(200):
    issue = random.choice(issues)
    location = random.choice(locations)
    problem = random.choice(problems)
    text = f"There is a {issue} {location} {problem}."

    if "pothole" in issue:
        category = "Pothole"
    elif "signal" in issue:
        category = "Signal"
    elif "light" in issue:
        category = "Lighting"
    elif "signboard" in issue:
        category = "Signboard"
    else:
        category = "Footpath"

    priority = "High" if "accidents" in problem else "Medium"

    data.append([text, category, priority])

df = pd.DataFrame(data, columns=["complaint_text", "category", "priority"])
df.to_csv("complaints.csv", index=False)
