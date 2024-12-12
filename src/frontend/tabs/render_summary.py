import streamlit as st
import plotly.graph_objects as go
import random
from datetime import datetime  # Added import

from backend.data_handler import DataHandler
from frontend.utils.edit_folder_metadata import edit_folder_metadata
from frontend.utils.render_section_header import render_section_header
from frontend.compute.summary_viz import create_axle_grouped_bar_chart, create_clubbed_horizontal_bar_chart

def render_summary():
    render_section_header(
        "System Summary",
        "Overview of system health and key metrics across all logs.",
        "📈"
    )
    
    edit_folder_metadata()

    # Initialize visibility states
    if 'show_tables' not in st.session_state:
        st.session_state.show_tables = True
    if 'show_charts' not in st.session_state:
        st.session_state.show_charts = True
    if 'axle_mode' not in st.session_state:
        st.session_state.axle_mode = False

    # Toolbar row
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("Toggle Tables", help="Show/Hide all tables"):
            st.session_state.show_tables = not st.session_state.show_tables
    with col2:
        if st.button("Toggle Charts", help="Show/Hide all charts"):
            st.session_state.show_charts = not st.session_state.show_charts
    with col3:
        if 'axle_mode_dict' not in st.session_state:
            st.session_state.axle_mode_dict = {}
        if st.button("Toggle Graph Mode", help="Switch between Error/Axle grouping"):
            for table_name, df in st.session_state.data_handler.tables.items():
                if len(df.columns) >= 3:
                    st.session_state.axle_mode_dict[table_name] = not st.session_state.axle_mode_dict.get(table_name, False)
                else:
                    st.session_state.axle_mode_dict[table_name] = False
    with col4:
        def update_color_seed():
            st.session_state.color_seed = random.randint(1, 100)
        if 'color_seed' not in st.session_state:
            st.session_state.color_seed = random.randint(1, 100)
        st.button("Change Color Palette", help="Randomize chart colors", on_click=update_color_seed)

    try:
        if not st.session_state.data_handler.tables:
            st.warning("No tables found. Please upload a folder first to analyze it.")
        else:
            for table_name, df in st.session_state.data_handler.tables.items():
                st.markdown(f"### {table_name}")
                left_col, right_col = st.columns(2)
                with left_col:
                    if st.session_state.show_tables:
                        st.dataframe(df)
                with right_col:
                    if st.session_state.show_charts:
                        axle_mode = st.session_state.axle_mode_dict.get(table_name, False)
                        if axle_mode and len(df.columns) < 3:
                            fig = create_clubbed_horizontal_bar_chart(df, st.session_state.color_seed)
                            st.info("Need at least 2 value columns to show axle-grouped view.")
                        else:
                            fig = create_clubbed_horizontal_bar_chart(df, st.session_state.color_seed) if not axle_mode else create_axle_grouped_bar_chart(df, st.session_state.color_seed)
                        st.plotly_chart(fig, key=f"{table_name}_{axle_mode}")
    except AttributeError:
        st.warning("Please upload a folder first to analyze it.")


