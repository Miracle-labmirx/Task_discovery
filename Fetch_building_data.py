import neo4j
from neo4j import GraphDatabase, basic_auth
# Replace these with your actual credentials
NEO4J_URI = "neo4j://neo4j:7687"
USERNAME = 'neo4j'
PASSWORD = 'password' 

# Create a Neo4j driver instance
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(USERNAME, PASSWORD))
# SATO 
api_endpoints = ["https://project-sato1.lasige.di.fc.ul.pt/api", "https://project-sato2.lasige.di.fc.ul.pt/api"]
headers = {"x-api-key": "sato_1oyQx-XWRQ1tq7VjLxIw_2NNWwLct7onsRGbQNNYTzs"}

def list_buildings():
    query = "MATCH (b:Building) RETURN b"
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            building = record["b"]
            # print(dict(building))
            name = building.get("name", "[No name]")
            print(name)

def list_spaces():
    query = "MATCH (s:Space) RETURN s"
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            space = record["s"]
            # print(dict(space))
            name = space.get("name", "[No name]")
            print(name)

def list_zones():
    query = "MATCH (z:Zone) RETURN z"
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            zone = record["z"]
            print(dict(zone))

def list_devices():
    query = "MATCH (d:Device) RETURN d"
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            device = record["d"]
            print(dict(device))

def list_external():
    query = "MATCH (e:External) RETURN e"
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            external = record["e"]
            print(dict(external))

def list_task():
    query = "MATCH (t:Task) RETURN t"
    with driver.session() as session:
        result = session.run(query)
        for record in result:
            task = record["t"]
            print(dict(task))

def get_spaces_for_building(building_name):
    query = """
    MATCH (b:Building {name: $building_name})-[:hasZone]->(z)
    RETURN b, z
    """
    with driver.session() as session:
        result = session.run(query, {"building_name": building_name})
        for record in result:
            building = dict(record["b"])
            zone = dict(record["z"])
            print(f"Building: {building['name']} --> Zone: {zone}")
            
def clear_neo4j_database():
    query = "MATCH (n) DETACH DELETE n"
    with driver.session() as session:
        session.run(query)
        print("✅ All nodes and relationships deleted.")