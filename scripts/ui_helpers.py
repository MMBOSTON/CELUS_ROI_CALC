import streamlit as st
from app_core import core_logic
import pandas as pd
import altair as alt
import pathlib

def metric_box(label, value):
    st.markdown(f"<div class='metric-box'><b>{label}</b><br><span class='stMetricValue'>{value}</span></div>", unsafe_allow_html=True)

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

def inject_custom_css():
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
        div[data-testid="stDownloadButton"] button#export_pdf_btn {
            background-color: #6d4c41;
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
        section[data-testid="stSidebar"] button {
            background-color: #90caf9 !important;
            color: #0d47a1 !important;
            border-radius: 0.3em !important;
            margin-bottom: 0.2em !important;
            font-size: 0.85rem !important;
            padding: 0.3em 0.7em !important;
            min-height: 1.7em !important;
            min-width: 1.7em !important;
        }
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

def render_scenario_card(idx, scenario, selected, tooltips, results_for_export, expand_all):
    if selected:
        st.markdown("<div class='scenario-card'>", unsafe_allow_html=True)
        cols = st.columns([0.5, 0.5], gap="small")
        with cols[0]:
            with st.expander(f"{scenario['label']} - Assumptions & Inputs", expanded=expand_all):
                bom, orders, conv, proto_prod, share, celus_conv, celus_share = scenario['defaults']
                bom_value = st.number_input(f"Average BOM Value $", value=bom, key=f"bom_{idx}", help=tooltips["bom"])
                bom_orders = st.number_input(f"Typical BOM volume # of orders", value=orders, key=f"orders_{idx}", help=tooltips["orders"])
                website_visitors = st.number_input(f"Website Visitors/month", value=25000, key=f"visitors_{idx}", help=tooltips["visitors"])
                conversion = st.number_input(f"% Conversion", value=conv, key=f"conv_{idx}", help=tooltips["conv"])
                prototype_to_prod = st.number_input(f"Prototype to Production", value=proto_prod, key=f"proto_{idx}", help=tooltips["proto"])
                share_bom = st.number_input(f"% Share of BOM", value=share, key=f"share_{idx}", help=tooltips["share"])
                celus_conversion = st.number_input(f"Increase in conversion to Active", value=celus_conv, key=f"celus_conv_{idx}", help=tooltips["celus_conv"])
                celus_share_bom = st.number_input(f"% Share of BOM with CELUS", value=celus_share, key=f"celus_share_{idx}", help=tooltips["celus_share"])
                errors = []
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
            with st.expander(f"{scenario['label']} - Results", expanded=expand_all):
                if 'errors' in locals() and errors:
                    st.warning("Please fix input errors to see results.")
                else:
                    results = core_logic.calculate_roi(
                        bom_value=bom_value,
                        bom_orders=bom_orders,
                        website_visitors=website_visitors,
                        conversion=conversion,
                        prototype_to_prod=prototype_to_prod,
                        share_bom=share_bom,
                        celus_conv=celus_conversion,
                        celus_share_bom=celus_share_bom
                    )
                    metric_box = globals().get('metric_box')
                    if metric_box:
                        metric_box("Total Value per BOM", f"${results['total_value_per_bom']:,.2f}")
                        metric_box("# Converted Users", f"{results['converted_users']:,.2f}")
                        metric_box("Total BOM Value from Users", f"${results['total_bom_value_from_users']:,.2f}")
                        metric_box("Value to Production", f"${results['value_to_production']:,.2f}")
                        metric_box("Revenue from Indirect Sales", f"${results['revenue_from_indirect_sales']:,.2f}")
                        metric_box("# Converted Users (CELUS)", f"{results['celus_converted_users']:,.2f}")
                        metric_box("Total BOM Value from Users (CELUS)", f"${results['celus_total_bom_value_from_users']:,.2f}")
                        metric_box("Value to Production (CELUS)", f"${results['celus_value_to_production']:,.2f}")
                        metric_box("Revenue from working with CELUS/month", f"${results['celus_revenue']:,.2f}")
                        metric_box("Multiplier", f"{results['multiplier']:,.2f}")
                        metric_box("Annual Revenue with CELUS", f"${results['annual_revenue_with_celus']:,.2f}")
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
                        "Total Value per BOM": results["total_value_per_bom"],
                        "# Converted Users": results["converted_users"],
                        "Total BOM Value from Users": results["total_bom_value_from_users"],
                        "Value to Production": results["value_to_production"],
                        "Revenue from Indirect Sales": results["revenue_from_indirect_sales"],
                        "# Converted Users (CELUS)": results["celus_converted_users"],
                        "Total BOM Value from Users (CELUS)": results["celus_total_bom_value_from_users"],
                        "Value to Production (CELUS)": results["celus_value_to_production"],
                        "Revenue from working with CELUS/month": results["celus_revenue"],
                        "Multiplier": results["multiplier"],
                        "Annual Revenue with CELUS": results["annual_revenue_with_celus"]
                    })
        st.markdown("</div>", unsafe_allow_html=True)

def render_comparison_table_and_charts(results_for_export):
    if len(results_for_export) > 1:
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

