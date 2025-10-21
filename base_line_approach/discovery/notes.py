import json
import requests
import pandas as pd
#load json kpi_instances file
# with open('json_files/devices.json') as f:
#     devices = json.load(f)


# device_ids = []
# for device in devices:
#     device_ids.append(device['id'])
#print(device_ids)
#print(json.dumps(devices, indent=4))



#Connecting to SATO api

# SATO_API = "https://project-sato1.lasige.di.fc.ul.pt/api"
# # SATO_API_2 = "https://project-sato2.lasige.di.fc.ul.pt/api"

# API_KEY = "sato_1oyQx-XWRQ1tq7VjLxIw_2NNWwLct7onsRGbQNNYTzs"
# HEADERS = {"x-api-key": API_KEY}

# all_devices_id = []
# target_query = SATO_API + "/devices?offset=%s"
# offset = 0
# def load_data():
#     while True:
#         response = requests.get(target_query % offset, headers=HEADERS)

#         if response.status_code != 200:
#             print("Failed to retrieve devices or finished retrieving all entities. Status code:", response.status_code)
#             break

#         devices = response.json()

#         # Stop if no devices are returned
#         if not devices:
#             break

#         # Extract only device IDs
#         for device in devices:
#             if 'id' in device:
#                 all_devices_id.append(device['id'])

#         # Update the offset to fetch the next batch
#         offset += 100

#     # Final output
#     print("There are", len(all_devices_id), "devices registered in SATO.")

#create a prefix tree with the device_ids
class Node:
    def __init__(self, value):
        self.value = value
        self.children = {}
        self.is_end = False

class PrefixTree:
    def __init__(self):
        self.root = Node(None)
    
    def insert(self, word):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = Node(char)
            current_node = current_node.children[char]
        current_node.is_end = True
    
    def search(self, word):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return current_node.is_end

    def starts_with(self, prefix):
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return False
            current_node = current_node.children[char]
        return True
    
    def delete(self, word):
        def _delete(node, word, index):
            if index == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0
            char = word[index]
            if char not in node.children:
                return False
            child_node = node.children[char]
            if _delete(child_node, word, index + 1):
                del node.children[char]
                return len(node.children) == 0
            return False
        _delete(self.root, word, 0)

# def load_ids_and_insert_into_tree(filename, prefix_tree):
#     with open(filename, "r") as file:
#         for line in file:
#             id_str = line.strip()
#             if id_str:  # avoid empty lines
#                 prefix_tree.insert(id_str)

# prefix_tree = PrefixTree()
# # for device_id in all_devices_id:
# #     prefix_tree.insert(device_id)

# load_ids_and_insert_into_tree("/caml/sato_ids.txt", prefix_tree)
# print("All IDs inserted into the prefix tree.")

def load_ids_and_insert_into_tree(
    filename,
    prefix_tree,
    sheet_name=0,        
    id_column="id",
    strip=True,
    case=None           
):
    # Read only the 'id' column for efficiency
    df = pd.read_excel(filename, sheet_name=sheet_name, usecols=[id_column])

    # Clean and normalize
    s = df[id_column].dropna().astype(str)
    if strip:
        s = s.str.strip()
    if case == "upper":
        s = s.str.upper()
    elif case == "lower":
        s = s.str.lower()

    # Insert unique, non-empty IDs into the trie
    for id_str in s[s.ne("")].drop_duplicates():
        prefix_tree.insert(id_str)

# --- Usage ---
prefix_tree = PrefixTree()
load_ids_and_insert_into_tree("/caml/standardized_sato_device.xlsx", prefix_tree, sheet_name=0, id_column="id")
print("All IDs inserted into the prefix tree.")

# Convert prefix tree to a dictionary

def node_to_dict(node):
    return {
        "value": node.value,
        "is_end": node.is_end,
        "children": {char: node_to_dict(child) for char, child in node.children.items()}
    }

# Load and rebuild the tree from file 

def dict_to_node(data):
    node = Node(data["value"])
    node.is_end = data["is_end"]
    node.children = {char: dict_to_node(child) for char, child in data["children"].items()}
    return node

# Convert root node to dictionary
tree_dict = node_to_dict(prefix_tree.root)
# Save to file
with open("prefix_tree_new.json", "w") as f:
    json.dump(tree_dict, f, indent=4)

print("Prefix tree saved to prefix_tree_new.json")

# To load it
with open("prefix_tree.json", "r") as f:
    data = json.load(f)

def load_from_json(self, filepath: str) -> None:
        with open(filepath, "r") as f:
            data = json.load(f)
        self.root = self._dict_to_node(data)

