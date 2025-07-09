"""
core_logic.py
Business logic for CELUS ROI Calculator.
Move your Excel/data processing, calculations, and core functions here.
"""
import json
import os
import pandas as pd
from datetime import datetime
import io
from fpdf import FPDF, XPos, YPos

# --- Scenario management ---
SCENARIO_FILE = "scenarios.json"
TEMPLATE_DIR = "templates"

# Default scenarios for single-file robustness
DEFAULT_SCENARIOS = [
    {
        "label": "Prototype - Simple Design",
        "defaults": (50, 10, 0.005, 0.25, 0.25, 0.0125, 0.4)
    },
    {
        "label": "Medium Volume - Simple Design",
        "defaults": (50, 300, 0.005, 0.25, 0.25, 0.0125, 0.4)
    },
    {
        "label": "High Volume - IoT Device",
        "defaults": (75, 5000, 0.005, 0.25, 0.25, 0.0075, 0.4)
    }
]

def load_scenarios():
    if os.path.exists(SCENARIO_FILE):
        with open(SCENARIO_FILE, "r") as f:
            return json.load(f)
    else:
        return DEFAULT_SCENARIOS.copy()

def save_scenarios(scenarios):
    with open(SCENARIO_FILE, "w") as f:
        json.dump(scenarios, f, indent=2)

# --- Calculation logic ---
def calculate_roi(bom_value, bom_orders, website_visitors, conversion, prototype_to_prod, share_bom, celus_conversion, celus_share_bom):
    total_value_per_bom = bom_value * bom_orders
    converted_users = website_visitors * conversion
    total_bom_value_from_users = converted_users * total_value_per_bom
    value_to_production = total_bom_value_from_users * prototype_to_prod
    revenue_from_indirect_sales = value_to_production * share_bom
    # CELUS
    celus_converted_users = website_visitors * celus_conversion
    celus_total_bom_value_from_users = celus_converted_users * total_value_per_bom
    celus_value_to_production = celus_total_bom_value_from_users * prototype_to_prod
    celus_revenue = celus_value_to_production * celus_share_bom
    multiplier = celus_revenue / revenue_from_indirect_sales if revenue_from_indirect_sales else 0
    annual_revenue_with_celus = celus_revenue * 12
    return {
        "Total Value per BOM": total_value_per_bom,
        "# Converted Users": converted_users,
        "Total BOM Value from Users": total_bom_value_from_users,
        "Value to Production": value_to_production,
        "Revenue from Indirect Sales": revenue_from_indirect_sales,
        "# Converted Users (CELUS)": celus_converted_users,
        "Total BOM Value from Users (CELUS)": celus_total_bom_value_from_users,
        "Value to Production (CELUS)": celus_value_to_production,
        "Revenue from working with CELUS/month": celus_revenue,
        "Multiplier": multiplier,
        "Annual Revenue with CELUS": annual_revenue_with_celus
    }

# --- Export results ---
def export_results_to_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(200, 10, text="CELUS ROI Calculator Results", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(5)
    for scenario in results:
        pdf.set_font("helvetica", style="B", size=11)
        pdf.cell(0, 8, text=f"Scenario: {scenario['Scenario']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("helvetica", size=10)
        for k, v in scenario.items():
            if k != "Scenario":
                pdf.cell(0, 7, text=f"{k}: {v}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(4)
    return bytes(pdf.output())

def export_results_to_csv(results):
    df_export = pd.DataFrame(results)
    return df_export.to_csv(index=False).encode('utf-8')

def export_results_to_excel(results):
    df_export = pd.DataFrame(results)
    excel_buffer = io.BytesIO()
    df_export.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)
    return excel_buffer

# --- Autosave ---
def autosave_scenarios(scenarios):
    try:
        save_scenarios(scenarios)
    except Exception as e:
        print(f"Auto-save failed: {e}")

__all__ = [
    "load_scenarios", "save_scenarios", "DEFAULT_SCENARIOS", "calculate_roi",
    "export_results_to_pdf", "export_results_to_csv", "export_results_to_excel", "autosave_scenarios"
]
