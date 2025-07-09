import os
import json
import pandas as pd
import copy
from app_core import core_logic

SCENARIO_FILE = "scenarios.json"
TEMPLATE_DIR = "templates"

# Scenario management functions

def load_scenarios_from_file():
    if os.path.exists(SCENARIO_FILE):
        with open(SCENARIO_FILE, "r") as f:
            return json.load(f)
    return [s.copy() for s in core_logic.DEFAULT_SCENARIOS]

def save_scenarios_to_file(scenarios):
    with open(SCENARIO_FILE, "w") as f:
        json.dump(scenarios, f, indent=2)

def add_scenario(scenarios):
    scenarios.append({
        "label": f"Custom Scenario {len(scenarios)+1}",
        "defaults": (50, 100, 0.005, 0.25, 0.25, 0.01, 0.4)
    })
    return scenarios

def remove_scenario(scenarios, idx):
    if len(scenarios) > 1:
        scenarios.pop(idx)
    return scenarios

def rename_scenario(scenarios, idx, new_name):
    scenarios[idx]["label"] = new_name
    return scenarios

def duplicate_scenario(scenarios, idx):
    new_scenario = copy.deepcopy(scenarios[idx])
    new_scenario["label"] += " (Copy)"
    scenarios.append(new_scenario)
    return scenarios

def save_template(scenarios, template_name):
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    with open(template_path, "w") as f:
        json.dump(scenarios, f, indent=2)
    return template_path

def list_templates():
    try:
        return [f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".json")]
    except Exception:
        return []

def load_template(template_name):
    template_path = os.path.join(TEMPLATE_DIR, template_name)
    with open(template_path, "r") as f:
        return json.load(f)

def import_scenarios_from_file(import_file):
    if import_file.name.endswith(".csv"):
        df_import = pd.read_csv(import_file)
    else:
        df_import = pd.read_excel(import_file)
    required_cols = ["label", "bom", "orders", "conv", "proto", "share", "celus_conv", "celus_share"]
    if all(col in df_import.columns for col in required_cols):
        return [
            {
                "label": row["label"],
                "defaults": (
                    float(row["bom"]),
                    float(row["orders"]),
                    float(row["conv"]),
                    float(row["proto"]),
                    float(row["share"]),
                    float(row["celus_conv"]),
                    float(row["celus_share"]),
                ),
            }
            for _, row in df_import.iterrows()
        ]
    else:
        missing = set(required_cols) - set(df_import.columns)
        raise ValueError(f"Missing columns: {missing}")