# print(prefix_tree.search('Aalborg'))

# print(prefix_tree.search('1'))

# print(prefix_tree.starts_with('1'))

# print the whole prefix tree hierarchically
def print_prefix_tree(node, prefix):
    if node.is_end:
        print(prefix)
    for char, child_node in node.children.items():
        print_prefix_tree(child_node, prefix + char)

# print_prefix_tree(prefix_tree.root, '')
        
def find_and_print_nodes_with_substring(root, target_substring):
    """
    Traverse the prefix tree and print all full substrings (paths)
    where 'target_substring' appears, along with the corresponding node info.
    """
    matching_nodes = []

    def dfs(node, current_path):
        if target_substring in current_path:
            matching_nodes.append((current_path, node))

        for char, child_node in node.children.items():
            dfs(child_node, current_path + char)

    # Start traversal from the root
    dfs(root, "")

    # Print results
    if matching_nodes:
        print(f"\n Found {len(matching_nodes)} matches containing '{target_substring}':\n")
        for i, (path, node) in enumerate(matching_nodes, 1):
            print(f"{i}. Path: {path}")
            print(f"   - Ends a word? {'yes' if node.is_end else 'no'}")
            print(f"   - Number of children: {len(node.children)}\n")
    else:
        print(f"\n No matches found containing '{target_substring}'.")



# def find_matches_and_print(root_node, json_path):
#     def dfs(node, path, results, target):
#         # Build the current full path string from root to this node
#         full_path = path + (node.value if node.value else "")

#         # Only consider full device IDs (is_end = True)
#         if node.is_end and isinstance(full_path, str) and target in full_path:
#             results.append(full_path)

#         for char, child in node.children.items():
#             dfs(child, full_path, results, target)

#     # Load all KPI task definitions
#     with open(json_path) as f:
#         kpi_definitions = json.load(f)

#     # Iterate over each KPI definition
#     for kpi in kpi_definitions:
#         kpi_id = kpi.get("id", "Unknown-KPI")
#         task_id = kpi.get("taskId", "Unknown-Task")
#         requires = kpi.get("requires", {})

#         print(f"\n KPI ID: {kpi_id}")
#         print(f" Task ID: {task_id}")

#         any_match_found = False

#         for req_name, req_info in requires.items():
#             # Extract the keyword to search for from either property field
#             property_key = req_info.get("measuresProperty") or req_info.get("controlsProperty")
#             if not property_key:
#                 continue

#             # Collect matches using DFS traversal
#             matched_ids = []
#             dfs(root_node, "", matched_ids, property_key)

#             print(f"\n  Requirement: {req_name}")
#             print(f"     Property Match: {property_key}")
#             print(f"     {len(matched_ids)} device(s) found:")
#             for device_id in matched_ids:
#                 print(f"        {device_id}")
#                 any_match_found = True

#         if not any_match_found:
#             print("   No matches found for this KPI definition.")

# def match_task_requirements(root_node, task_json_path):
#     def dfs_match(node, path, results, target_keywords):
#         full_path = path + (node.value if node.value else "")
#         if node.is_end and any(keyword in full_path for keyword in target_keywords):
#             results.append(full_path)
#         for char, child in node.children.items():
#             dfs_match(child, full_path, results, target_keywords)

#     with open(task_json_path) as f:
#         tasks = json.load(f)

#     for task in tasks:
#         print(f"\n---\nTask: {task['name']}\nTask ID: {task['taskId']}")
#         requirements = task.get("requires", {})
#         found_any = False

#         for req_key, req_details in requirements.items():
#             print(f"\nRequirement: {req_key}")
#             match_keywords = []

#             # Type-based search
#             if "type" in req_details:
#                 if isinstance(req_details["type"], list):
#                     match_keywords.extend(req_details["type"])
#                 else:
#                     match_keywords.append(req_details["type"])

#             # Property-based search
#             for prop_key in ["measuresProperty", "controlsProperty"]:
#                 if prop_key in req_details:
#                     match_keywords.extend(req_details[prop_key] if isinstance(req_details[prop_key], list) else [req_details[prop_key]])

#             matched_ids = []
#             dfs_match(root_node, "", matched_ids, match_keywords)

#             print(f"Matched {len(matched_ids)} entities:")
#             for match in matched_ids:
#                 print(f" - {match}")
#                 found_any = True

#         if not found_any:
#             print("No matches found.")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import json
import copy
import re
import os
from typing import Iterable, Dict, Any, List, Tuple

