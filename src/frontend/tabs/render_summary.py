import streamlit as st
import plotly.graph_objects as go
import random
from datetime import datetime  # Added import

from backend.data_handler import DataHandler
from frontend.utils.render_section_header import render_section_header
from frontend.compute.summary_viz import create_clubbed_horizontal_bar_chart

def render_summary():
    render_section_header(
        "System Summary",
        "Overview of system health and key metrics across all logs.",
        "📈"
    )
    # Settings to edit and save folder metadata moved from settings panel to here
    # Add inputs for Date, Depot Name, and Coach Name
    col1, col2, col3 = st.columns(3)
    with col1:
        # Date input
        date_value = None
        if 'folder_date' not in st.session_state:
            st.session_state.folder_date = datetime.now().strftime("%d-%m-%Y")
        else:
            try:
                date_value = datetime.strptime(st.session_state.folder_date, "%d-%m-%Y")
            except:
                pass
        new_date = st.date_input(
            "Date",
            value=date_value or datetime.now(),
            format="DD-MM-YYYY",
        )
        st.session_state.folder_date = new_date.strftime("%d-%m-%Y")
    with col2:
        # Depot Name input
        new_depot = st.text_input(
            "Depot Name",
            value=st.session_state.get('depot_name', ""),
        )
        st.session_state.depot_name = new_depot
    with col3:
        # Coach Name input
        new_coach = st.text_input(
            "Coach Name",
            value=st.session_state.get('coach_name', ""),
        )
        st.session_state.coach_name = new_coach

    # Initialize visibility states
    if 'show_tables' not in st.session_state:
        st.session_state.show_tables = True
    if 'show_charts' not in st.session_state:
        st.session_state.show_charts = True

    # Add toggle buttons in a horizontal layout
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("Toggle Tables", help="Show/Hide all tables"):
            st.session_state.show_tables = not st.session_state.show_tables
    with col2:
        if st.button("Toggle Charts", help="Show/Hide all charts"):
            st.session_state.show_charts = not st.session_state.show_charts
    with col3:
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
                        fig = create_clubbed_horizontal_bar_chart(df, st.session_state.color_seed)
                        st.plotly_chart(fig, key=table_name)
    except AttributeError:
        st.warning("Please upload a folder first to analyze it.")


