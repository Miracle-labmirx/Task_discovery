import requests
import json
#from notes import dict_to_node, print_prefix_tree, load_from_json, PrefixTree, match_task_requirements, load_ids_and_insert_into_tree, find_and_print_nodes_with_substring
from match_tasks_generic import PrefixTree, load_ids_and_insert_into_tree, RuleSet, match_tasks_with_rules

# To load it:
# print("Loading data....")
# with open("./json_files/prefix_tree.json", "r") as f:
#     data = json.load(f)

# all_entity_tree = PrefixTree()
# all_entity_tree.root = dict_to_node(data)
# Example usage:
# find_and_print_nodes_with_substring(all_entity_tree.root, "Setpoint-Air-Pressure-Supply")
# print_prefix_tree(device_tree.root, '')

# find_matches_and_print(device_tree.root, "./json_files/tasks_kpi.json")

# ------------ Load Task Requirements ------------
# with open("/caml/base_line_approach/discovery/json_files/EUI_task.json", "r") as f:
#     task_data = json.load(f)
# if not task_data:
#     raise ValueError("Task definition is empty.")
# # ------------ Load Prefix Tree from JSON ------------
# # with open("./json_files/prefix_tree.json", "r") as p:
# #     prefix_tree_data = json.load(p)

# prefix_tree = PrefixTree()
# load_ids_and_insert_into_tree("/caml/standardized_sato_device.xlsx", prefix_tree, sheet_name=0, id_column="id")
# match_task_requirements(prefix_tree.root, "./json_files/EUI_task.json")
#-------------------------------------------------------------------------------------------------------------------

strict_rules = RuleSet(
    name="strict_building_rules",
    location_patterns=[r"\b(Building|Zone|Space)\b"],
    entity_patterns=[r"\bSensor\b"],
    measure_patterns=[r"\b(Accumulated[-_ ]?Load|Total[-_ ]?Load)\b"],
    require_all=True,   # ensures all rule categories must match
    verbose=True
)
strict_rules.compile()

prefix_tree = PrefixTree()
load_ids_and_insert_into_tree("/caml/standardized_sato_device.xlsx", prefix_tree, id_column="id")

# Run matcher – Sato is only generated when *all rules* match
match_tasks_with_rules(prefix_tree.root, "./json_files/EUI_task.json", strict_rules)