# ================= Regexes & config (unchanged) =================
TOKEN = r"(?:^|[^A-Za-z]){tok}(?:[^A-Za-z]|$)"
ALLOWED_LOC_TOKENS = ("Building", "Zone", "Space")
LOC_RE = re.compile(TOKEN.format(tok=fr"({'|'.join(ALLOWED_LOC_TOKENS)})"))
SENSOR_RE = re.compile(TOKEN.format(tok=r"Sensor"))

DASH = r"[-_\s\u2010-\u2015]?"
ACCUM_LOAD_RE = re.compile(rf"Accumulated{DASH}Load", re.IGNORECASE)
TOTAL_LOAD_RE  = re.compile(rf"Total{DASH}Load",        re.IGNORECASE)

RECOGNIZED_REQ_KEYS = {
    "type", "measuresProperty", "controlsProperty", "class", "category",
    "measure", "measures", "measuredProperty", "hasQuantityKind"
}

REQ_BLOCK_MODE = "any"
VERBOSE = True


# ================= Helpers (unchanged) =================
def collect_all_ids(node):
    out = []
    def dfs(n, path):
        full_path = path + (getattr(n, "value", "") or "")
        if getattr(n, "is_end", False):
            out.append(full_path)
        for _, child in n.children.items():
            dfs(child, full_path)
    dfs(node, "")
    return out

def mentions_location_rule(id_str: str) -> bool:
    return bool(LOC_RE.search(id_str))

def sensor_measure_rule(id_str: str) -> bool:
    if not SENSOR_RE.search(id_str):
        return False
    return bool(ACCUM_LOAD_RE.search(id_str) or TOTAL_LOAD_RE.search(id_str))

def location_tokens_present(id_str: str) -> List[str]:
    present = []
    for tok in ALLOWED_LOC_TOKENS:
        if re.search(TOKEN.format(tok=tok), id_str):
            present.append(tok)
    return present

def iter_requirement_blocks(requirements: Any) -> Iterable[Dict[str, Any]]:
    if not requirements:
        return []
    if isinstance(requirements, dict):
        return (b for b in requirements.values() if isinstance(b, dict))
    if isinstance(requirements, list):
        return (b for b in requirements if isinstance(b, dict))
    return []

def build_requirement_groups(req_details: Dict[str, Any]) -> List[List[str]]:
    groups = []
    for key, vals in req_details.items():
        if key not in RECOGNIZED_REQ_KEYS:
            continue
        if not isinstance(vals, list):
            vals = [vals]
        groups.append([str(v) for v in vals])
    return groups

def requirement_value_matches(id_str: str, value: str) -> bool:
    v = value.strip()
    vl = v.lower()
    if vl == "sensor":
        return bool(SENSOR_RE.search(id_str))
    if "accumulated" in vl and "load" in vl:
        return bool(ACCUM_LOAD_RE.search(id_str))
    if vl.startswith("total") and "load" in vl:
        return bool(TOTAL_LOAD_RE.search(id_str))
    for tok in ALLOWED_LOC_TOKENS:
        if v == tok:
            return bool(re.search(TOKEN.format(tok=tok), id_str))
    return (vl in id_str.lower())

def id_satisfies_requirement_block(id_str: str, req_block: Dict[str, Any]) -> bool:
    groups = build_requirement_groups(req_block)
    if not groups:
        return True
    for group in groups:
        if not any(requirement_value_matches(id_str, val) for val in group):
            return False
    return True

def id_satisfies_requirements(id_str: str, requirements: Any) -> bool:
    blocks = list(iter_requirement_blocks(requirements))
    if not blocks:
        return True
    if REQ_BLOCK_MODE == "all":
        return all(id_satisfies_requirement_block(id_str, b) for b in blocks)
    return any(id_satisfies_requirement_block(id_str, b) for b in blocks)


# ================= New: task instance creation + saving =================
def _safe_id_fragment(s: str, max_len: int = 120) -> str:
    """
    Turn a string into a filesystem-safe fragment (for filenames).
    Keep alphanum and a few chars; replace others with '-'; collapse runs.
    """
    frag = re.sub(r"[^A-Za-z0-9_.:/\-]+", "-", s)
    frag = re.sub(r"-{2,}", "-", frag).strip("-")
    if len(frag) > max_len:
        frag = frag[:max_len].rstrip("-")
    return frag or "entity"

