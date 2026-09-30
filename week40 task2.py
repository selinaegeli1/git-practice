import pandas as pd
import yaml
import json

# 1. Les inn konfigurasjonsfilen (YAML)
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

# Henter ut relevante parametere
max_days = config["max_days_since_calibration"]
output_file = config["output_file"]

# 2. Leser inn data fra excel og csv. filen
sensors = pd.read_excel("sensors.xlsx")
calibrations = pd.read_csv("calibrations.csv")

# Her så slår de sammen dataene fra de to filene basert på sensor_id
data = sensors.merge(calibrations, on = "sensor_id")

# Finner sensorer som har gått over max_days_since_calibration
overdue = data[data["days_since_calibration"] > max_days]

# Lager en liste med dictionaries som inneholder sensor_id, lab_room, owner og days_since_calibration
result = overdue[
    ["sensor_id", "lab_room", "owner", "days_since_calibration"]
].to_dict(orient = "records")

# Til slutt skriver resultatet til en .json fil
with open(output_file, "w") as file:
    json.dump(result, file, indent = 2)
