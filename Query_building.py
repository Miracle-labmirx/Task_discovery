# import requests

# api_endpoints = ["https://project-sato1.lasige.di.fc.ul.pt/api", "https://project-sato2.lasige.di.fc.ul.pt/api"]
# headers = {"x-api-key": "sato_1oyQx-XWRQ1tq7VjLxIw_2NNWwLct7onsRGbQNNYTzs"}

# # Listing all zones of a building, the same logic can be used for zones and zones, etc..
# rooms = requests.get(
#     api_endpoints[1] + "/buildings/Lisbon-FCUL-Library/zones", headers= headers, verify=False)

# if(rooms.status_code != 200):
#     print("Query error:", rooms.status_code, "\nDetails:", rooms.text)
# else:
#     rooms = rooms.json()


# print(rooms)

# import requests
# import sys
# import json

# api_endpoint = "https://project-sato2.lasige.di.fc.ul.pt/api"
# headers = {
#     "x-api-key": "sato_1oyQx-XWRQ1tq7VjLxIw_2NNWwLct7onsRGbQNNYTzs"
# }

# # all_zones = []
# # target_query = api_endpoint + "/buildings/Lisbon-FCUL-Library/zones?offset=%s"
# # offset = 0

# # while True:
# #     response = requests.get(target_query % offset, headers=headers, verify=False)

# #     if response.status_code == 400:
# #         print("Finished retrieving all zones.")
# #         break

# #     if response.status_code != 200:
# #         print("Query error:", response.status_code, "\nDetails:", response.text)
# #         # sys.exit()
# #         break

# #     zones = response.json()
# #     names = [item['name'] for item in zones if 'name' in item]

# #     print(names)
# #     # print(zones)
# #     # print("Retrieved", len(zones), "zones from Lisbon-FCUL-Library.")
# #     # all_zones += zones if isinstance(zones, list) else [zones]
# #     all_zones.extend(zones)
# #     offset += 100
 
# # print("There are", len(all_zones), "zones registered in SATO for Lisbon-FCUL-Library.")
# # print(all_zones)



# all_zones = []
# # all_zones_id = []
# target_query = api_endpoint + "/zones?offset=%s"
# offset = 0
# def load_data():
#     global offset
#     while True:
#         response = requests.get(target_query % offset, headers= headers)

#         if response.status_code != 200:
#             print("Failed to retrieve zones or finished retrieving all entities. Status code:", response.status_code)
#             break

#         zones = response.json()

#         # Stop if no zones are returned
#         if not zones:
#             break
#         all_zones.extend(zones)
#         # Extract only space IDs
#         # for space in zones:
#         #     if 'id' in space:
#         #         all_zones_id.append(space['id'])

#         # Update the offset to fetch the next batch
#         offset += 100

#         print(f"Retrieved {len(all_zones)} total zones.")

#         #  Filter zones that contain spaces
#         zones_with_spaces = [space for space in all_zones if "hasSpace" in space]

#         print(f"\n {len(zones_with_spaces)} zones contain spaces. Printing hierarchy")
     
#         for zone in zones_with_spaces:

#             zone_name = zone.get("name", zone.get("id", "Unnamed zone"))
#             print(f"Zone: {zone_name}")

#             spaces = zone["hasSpace"]
#             if isinstance(spaces, list):
#                 for space in spaces:
#                     print(f"Space: {space}")
            
#             else:
#                 print(f"Space: {spaces}")
#     # Final output
#     # print("There are", len(all_zones_id), "zones registered in SATO.")

#     # Save full space data with zones to JSON
#     with open("zones_with_spaces.json", "w") as f:
#         json.dump(zones_with_spaces, f, indent= 4)
#         print("\n Saved filtered zones with zones to 'zones_with_zones.json'")


#     # #  Save to JSON file
#     # with open("zones.json", "w") as json_file:
#     #     json.dump(all_zones_id, json_file, indent=4)
#     #     print("Saved to zones.json")

#     # # Save to plain text file (one ID per line)
#     # with open("zones.txt", "w") as text_file:
#     #     for space_id in all_zones_id:
#     #         text_file.write(space_id + "\n")
#     #     print("Saved to zones.txt")
# load_data()


# import requests
# import sys
# import json

# import requests

# SATO_API = "https://project-sato1.lasige.di.fc.ul.pt/api"
# API_KEY = "sato_1oyQx-XWRQ1tq7VjLxIw_2NNWwLct7onsRGbQNNYTzs"
# HEADERS = {"x-api-key": API_KEY}
# VERIFY_SSL = False

# all_entity_ids = []