def add_entity_to_requires(requires: Any, entity_id: str) -> Any:
    """
    Insert the matched entity id *under* the requirements section.
    - dict: add key 'entityId'
    - list: append a new block {'entityId': '<id>'}
    - None/other: create {'entityId': '<id>'}
    """
    if isinstance(requires, dict):
        new_req = copy.deepcopy(requires)
        key = "entityId" if "entityId" not in new_req else "_entityId"
        new_req[key] = entity_id
        return new_req
    if isinstance(requires, list):
        new_req = copy.deepcopy(requires)
        new_req.append({"entityId": entity_id})
        return new_req
    return {"entityId": entity_id}

def make_task_instance(base_task: Dict[str, Any], entity_id: str) -> Dict[str, Any]:
    """
    Clone the base task and inject the entity_id under 'requires'.
    Also adjust name and taskId for traceability.
    """
    t = copy.deepcopy(base_task)
    base_name = t.get("name") or "Task"
    base_id   = t.get("taskId") or (t.get("id") or "T")  # fall back to 'id' if present
    frag = _safe_id_fragment(entity_id)

    t["name"]   = f"{base_name} {entity_id}"
    t["taskId"] = f"{base_id}::{frag}"
    t["requires"] = add_entity_to_requires(t.get("requires"), entity_id)
    return t

def _unique_path(base_dir: str, filename_no_ext: str) -> str:
    """
    Ensure we don't overwrite: if file exists, append _2, _3, ...
    """
    path = os.path.join(base_dir, f"{filename_no_ext}.json")
    if not os.path.exists(path):
        return path
    i = 2
    while True:
        candidate = os.path.join(base_dir, f"{filename_no_ext}_{i}.json")
        if not os.path.exists(candidate):
            return candidate
        i += 1

def save_task_instance(instance: Dict[str, Any], out_dir: str) -> str:
    """
    Save a single task instance to its own JSON file.
    Filename is based on instance['taskId'] (sanitized). If missing, use name.
    Returns the output path.
    """
    os.makedirs(out_dir, exist_ok=True)
    base = instance.get("taskId") or instance.get("name") or "task"
    fname = _safe_id_fragment(base)
    out_path = _unique_path(out_dir, fname)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(instance, f, indent=2, ensure_ascii=False)
    return out_path


# ================= Main (enhanced: one file per match) =================
def match_task_requirements(root_node, task_json_path, out_dir: str = "expanded_tasks_per_entity"):
    """
    For each task in task_json_path:
      - find matching entities
      - for each match, create a *new* task instance with the entity ID
        inserted under 'requires'
      - save EACH instance to its OWN JSON file (no batching)
    """
    all_ids = collect_all_ids(root_node)

    with open(task_json_path, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    total_saved = 0

    for task in tasks:
        print(f"\n---\nTask: {task.get('name')}\nTask ID: {task.get('taskId') or task.get('id')}")
        requirements = task.get("requires")

        total = len(all_ids)
        after_loc = 0
        after_sensor = 0
        after_requirements = 0

        matched_ids: List[Tuple[str, List[str], str]] = []

        for id_str in all_ids:
            # Stage 1: Building/Zone/Space present
            if not mentions_location_rule(id_str):
                continue
            after_loc += 1

            # Stage 2: Sensor + (Accumulated|Total)-Load
            if not sensor_measure_rule(id_str):
                continue
            after_sensor += 1

            # Stage 3: Requirements
            if not id_satisfies_requirements(id_str, requirements):
                continue
            after_requirements += 1

            measure = "Accumulated-Load" if ACCUM_LOAD_RE.search(id_str) else ("Total-Load" if TOTAL_LOAD_RE.search(id_str) else "")
            matched_ids.append((id_str, location_tokens_present(id_str), measure))

        if VERBOSE:
            print(f"IDs total: {total}")
            print(f"  Passed location (Building/Zone/Space): {after_loc}")
            print(f"  Passed Sensor + (Accumulated|Total)-Load: {after_sensor}")
            print(f"  Passed requirements ({REQ_BLOCK_MODE} blocks): {after_requirements}")

        if matched_ids:
            print(f"Matched {len(matched_ids)} entities that satisfy ALL criteria:")
            for (id_str, locs, measure) in matched_ids:
                loc_tag = ",".join(locs) if locs else "-"
                print(f" - {id_str}    [locs: {loc_tag} | measure: {measure}]")

                # Create and save ONE FILE PER MATCH
                instance = make_task_instance(task, id_str)
                out_path = save_task_instance(instance, out_dir=out_dir)
                total_saved += 1
                if VERBOSE:
                    print(f"   saved: {out_path}")
        else:
            print("No matches found.")

    if VERBOSE:
        print(f"\nSaved {total_saved} task instance files in: {out_dir}")

