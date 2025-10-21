import neo4j
from neo4j import GraphDatabase, basic_auth
from Fetch_building_data import list_buildings, list_spaces, list_zones, list_devices, list_external, list_task, get_spaces_for_building, clear_neo4j_database

 
# Replace these with your actual credentials
NEO4J_URI = "neo4j://neo4j:7687"
USERNAME = 'neo4j'
PASSWORD = 'password' 

# Create a Neo4j driver instance
driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(USERNAME, PASSWORD))
# SATO 
api_endpoints = ["https://project-sato1.lasige.di.fc.ul.pt/api", "https://project-sato2.lasige.di.fc.ul.pt/api"]
headers = {"x-api-key": "sato_1oyQx-XWRQ1tq7VjLxIw_2NNWwLct7onsRGbQNNYTzs"}

# list_spaces()
clear_neo4j_database()
driver.close()
