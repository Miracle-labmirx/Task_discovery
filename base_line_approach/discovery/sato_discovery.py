import requests
import json
from threading import Thread

ENDPOINT = "https://project-sato1.lasige.di.fc.ul.pt"
API_ENDPOINT = "https://project-sato1.lasige.di.fc.ul.pt/api"
# API_KEY = "sato_0rwFb7eqdMzPz46ofNurE_Iki4cvso5C-gDaCQk-Gw0"
API_KEY = "sato_1oyQx-XWRQ1tq7VjLxIw_2NNWwLct7onsRGbQNNYTzs"
HEADERS = {"x-api-key": API_KEY}

def isEndpointWorking():
    response = requests.get(ENDPOINT + "/_version", headers=HEADERS,verify=False)
    print(response.status_code)
    if response.status_code == 200:
        return True
    return False

def getBuildings():
    buildings = requests.get(API_ENDPOINT + "/buildings", headers=HEADERS,verify=False)
    print(buildings.status_code)
    # print(buildings.content)
    if buildings is not None and buildings.status_code == 200:
        return buildings.json()
    return None

def discoveryBuildingTasks(building_id):
    #print(building_id)
    current_building_tasks = requests.get(API_ENDPOINT + "/buildings/" + building_id + "/tasks", headers=HEADERS,verify=False)
    if current_building_tasks is not None and current_building_tasks.status_code == 200:
        # print(json.dumps(current_building_tasks.json(), indent=4))
        json.dumps(current_building_tasks.json(), indent=4)
    else:
        print("There are no tasks in building " + building_id)

def getZones(building_id):
    zones = requests.get(API_ENDPOINT + "/building/" + building_id + "/zones", headers=HEADERS,verify=False)
    if zones is not None and zones.status_code == 200:
        return zones.json()
    return None

def discoveryZoneTasks(zone_id):
    current_zone_tasks = requests.get(API_ENDPOINT + "/zone/" + zone_id + "/tasks", headers=HEADERS,verify=False)
    if current_zone_tasks is not None and current_zone_tasks.status_code == 200:
        # print(json.dumps(current_zone_tasks.json(), indent=4))
        json.dumps(current_zone_tasks.json(), indent=4)
    else:
        print("There are no tasks in zone " + zone_id)

def getSpaces(building_id):
    spaces = requests.get(API_ENDPOINT + "/building/" + building_id + "/rooms", headers=HEADERS,verify=False)
    if spaces is not None and spaces.status_code == 200:
        return spaces.json()
    return None

def getDevicesInSpace(space_id):
    devices = requests.get(API_ENDPOINT + "/room/" + space_id + "/devices", headers=HEADERS,verify=False)
    if devices is not None and devices.status_code == 200:
        return devices.json()
    return None

def discoverySpaceTasks(space_id):
    current_space_tasks = requests.get(API_ENDPOINT + "/room/" + space_id + "/tasks", headers=HEADERS,verify=False)
    if current_space_tasks is not None and current_space_tasks.status_code == 200:
        # print(json.dumps(current_space_tasks.json(), indent=4))
        json.dumps(current_space_tasks.json(), indent=4)
    else:
        print("There are no tasks in space " + space_id)

def main():
    if not isEndpointWorking():
        print("Endpoint is not working")
        return
    buildings = getBuildings()
    # print(json.dumps(buildings, indent=4))
    return
    if buildings is None:
        print("There are no buildings")
        return
    #buildings = [ {"id"="Aalborg-Office"}, {"id"="Lisbon_FCUL_Library"} ]]
    #declare an array of dictionaries with and id prperty and value
    #buildings = [ {"id":"Aalborg-Office"} ]
    #buildings = [ {"id":"Lisbon_FCUL_Library"} ]
    #buildings = [ {"id":"Lisbon_FCUL_Library"}, {"id":"Aalborg-Office"} ]
    threads = []
    for building in buildings:
        #discoveryBuildingTasks(building.get("id")) #single-thread
        threads.append(Thread(target=discoveryBuildingTasks, args=(building.get("id"),)))
        spaces = getSpaces(building.get("id"))
        # print(spaces)
        if spaces is None:
            continue
        for space in spaces:
            print(space.get("id"))
            #discoverySpaceTasks(space.get("id")) #single-thread
            threads.append(Thread(target=discoverySpaceTasks, args=(space.get("id)",))))
        zones = getZones(building.get("id"))
        for zone in zones:
            #discoveryZoneTasks(zone.get("id")) #single-thread
            threads.append(Thread(target=discoveryZoneTasks, args=(zone.get("id"),)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()  
    
if __name__ == "__main__":
    main()

#buffer comments
#print(json.dumps(building, indent=4))