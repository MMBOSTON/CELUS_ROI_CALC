# CELUS ROI Calculator Streamlit App
# This is a direct copy of scripts/roi_calculator_app.py for cloud deployment.

# print("ROI Calculator app started")
import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
import io
import altair as alt
from fpdf import FPDF, XPos, YPos
import pathlib

st.set_page_config(page_title="CELUS ROI Calculator", layout="wide")

# --- Session state initialization (must be at the top!) ---
if "expand_all" not in st.session_state:
    st.session_state.expand_all = False

# --- Scenario management helpers ---
SCENARIO_FILE = "scenarios.json"
TEMPLATE_DIR = "templates"

# Default scenarios
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

# Load scenarios from file or use defaults
if os.path.exists(SCENARIO_FILE):
    with open(SCENARIO_FILE, "r") as f:
        scenarios = json.load(f)
else:
    scenarios = DEFAULT_SCENARIOS.copy()

# Ensure template directory exists
os.makedirs(TEMPLATE_DIR, exist_ok=True)

# --- Sidebar: Logo, Instructions and Scenario selection ---
st.sidebar.markdown("""
**Instructions:**

Select one or more scenarios below to view and adjust their assumptions and see the calculated ROI results. The average BOM Values & Revenues are based on Monthly estimates, and the calculations will show how working with CELUS can impact your business.
""")

# --- Sidebar: Select Scenarios (Collapsible) ---
with st.sidebar.expander("Select Scenarios", expanded=False):
    # Scenario customization (add/remove/rename)
    if "scenarios" not in st.session_state:
        # Always start with only the three default scenarios unless loading from file
        st.session_state.scenarios = [s.copy() for s in DEFAULT_SCENARIOS]
    if "selected" not in st.session_state or len(st.session_state.selected) != len(st.session_state.scenarios):
        st.session_state.selected = [True] * len(st.session_state.scenarios)

    # Add scenario
    if st.button("Add Scenario"):
        st.session_state.scenarios.append({
            "label": f"Custom Scenario {len(st.session_state.scenarios)+1}",
            "defaults": (50, 100, 0.005, 0.25, 0.25, 0.01, 0.4)
        })
        st.session_state.selected.append(True)

    # Remove scenario
    remove_idx = st.selectbox("Remove Scenario", [i for i, s in enumerate(st.session_state.scenarios)], format_func=lambda i: st.session_state.scenarios[i]["label"] if st.session_state.scenarios else "", key="remove_scenario")
    if st.button("Remove Selected Scenario") and len(st.session_state.scenarios) > 1:
        st.session_state.scenarios.pop(remove_idx)
        st.session_state.selected.pop(remove_idx)

    # Rename scenario
    rename_idx = st.selectbox("Rename Scenario", [i for i, s in enumerate(st.session_state.scenarios)], format_func=lambda i: st.session_state.scenarios[i]["label"] if st.session_state.scenarios else "", key="rename_scenario")
    new_name = st.text_input("New Name", value=st.session_state.scenarios[rename_idx]["label"] if st.session_state.scenarios else "", key="rename_input")
    if st.button("Rename"):
        st.session_state.scenarios[rename_idx]["label"] = new_name

    # Scenario selection checkboxes
    st.session_state.selected = [st.checkbox(s["label"], value=st.session_state.selected[i], key=f"sel_{i}") for i, s in enumerate(st.session_state.scenarios)]

    # Save/load scenarios
    col_save, col_load = st.columns(2)
    with col_save:
        if st.button("Save Scenarios"):
            with open(SCENARIO_FILE, "w") as f:
                json.dump(st.session_state.scenarios, f, indent=2)
            st.success("Scenarios saved!")
    with col_load:
        if st.button("Load Scenarios"):
            if os.path.exists(SCENARIO_FILE):
                with open(SCENARIO_FILE, "r") as f:
                    st.session_state.scenarios = json.load(f)
                st.session_state.selected = [True] * len(st.session_state.scenarios)
                st.success("Scenarios loaded!")
            else:
                st.error("No saved scenarios found.")

