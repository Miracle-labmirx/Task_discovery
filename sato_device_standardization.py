import pandas as pd
import re

# Load Excel file
df = pd.read_excel("sato_device.xlsx")

def standardize_id(entry):
    if pd.isna(entry):
        return entry

    entry = str(entry)

    # Step 1: Add "Building_" prefix
    entry = "Building_" + entry

    # Step 2: Add "Space_" before Floor-X:Room-Y
    floor_room_pattern = r"(Floor-\d+:Room-[^:]+)"
    entry = re.sub(floor_room_pattern, r"Space_\1", entry)

    # Step 3: Add "Space_" before Floor-X:Apartment-Y
    floor_apartment_pattern = r"(Floor-\d+:Apartment-[^:]+)"
    entry = re.sub(floor_apartment_pattern, r"Space_\1", entry)

    # Step 4: Add "Space_" before any segment containing "Floor" (even without room/apartment)
    floor_any_pattern = r":([^:]*Floor[^:]*)"
    def prefix_floor_any(match):
        segment = match.group(1)
        if not segment.startswith("Space_"):
            return ":Space_" + segment
        return ":" + segment
    entry = re.sub(floor_any_pattern, prefix_floor_any, entry)

    # Step 5: Add "Zone_" before any segment containing "Atrium"
    atrium_pattern = r":([^:]*Atrium[^:]*)"
    def prefix_atrium(match):
        segment = match.group(1)
        if not segment.startswith("Zone_"):
            return ":Zone_" + segment
        return ":" + segment
    entry = re.sub(atrium_pattern, prefix_atrium, entry)

    # Step 6: Add "Space_" before any segment containing "technical room"
    tech_room_pattern = r":([^:]*Technical-Room[^:]*)"
    def prefix_tech_room(match):
        segment = match.group(1)
        if not segment.startswith("Space_"):
            return ":Space_" + segment
        return ":" + segment
    entry = re.sub(tech_room_pattern, prefix_tech_room, entry, flags=re.IGNORECASE)

    # Step 7: For any segment that contains "Zone", add "Zone_" prefix if not already present
    zone_anywhere_pattern = r":([^:]*Zone[^:]*)"
    def prefix_zone(match):
        segment = match.group(1)
        if not segment.startswith("Zone_"):
            return ":Zone_" + segment
        return ":" + segment
    entry = re.sub(zone_anywhere_pattern, prefix_zone, entry)

    return entry

# Apply the transformation
df["id"] = df["id"].apply(standardize_id)

# Display result
print(df.head())

# Optional: Export to Excel
df.to_excel("standardized_sato_device.xlsx", index=False)