def render_export_buttons(results_for_export, core_logic, datetime):
    if results_for_export:
        import streamlit as st
        export_col1, export_col2, export_col3 = st.columns([1,1,1])
        with export_col1:
            csv = core_logic.export_results_to_csv(results_for_export)
            st.download_button(
                label="Export Results to CSV",
                data=csv,
                file_name=f"celus_roi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime='text/csv',
                key="export_csv_btn",
                help="Download results as CSV."
            )
        with export_col2:
            excel_buffer = core_logic.export_results_to_excel(results_for_export)
            st.download_button(
                label="Export Results to Excel",
                data=excel_buffer,
                file_name=f"celus_roi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                key="export_xlsx_btn",
                help="Download results as Excel."
            )
        with export_col3:
            pdf_bytes = core_logic.export_results_to_pdf(results_for_export)
            st.download_button(
                label="Export Results to PDF",
                data=pdf_bytes,
                file_name=f"celus_roi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime='application/pdf',
                key="export_pdf_btn",
                help="Download results as PDF."
            )

def render_sidebar_controls(st, state, scenario_manager):
    # Add Scenario
    if st.sidebar.button("Add Scenario"):
        state.scenarios = scenario_manager.add_scenario(state.scenarios)
        state.selected.append(True)
    # Remove Scenario
    remove_idx = st.sidebar.selectbox("Remove Scenario", [i for i, s in enumerate(state.scenarios)], format_func=lambda i: state.scenarios[i]["label"] if state.scenarios else "", key="remove_scenario")
    if st.sidebar.button("Remove Selected Scenario"):
        state.scenarios = scenario_manager.remove_scenario(state.scenarios, remove_idx)
        state.selected.pop(remove_idx)
    # Rename Scenario
    rename_idx = st.sidebar.selectbox("Rename Scenario", [i for i, s in enumerate(state.scenarios)], format_func=lambda i: state.scenarios[i]["label"] if state.scenarios else "", key="rename_scenario")
    new_name = st.sidebar.text_input("New Name", value=state.scenarios[rename_idx]["label"] if state.scenarios else "", key="rename_input")
    if st.sidebar.button("Rename"):
        state.scenarios = scenario_manager.rename_scenario(state.scenarios, rename_idx, new_name)
    # Selection checkboxes
    state.selected = [st.sidebar.checkbox(s["label"], value=state.selected[i], key=f"sel_{i}") for i, s in enumerate(state.scenarios)]
    # Save/Load
    col_save, col_load = st.sidebar.columns(2)
    with col_save:
        if st.button("Save Scenarios"):
            scenario_manager.save_scenarios_to_file(state.scenarios)
            st.sidebar.success("Scenarios saved!")
    with col_load:
        if st.button("Load Scenarios"):
            state.scenarios = scenario_manager.load_scenarios_from_file()
            state.selected = [True] * len(state.scenarios)
            st.sidebar.success("Scenarios loaded!")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Scenario Templates")
    new_template_name = st.sidebar.text_input("Template name", "my_template.json", key="template_name")
    if st.sidebar.button("Save Scenario Set as Template"):
        scenario_manager.save_template(state.scenarios, new_template_name)
        st.sidebar.success(f"Template saved as {new_template_name}")
    try:
        template_files = scenario_manager.list_templates()
    except Exception:
        template_files = []
    selected_template = st.sidebar.selectbox("Load Scenario Template", template_files, key="load_template_select")
    if st.sidebar.button("Load Selected Template") and selected_template:
        state.scenarios = scenario_manager.load_template(selected_template)
        state.selected = [True] * len(state.scenarios)
        st.sidebar.success(f"Loaded template: {selected_template}")

def render_sidebar_duplicate(st, state, scenario_manager):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Duplicate Scenario")
    dup_idx = st.sidebar.selectbox("Select Scenario to Duplicate", [i for i, s in enumerate(state.scenarios)], format_func=lambda i: state.scenarios[i]["label"] if state.scenarios else "", key="dup_scenario")
    if st.sidebar.button("Duplicate Selected Scenario"):
        state.scenarios = scenario_manager.duplicate_scenario(state.scenarios, dup_idx)
        state.selected.append(True)
        st.sidebar.success(f"Duplicated scenario: {state.scenarios[-1]['label']}")

def render_sidebar_import(st, state, scenario_manager, pathlib):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Import Scenarios")
    sample_template_path = pathlib.Path("sample_scenarios_template.csv")
    if sample_template_path.exists():
        with open(sample_template_path, "rb") as f:
            st.sidebar.download_button(
                label="Download Sample Import Template",
                data=f,
                file_name="sample_scenarios_template.csv",
                mime="text/csv",
                key="download_sample_template"
            )
    else:
        st.sidebar.info("Sample import template not found.")
    import_file = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"], key="import_file")
    if import_file is not None:
        try:
            state.scenarios = scenario_manager.import_scenarios_from_file(import_file)
            state.selected = [True] * len(state.scenarios)
            st.sidebar.success("Scenarios imported!")
        except Exception as e:
            st.sidebar.error(f"Import failed: {e}")