# --- Sidebar: Scenario Templates (Collapsible) ---
with st.sidebar.expander("Scenario Templates", expanded=False):
    # Save current scenarios as template
    new_template_name = st.text_input("Template name", "my_template.json", key="template_name")
    if st.button("Save Scenario Set as Template"):
        template_path = os.path.join(TEMPLATE_DIR, new_template_name)
        with open(template_path, "w") as f:
            json.dump(st.session_state.scenarios, f, indent=2)
        st.success(f"Template saved as {new_template_name}")

    # List available templates
    try:
        template_files = [f for f in os.listdir(TEMPLATE_DIR) if f.endswith(".json")]
    except Exception:
        template_files = []

    selected_template = st.selectbox("Load Scenario Template", template_files, key="load_template_select")
    if st.button("Load Selected Template") and selected_template:
        template_path = os.path.join(TEMPLATE_DIR, selected_template)
        with open(template_path, "r") as f:
            st.session_state.scenarios = json.load(f)
        st.session_state.selected = [True] * len(st.session_state.scenarios)
        st.success(f"Loaded template: {selected_template}")

# --- Sidebar: Duplicate Scenario (Collapsible) ---
with st.sidebar.expander("Duplicate Scenario", expanded=False):
    dup_idx = st.selectbox("Select Scenario to Duplicate", [i for i, s in enumerate(st.session_state.scenarios)], format_func=lambda i: st.session_state.scenarios[i]["label"] if st.session_state.scenarios else "", key="dup_scenario")
    if st.button("Duplicate Selected Scenario"):
        import copy
        new_scenario = copy.deepcopy(st.session_state.scenarios[dup_idx])
        new_scenario["label"] += " (Copy)"
        st.session_state.scenarios.append(new_scenario)
        st.session_state.selected.append(True)
        st.success(f"Duplicated scenario: {new_scenario['label']}")

