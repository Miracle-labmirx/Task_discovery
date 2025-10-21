# filepath: general_task_matcher.py
import json
import re
import os
import copy
from typing import List, Dict, Any, Iterable, Tuple, Callable, Optional
from dataclasses import dataclass, field
import pandas as pd
# ========== Prefix Tree (unchanged) ==========
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
    
    def collect_all_ids(self, node=None) -> list:
        """Traverse the tree and collect all complete words (IDs)."""
        node = node or self.root
        all_ids = []

        def dfs(n, path):
            new_path = path + (n.value or "")
            if n.is_end:
                all_ids.append(new_path)
            for child in n.children.values():
                dfs(child, new_path)

        dfs(node, "")
        return all_ids


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

# ========== Generalized Rule Framework ==========
@dataclass
class RuleSet:
    """Generic rule definitions for entity matching."""
    name: str
    location_patterns: List[str] = field(default_factory=list)
    entity_patterns: List[str] = field(default_factory=list)
    measure_patterns: List[str] = field(default_factory=list)
    custom_rules: List[Callable[[str], bool]] = field(default_factory=list)
    require_all: bool = True
    verbose: bool = True

    def compile(self):
        """Compile regexes."""
        def compile_group(group: List[str]) -> List[re.Pattern]:
            return [re.compile(p, re.IGNORECASE) for p in group]
        self.location_regexes = compile_group(self.location_patterns)
        self.entity_regexes = compile_group(self.entity_patterns)
        self.measure_regexes = compile_group(self.measure_patterns)

    def match_location(self, text: str) -> bool:
        return any(r.search(text) for r in self.location_regexes)

    def match_entity(self, text: str) -> bool:
        return any(r.search(text) for r in self.entity_regexes)

    def match_measure(self, text: str) -> bool:
        return any(r.search(text) for r in self.measure_regexes)

    def match_custom(self, text: str) -> bool:
        return all(fn(text) for fn in self.custom_rules)

    def matches_all(self, text: str) -> bool:
        """General logical AND combination of all rule categories."""
        return (
            self.match_location(text)
            and self.match_entity(text)
            and self.match_measure(text)
            and self.match_custom(text)
        )

    @classmethod
    def from_json(cls, path: str) -> "RuleSet":
        with open(path, "r") as f:
            data = json.load(f)
        rs = cls(**data)
        rs.compile()
        return rs


# ========== Utility Functions ==========
def _safe_id_fragment(s: str, max_len: int = 120) -> str:
    frag = re.sub(r"[^A-Za-z0-9_.:/\-]+", "-", s)
    frag = re.sub(r"-{2,}", "-", frag).strip("-")
    return frag[:max_len] if frag else "entity"

def _unique_path(base_dir: str, filename_no_ext: str) -> str:
    path = os.path.join(base_dir, f"{filename_no_ext}.json")
    if not os.path.exists(path):
        return path
    i = 2
    while True:
        candidate = os.path.join(base_dir, f"{filename_no_ext}_{i}.json")
        if not os.path.exists(candidate):
            return candidate
        i += 1

def add_entity_to_requires(requires: Any, entity_id: str) -> Any:
    if isinstance(requires, dict):
        req = copy.deepcopy(requires)
        req["entityId"] = entity_id
        return req
    if isinstance(requires, list):
        req = copy.deepcopy(requires)
        req.append({"entityId": entity_id})
        return req
    return {"entityId": entity_id}

def make_task_instance(base_task: Dict[str, Any], entity_id: str) -> Dict[str, Any]:
    t = copy.deepcopy(base_task)
    base_name = t.get("name", "Task")
    base_id = t.get("taskId", "T")
    frag = _safe_id_fragment(entity_id)
    t["name"] = f"{base_name}::{entity_id}"
    t["taskId"] = f"{base_id}::{frag}"
    t["requires"] = add_entity_to_requires(t.get("requires"), entity_id)
    return t

def save_task_instance(instance: Dict[str, Any], out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    base = instance.get("taskId") or instance.get("name") or "task"
    fname = _safe_id_fragment(base)
    out_path = _unique_path(out_dir, fname)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(instance, f, indent=2, ensure_ascii=False)
    return out_path

# ========== Main Matching Logic ==========
def match_tasks_with_rules(
    root_node: Node,
    task_json_path: str,
    ruleset: RuleSet,
    out_dir: str = "expanded_tasks"
):
    # Collect all entity IDs using the prefix tree
    prefix_tree = PrefixTree()
    prefix_tree.root = root_node
    ids = prefix_tree.collect_all_ids()

    with open(task_json_path, "r", encoding="utf-8") as f:
        tasks = json.load(f)

    total_saved = 0
    for task in tasks:
        name = task.get("name")
        if ruleset.verbose:
            print(f"\nProcessing task: {name}")

        matched = [i for i in ids if ruleset.matches_all(i)]
        for mid in matched:
            instance = make_task_instance(task, mid)
            save_task_instance(instance, out_dir)
            total_saved += 1
            if ruleset.verbose:
                print(f"  → Matched entity: {mid}")

    print(f"\n Total saved task instances: {total_saved}")



# ========== Example Default RuleSet (building tasks) ==========
DEFAULT_RULESET = RuleSet(
    name="building_default",
    location_patterns=[r"\b(Building|Zone|Space)\b"],
    entity_patterns=[r"\bSensor\b"],
    measure_patterns=[r"\b(Accumulated[-_ ]?Load|Total[-_ ]?Load)\b"],
    verbose=True
)
DEFAULT_RULESET.compile()