# def fetch_paginated(endpoint_template, entity_type_label, parent_id=None):
#     """Generic fetcher for paginated entities."""
#     offset = 0
#     results = []
#     while True:
#         if parent_id:
#             endpoint = endpoint_template.format(id=parent_id, offset=offset)
#         else:
#             endpoint = endpoint_template.format(offset=offset)

#         response = requests.get(SATO_API + endpoint, headers=HEADERS, verify=VERIFY_SSL)
#         if response.status_code != 200:
#             break

#         data = response.json()
#         if not data:
#             break

#         for item in data:
#             entity_id = item.get("id")
#             if entity_id:
#                 all_entity_ids.append(entity_id)
#                 results.append(item)

#         offset += 100

#     return results

# def fetch_buildings():
#     return fetch_paginated("/buildings?offset={offset}", "building")

# def fetch_zones(building_id):
#     return fetch_paginated("/building/{id}/zones?offset={offset}", "zone", building_id)

# def fetch_spaces(building_id):
#     return fetch_paginated("/building/{id}/rooms?offset={offset}", "space", building_id)

# def fetch_devices():
#     return fetch_paginated("/devices?offset={offset}", "device")

# def save_to_file(filename="sato_ids.txt"):
#     with open(filename, "w") as f:
#         for entity_id in all_entity_ids:
#             f.write(entity_id + "\n")
#     print(f"{len(all_entity_ids)} IDs saved to {filename}")

# def main():
#     buildings = fetch_buildings()
#     for building in buildings:
#         building_id = building.get("id")
#         if not building_id:
#             continue
#         fetch_zones(building_id)
#         fetch_spaces(building_id)
#     fetch_devices()
#     save_to_file()


# main()



import requests
import json
import pandas as pd
import openpyxl

try:
    import openpyxl
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])

SATO_API = "https://project-sato1.lasige.di.fc.ul.pt/api"
API_KEY = "sato_1oyQx-XWRQ1tq7VjLxIw_2NNWwLct7onsRGbQNNYTzs"
HEADERS = {"x-api-key": API_KEY}
VERIFY_SSL = False

# all_entity_ids = []
# metadata_map = {}

all_data = []

def fetch_paginated(endpoint_template, entity_type, parent_id=None):
    offset = 0
    results = []

    while True:
        if parent_id:
            endpoint = endpoint_template.format(id=parent_id, offset=offset)
        else:
            endpoint = endpoint_template.format(offset=offset)

        response = requests.get(SATO_API + endpoint, headers=HEADERS, verify=VERIFY_SSL)
        if response.status_code != 200:
            break

        data = response.json()
        if not data:
            break

        # for item in data:
        #     entity_id = item.get("id")
        #     if entity_id:
        #         all_entity_ids.append(entity_id)
        #         results.append(item)

        #         # Build metadata entry
        #         metadata = {"type": entity_type}
        #         if entity_type in {"Building", "Zone", "Space"}:
        #             metadata["area"] = item.get("area", 0)
        #         if entity_type == "Device":
        #             metadata["category"] = item.get("category")
        #             metadata["measuresProperty"] = item.get("measuresProperty", [])
        #             metadata["controlsProperty"] = item.get("controlsProperty", [])
        #             metadata["unit"] = item.get("unit")
        #         metadata_map[entity_id] = metadata

        offset += 100

    return results

def fetch_buildings():
    return fetch_paginated("/buildings?offset={offset}", "Building")

def fetch_zones(building_id):
    return fetch_paginated("/building/{id}/zones?offset={offset}", "Zone", building_id)

def fetch_spaces(building_id):
    return fetch_paginated("/building/{id}/rooms?offset={offset}", "Space", building_id)

def fetch_devices():
    return fetch_paginated("/devices?offset={offset}", "Device")

def save_ids_to_file(filename="sato_ids.txt"):
    with open(filename, "w") as f:
        for entity_id in all_entity_ids:
            f.write(entity_id + "\n")
    print(f" {len(all_entity_ids)} IDs saved to {filename}")

def save_to_excel(filename="sato_entities.xlsx"):
    df = pd.DataFrame(all_data)
    df.to_excel(filename, index=False)
    print(f"Saved {len(df)} entities to {filename}")


def save_metadata_to_json(filename="sato_metadata.json"):
    with open(filename, "w") as f:
        json.dump(metadata_map, f, indent=4)
    print(f" Metadata for {len(metadata_map)} entities saved to {filename}")

def main():
    buildings = fetch_buildings()
    for building in buildings:
        building_id = building.get("id")
        if not building_id:
            continue
        fetch_zones(building_id)
        fetch_spaces(building_id)
    fetch_devices()
    # save_ids_to_file()
    # save_metadata_to_json()
    save_to_excel()

main()