# --- Sidebar: Import Scenarios (Collapsible) ---
with st.sidebar.expander("Import Scenarios", expanded=False):
    sample_template_path = pathlib.Path("sample_scenarios_template.csv")
    if sample_template_path.exists():
        with open(sample_template_path, "rb") as f:
            st.download_button(
                label="Download Sample Import Template",
                data=f,
                file_name="sample_scenarios_template.csv",
                mime="text/csv",
                key="download_sample_template"
            )
    else:
        st.info("Sample import template not found.")
    import_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"], key="import_file")
    if import_file is not None:
        try:
            if import_file.name.endswith(".csv"):
                df_import = pd.read_csv(import_file)
            else:
                df_import = pd.read_excel(import_file)
            # Expect columns: label, bom, orders, conv, proto, share, celus_conv, celus_share
            required_cols = ["label", "bom", "orders", "conv", "proto", "share", "celus_conv", "celus_share"]
            if all(col in df_import.columns for col in required_cols):
                st.session_state.scenarios = [
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
                st.session_state.selected = [True] * len(st.session_state.scenarios)
                st.success("Scenarios imported!")
            else:
                st.error(f"Missing columns: {set(required_cols) - set(df_import.columns)}")
        except Exception as e:
            st.error(f"Import failed: {e}")

# --- Custom CSS for button coloring and column width ---
st.markdown(
    """
    <style>
    /* Export buttons */
    div[data-testid="stDownloadButton"] button#export_csv_btn {
        background-color: #1976d2;
        color: white;
    }
    div[data-testid="stDownloadButton"] button#export_xlsx_btn {
        background-color: #388e3c;
        color: white;
    }
    /* Expand/Collapse buttons */
    div[data-testid="stButton"] button#expand_all_btn {
        background-color: #4CAF50;
        color: white;
        border-radius: 0.3em;
        font-weight: bold;
    }
    div[data-testid="stButton"] button#collapse_all_btn {
        background-color: #f44336;
        color: white;
        border-radius: 0.3em;
        font-weight: bold;
    }
    /* Sidebar Save/Load/Scenario buttons and all sidebar buttons smaller and light blue */
    section[data-testid="stSidebar"] button {
        background-color: #90caf9 !important;
        color: #0d47a1 !important;
        border-radius: 0.2em !important;
        margin-bottom: 0.1em !important;
        font-size: 0.8rem !important;
        padding: 0.2em 0.5em !important;
        min-height: 1.3em !important;
        min-width: 1.3em !important;
    }
    /* Sidebar subheader spacing */
    section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        margin-top: 0.3em !important;
        margin-bottom: 0.2em !important;
    }
    /* Sidebar markdown and widget spacing tighter */
    section[data-testid="stSidebar"] .block-container > div > div {
        margin-bottom: 0.15em !important;
    }
    section[data-testid="stSidebar"] .stTextInput, section[data-testid="stSidebar"] .stSelectbox, section[data-testid="stSidebar"] .stFileUploader, section[data-testid="stSidebar"] .stCheckbox {
        margin-bottom: 0.1em !important;
    }
    /* Color all other white buttons (main area) */
    .stButton > button {
        background-color: #1976d2 !important;
        color: white !important;
        border-radius: 0.2em !important;
        font-weight: 500;
        font-size: 0.95rem !important;
        padding: 0.2em 0.7em !important;
    }
    /* Make scenario card columns and metric/input boxes narrower */
    .block-container .scenario-card .stColumns {
        gap: 0.1rem !important; /* ultra tight */
    }
    .block-container .scenario-card .element-container > div > div[data-testid="column"] {
        max-width: 150px !important;
        min-width: 80px !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    .scenario-card .metric-box, .scenario-card .stNumberInput, .scenario-card .stTextInput {
        max-width: 140px !important;
        min-width: 80px !important;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 0.08rem !important;
        padding-top: 0.08rem !important;
        padding-bottom: 0.08rem !important;
    }
    .scenario-card .stExpanderContent {
        padding-left: 0.05rem !important;
        padding-right: 0.05rem !important;
    }
    /* Reduce scenario card and metric box padding and border radius */
    .scenario-card {
        background: #f4f8fc;
        border-radius: 0.3rem !important;
        padding: 0.3rem 0.3rem 0.2rem 0.3rem !important;
        margin-bottom: 0.7rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        border: 1px solid #e3e8ee;
        display: flex;
        flex-direction: row;
        align-items: stretch;
    }
    .metric-box {
        background: #eaf3fb;
        border-radius: 0.2rem !important;
        padding: 0.15rem 0.3rem 0.1rem 0.3rem !important;
        margin-bottom: 0.08rem !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    /* Expander header compactness and alignment */
    .stExpander > summary {
        min-width: 0 !important;
        padding: 0.08rem 0.2rem 0.08rem 0.2rem !important;
        font-size: 0.98rem !important;
        font-weight: 600 !important;
        background: #e3e8ee !important;
        border-radius: 0.2rem !important;
        margin-bottom: 0.05rem !important;
    }
    .stExpander > summary span {
        width: 100% !important;
        display: inline-block !important;
        text-align: left !important;
    }
    /* Try to align both columns to same height (best effort) */
    .scenario-card .stColumns {
        align-items: stretch !important;
        display: flex !important;
    }
    .scenario-card .stColumns > div[data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
        justify-content: stretch !important;
    }
    /* Reduce font size for input labels and metric values */
    .scenario-card label, .scenario-card .stExpanderContent label {
        font-size: 0.92rem !important;
        margin-bottom: 0.01rem !important;
    }
    .metric-box .stMetricValue {
        font-size: 1.01rem !important;
    }
    /* Force scenario card columns to equal height */
    .scenario-card .stColumns {
        display: flex !important;
        align-items: stretch !important;
        min-height: 100%;
    }
    .scenario-card .stColumns > div[data-testid="column"] {
        display: flex !important;
        flex-direction: column !important;
        justify-content: stretch !important;
        min-height: 100%;
    }
    .scenario-card .stExpander {
        flex: 1 1 auto !important;
        display: flex !important;
        flex-direction: column !important;
        min-height: 100%;
    }
    .scenario-card .stExpanderContent {
        flex: 1 1 auto !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        min-height: 100%;
    }
    /* Make both columns (Assumptions & Inputs and Results) widgets even more compact */
    .scenario-card .stExpanderContent > div > div[data-testid="column"] {
        max-width: 140px !important;
        min-width: 80px !important;
        padding-left: 0.01rem !important;
    .scenario-card .stExpanderContent label {
        margin-bottom: 0.01rem !important;
        font-size: 0.90rem !important;
    }
    .scenario-card .stExpanderContent .stExpander {
        margin-bottom: 0.01rem !important;
    }
    /* Reduce vertical spacing between metric/input boxes */
    .scenario-card .metric-box {
        margin-bottom: 0.18rem !important;
        padding-top: 0.35rem !important;
        padding-bottom: 0.35rem !important;
    }
    /* Reduce font size for metric labels and values */
    .scenario-card .metric-box b {
        font-size: 0.97rem !important;
    }
    .scenario-card .metric-box .stMetricValue {
        font-size: 1.00rem !important;
    }
    /* Make expander headers more compact */
    .scenario-card .stExpander > summary {
        min-height: 1.2em !important;
        padding-top: 0.1em !important;
        padding-bottom: 0.1em !important;
    }
    .scenario-card .stExpander > summary span {
        font-size: 1.00rem !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- App Header and Description ---
st.markdown("""
# CELUS ROI CALCULATOR

**What does this app do?**

The CELUS ROI Calculator helps component manufacturers and suppliers estimate the financial impact of using the CELUS AI-based PCB design platform. By simulating different PCB production (BOM) scenarios, you can see how CELUS can increase lead generation, improve conversion rates, and boost indirect sales revenue. 

**Value Proposition:**
- Quantifies the business value of CELUS for your organization
- Models multiple scenarios for different product/volume types
- Shows the uplift in revenue and conversion from CELUS adoption
- Enables data-driven decision making for digital transformation
""", unsafe_allow_html=True)

# --- Main UI ---
st.subheader("Assumptions & Inputs    |    Results")
# Add UI/UX enhancements: scenario cards, consistent styling, expand/collapse all
st.markdown(
    """
    <style>
    .scenario-card {
        background: #f4f8fc;
        border-radius: 0.75rem;
        padding: 1.5rem 1.5rem 1.25rem 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #e3e8ee;
    }
    .metric-box {
        background: #eaf3fb;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem 0.5rem 1rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .metric-box .stMetricValue { font-size: 1.1rem !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# Expand/collapse all logic
expand_col, collapse_col = st.columns([1, 1])
with expand_col:
    expand_btn = st.button("Expand All", key="expand_all_btn")
    st.markdown('<style>div[data-testid="stButton"] button#expand_all_btn {background-color: #4CAF50; color: white;}</style>', unsafe_allow_html=True)
with collapse_col:
    collapse_btn = st.button("Collapse All", key="collapse_all_btn")
    st.markdown('<style>div[data-testid="stButton"] button#collapse_all_btn {background-color: #f44336; color: white;}</style>', unsafe_allow_html=True)

# Custom button styles
st.markdown(
    """
    <style>
    .stButton > button {
        margin-right: 0.5em;
    }
    .export-csv-btn {
        background-color: #1976d2 !important;
        color: white !important;
    }
    .export-xlsx-btn {
        background-color: #388e3c !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if expand_btn:
    st.session_state.expand_all = True
if collapse_btn:
    st.session_state.expand_all = False

def metric_box(label, value):
    st.markdown(f"<div class='metric-box'><b>{label}</b><br><span class='stMetricValue'>{value}</span></div>", unsafe_allow_html=True)

# --- Results for export ---
results_for_export = []

# --- Tooltips for inputs ---
tooltips = {
    "bom": "Average Bill of Materials (BOM) value in USD per order.",
    "orders": "Number of BOM orders per month.",
    "visitors": "Monthly website visitors.",
    "conv": "Fraction of visitors converting to leads (e.g., 0.005 = 0.5%).",
    "proto": "Fraction of prototypes that go to production (e.g., 0.25 = 25%).",
    "share": "Share of BOM revenue captured (e.g., 0.25 = 25%).",
    "celus_conv": "Fraction of visitors converting to leads with CELUS.",
    "celus_share": "Share of BOM revenue captured with CELUS."
}

# Only render scenario cards if there is at least one selected scenario
display_any = any(st.session_state.selected)
if display_any:
    for idx, scenario in enumerate(st.session_state.scenarios):
        if not st.session_state.selected[idx]:
            continue
        errors = []
        st.markdown("<div class='scenario-card'>", unsafe_allow_html=True)
        # Make columns even narrower: 32% for inputs, 32% for results, 36% spacer
        cols = st.columns([0.32, 0.32, 0.36], gap="small")
        with cols[0]:
            with st.expander(f"{scenario['label']} - Assumptions & Inputs", expanded=st.session_state.expand_all):
                bom, orders, conv, proto_prod, share, celus_conv, celus_share = scenario['defaults']
                bom_value = st.number_input(f"Average BOM Value $", value=bom, key=f"bom_{idx}", help=tooltips["bom"])
                bom_orders = st.number_input(f"Typical BOM volume # of orders", value=orders, key=f"orders_{idx}", help=tooltips["orders"])
                website_visitors = st.number_input(f"Website Visitors/month", value=25000, key=f"visitors_{idx}", help=tooltips["visitors"])
                conversion = st.number_input(f"% Conversion", value=conv, key=f"conv_{idx}", help=tooltips["conv"])
                prototype_to_prod = st.number_input(f"Prototype to Production", value=proto_prod, key=f"proto_{idx}", help=tooltips["proto"])
                share_bom = st.number_input(f"% Share of BOM", value=share, key=f"share_{idx}", help=tooltips["share"])
                celus_conversion = st.number_input(f"Increase in conversion to Active", value=celus_conv, key=f"celus_conv_{idx}", help=tooltips["celus_conv"])
                celus_share_bom = st.number_input(f"% Share of BOM with CELUS", value=celus_share, key=f"celus_share_{idx}", help=tooltips["celus_share"])
                # Input validation
                if bom_value < 0: errors.append("BOM Value must be non-negative.")
                if bom_orders < 0: errors.append("BOM Orders must be non-negative.")
                if website_visitors < 0: errors.append("Website Visitors must be non-negative.")
                for val, name in zip([conversion, prototype_to_prod, share_bom, celus_conversion, celus_share_bom],
                                     ["% Conversion", "Prototype to Production", "% Share of BOM", "Increase in conversion to Active", "% Share of BOM with CELUS"]):
                    if not (0 <= val <= 1):
                        errors.append(f"{name} must be between 0 and 1.")
                if errors:
                    for e in errors:
                        st.error(e)
        with cols[1]:
            if not errors:
                with st.expander(f"{scenario['label']} - Results", expanded=st.session_state.expand_all):
                    total_value_per_bom = bom_value * bom_orders
                    converted_users = website_visitors * conversion
                    total_bom_value_from_users = converted_users * total_value_per_bom
                    value_to_production = total_bom_value_from_users * prototype_to_prod
                    revenue_from_indirect_sales = value_to_production * share_bom
                    # CELUS
                    celus_converted_users = website_visitors * celus_conversion
                    celus_total_bom_value_from_users = celus_converted_users * total_bom_value_from_users
                    celus_value_to_production = celus_total_bom_value_from_users * prototype_to_prod
                    celus_revenue = celus_value_to_production * celus_share_bom
                    multiplier = celus_revenue / revenue_from_indirect_sales if revenue_from_indirect_sales else 0
                    annual_revenue_with_celus = celus_revenue * 12
                    metric_box("Total Value per BOM", f"${total_value_per_bom:,.2f}")
                    metric_box("# Converted Users", f"{converted_users:,.2f}")
                    metric_box("Total BOM Value from Users", f"${total_bom_value_from_users:,.2f}")
                    metric_box("Value to Production", f"${value_to_production:,.2f}")
                    metric_box("Revenue from Indirect Sales", f"${revenue_from_indirect_sales:,.2f}")
                    metric_box("# Converted Users (CELUS)", f"{celus_converted_users:,.2f}")
                    metric_box("Total BOM Value from Users (CELUS)", f"${celus_total_bom_value_from_users:,.2f}")
                    metric_box("Value to Production (CELUS)", f"${celus_value_to_production:,.2f}")
                    metric_box("Revenue from working with CELUS/month", f"${celus_revenue:,.2f}")
                    metric_box("Multiplier", f"{multiplier:,.2f}")
                    metric_box("Annual Revenue with CELUS", f"${annual_revenue_with_celus:,.2f}")
                    # For export
                    results_for_export.append({
                        "Scenario": scenario["label"],
                        "BOM Value": bom_value,
                        "BOM Orders": bom_orders,
                        "Website Visitors": website_visitors,
                        "% Conversion": conversion,
                        "Prototype to Production": prototype_to_prod,
                        "% Share of BOM": share_bom,
                        "Increase in conversion to Active": celus_conv,
                        "% Share of BOM with CELUS": celus_share_bom,
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
                    })
        st.markdown("</div>", unsafe_allow_html=True)

# --- Scenario Comparison Table & Visualization ---

if len(results_for_export) > 1:
    st.markdown('<div class="comparison-container">', unsafe_allow_html=True)
    with st.expander("Scenario Comparison Table", expanded=False):
        st.markdown("<span style='font-size:1.1rem; font-weight:600;'>Scenario Comparison Table</span>", unsafe_allow_html=True)
        df_compare = pd.DataFrame(results_for_export)
        st.dataframe(df_compare.set_index("Scenario"), use_container_width=True)

    with st.expander("Scenario Comparison Charts", expanded=False):
        st.markdown("<span style='font-size:1.1rem; font-weight:600;'>Scenario Comparison Charts</span>", unsafe_allow_html=True)
        chart_type = st.radio(
            "Select chart type:",
            ["Bar (Single Metric)", "Grouped Bar (Multiple Metrics)"],
            horizontal=True,
            key="chart_type_radio"
        )
        if chart_type == "Bar (Single Metric)":
            metric = st.selectbox(
                "Select metric to compare:",
                ["Annual Revenue with CELUS", "Multiplier", "# Converted Users", "Revenue from Indirect Sales"],
                key="bar_metric_select"
            )
            chart = alt.Chart(df_compare).mark_bar().encode(
                x=alt.X('Scenario:N', title='Scenario'),
                y=alt.Y(f'{metric}:Q', title=metric),
                color=alt.Color('Scenario:N', legend=None)
            ).properties(title=f'{metric} by Scenario', width=500)
            st.altair_chart(chart, use_container_width=True)
        else:
            metrics = st.multiselect(
                "Select metrics to compare:",
                ["Annual Revenue with CELUS", "Multiplier", "# Converted Users", "Revenue from Indirect Sales"],
                default=["Annual Revenue with CELUS", "Multiplier"],
                key="grouped_bar_metrics"
            )
            if metrics:
                df_melt = df_compare.melt(id_vars=["Scenario"], value_vars=metrics, var_name="Metric", value_name="Value")
                chart = alt.Chart(df_melt).mark_bar().encode(
                    x=alt.X('Scenario:N', title='Scenario'),
                    y=alt.Y('Value:Q'),
                    color=alt.Color('Metric:N', title='Metric'),
                    column=alt.Column('Metric:N', title=None)
                ).properties(title='Grouped Bar Chart by Scenario', width=150)
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Select at least one metric to display grouped bar chart.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Custom CSS for comparison container alignment ---
st.markdown(
    """
    <style>
    .comparison-container {
        max-width: 670px;
        margin-left: auto;
        margin-right: auto;
        margin-top: 0.5rem;
        margin-bottom: 1.2rem;
    }
    .comparison-container .stExpander {
        margin-bottom: 0.7rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

if results_for_export:
    df_export = pd.DataFrame(results_for_export)
    export_col1, export_col2, export_col3 = st.columns([1,1,1])
    with export_col1:
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Export Results to CSV",
            data=csv,
            file_name=f"celus_roi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime='text/csv',
            key="export_csv_btn",
            help="Download results as CSV."
        )
        st.markdown('<style>div[data-testid="stDownloadButton"] button {background-color: #1976d2; color: white;}</style>', unsafe_allow_html=True)
    with export_col2:
        excel_buffer = io.BytesIO()
        df_export.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button(
            label="Export Results to Excel",
            data=excel_buffer,
            file_name=f"celus_roi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            key="export_xlsx_btn",
            help="Download results as Excel."
        )
        st.markdown('<style>div[data-testid="stDownloadButton"] button {background-color: #388e3c; color: white;</style>', unsafe_allow_html=True)
    with export_col3:
        pdf_bytes = export_results_to_pdf(results_for_export)
        st.download_button(
            label="Export Results to PDF",
            data=pdf_bytes,
            file_name=f"celus_roi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime='application/pdf',
            key="export_pdf_btn",
            help="Download results as PDF."
        )
        st.markdown('<style>div[data-testid="stDownloadButton"] button {background-color: #6d4c41; color: white;}</style>', unsafe_allow_html=True)

# --- Stop/Rerun button in UI ---
stop_col, rerun_col = st.columns([1, 1])
with stop_col:
    if st.button("Stop App", key="stop_app_btn"):
        st.stop()
with rerun_col:
    if st.button("Rerun App", key="rerun_app_btn"):
        st.rerun()

# --- Make right-side subheaders smaller ---
st.markdown("""
<style>
/* Make right-side subheaders (Results) smaller */
section.main .stExpander > summary span, .scenario-card .stExpander > summary span {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Auto-save scenario changes ---
def autosave_scenarios():
    try:
        with open(SCENARIO_FILE, "w") as f:
            json.dump(st.session_state.scenarios, f, indent=2)
    except Exception as e:
        st.sidebar.warning(f"Auto-save failed: {e}")

# Call autosave after any scenario change
scenario_keys = ["scenarios", "selected"]
if any(k in st.session_state for k in scenario_keys):
    autosave_scenarios()

# Update all file paths to use 'Template/ROI Calculator_v1.xlsx' or similar, instead of just the filename.

# --- Custom CSS for both columns compactness ---
st.markdown(
    """
    <style>
    /* Make both columns (Assumptions & Inputs and Results) widgets even more compact */
    .scenario-card .stExpanderContent > div > div[data-testid="column"] {
        max-width: 140px !important;
        min-width: 80px !important;
        padding-left: 0.01rem !important;
        padding-right: 0.01rem !important;
    }
    .scenario-card .stExpanderContent .stNumberInput, .scenario-card .stExpanderContent .stTextInput {
        margin-bottom: 0.01rem !important;
        padding-top: 0.01rem !important;
        padding-bottom: 0.01rem !important;
    }
    .scenario-card .stExpanderContent label {
        margin-bottom: 0.01rem !important;
        font-size: 0.90rem !important;
    }
    .scenario-card .stExpanderContent .stExpander {
        margin-bottom: 0.01rem !important;
    }
    /* Reduce vertical spacing between metric/input boxes */
    .scenario-card .metric-box {
        margin-bottom: 0.18rem !important;
        padding-top: 0.35rem !important;
        padding-bottom: 0.35rem !important;
    }
    /* Reduce font size for metric labels and values */
    .scenario-card .metric-box b {
        font-size: 0.97rem !important;
    }
    .scenario-card .metric-box .stMetricValue {
        font-size: 1.00rem !important;
    }
    /* Make expander headers more compact */
    .scenario-card .stExpander > summary {
        min-height: 1.2em !important;
        padding-top: 0.1em !important;
        padding-bottom: 0.1em !important;
    }
    .scenario-card .stExpander > summary span {
        font-size: 1.00rem !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
