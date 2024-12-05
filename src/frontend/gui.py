# src/frontend/streamlit_gui.py

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from backend.data_handler import DataHandler
import tempfile
import os
from pathlib import Path
from functools import lru_cache
from frontend.compute.visualizations import create_bar_chart, create_pie_chart, create_treemap, get_color
from frontend.utils.css_utils import inject_main_css, inject_column_css, get_metrics_css, inject_tab_css  # Import CSS utilities
from frontend.utils.sidebar_utils import show_help, show_credits  # Import sidebar utilities
from frontend.tabs.render_brakes_log import render_brakes_log;
from frontend.tabs.render_dump_log import render_dump_log;
from frontend.tabs.render_summary import render_summary;
from frontend.tabs.render_settings import render_settings  # Add this import
import glob
import tkinter as tk
from tkinter import filedialog
import re  # Import regex module

@lru_cache(maxsize=32)
def process_folder(folder_path: str):
    """Cache folder processing to avoid recomputing"""
    return DataHandler(folder_path)

def get_csv_files(folder_path: str) -> list:
    """Efficiently get CSV files using pathlib"""
    return [f for f in Path(folder_path).glob('*.csv')]

class StreamlitGUI:
    def __init__(self):
        self.init_page_config()
        self.init_session_state()
        # Use the get_color function from visualizations.py
        self.get_color = get_color
    
    def init_page_config(self):
        st.set_page_config(
            page_title="Error Analyzer",
            page_icon="📊",
            layout="wide"
        )
        # Inject CSS styles using the utility function
        inject_main_css()
        inject_tab_css()  # Inject tab CSS
    
    def init_session_state(self):
        # Existing state variables
        if 'data_handler' not in st.session_state:
            st.session_state.data_handler = None
        if 'selected_errors' not in st.session_state:
            st.session_state.selected_errors = set()
        if 'axes_swapped' not in st.session_state:
            st.session_state.axes_swapped = False
        if 'sort_by' not in st.session_state:
            st.session_state.sort_by = None
        if 'sort_ascending' not in st.session_state:
            st.session_state.sort_ascending = True
        # Add new state variable for annotation toggle
        if 'show_percentage' not in st.session_state:
            st.session_state.show_percentage = True  # Default to showing percentages
        if 'selected_tags' not in st.session_state:
            st.session_state.selected_tags = set()
        if 'error_view_mode' not in st.session_state:
            st.session_state.error_view_mode = "Individual Errors"
        if 'tab_badges' not in st.session_state:
            st.session_state.tab_badges = {
                'Brakes Log': {'count': 0, 'color': '#dc3545'},
                'Dump Log': {'count': 0, 'color': '#fd7e14'},
                'Summary': {'count': 0, 'color': '#198754'}
            }
        if 'folder_date' not in st.session_state:
            st.session_state.folder_date = None
        if 'depot_name' not in st.session_state:
            st.session_state.depot_name = None
        if 'coach_name' not in st.session_state:
            st.session_state.coach_name = None
    
    def render(self):
        # Create tabs for navigation
        # Update tabs to include Settings
        tabs = st.tabs(["Brakes Log", "Dump Log", "Summary", "Settings"])
        
        # Sidebar content
        with st.sidebar:
            st.header("Settings")

            # Function to open folder selection dialog
            def select_folder():
                root = tk.Tk()
                root.withdraw()  # Hide the main window
                root.attributes('-topmost', True)  # Bring the dialog to the front
                folder_selected = filedialog.askdirectory()
                root.destroy()
                return folder_selected

            # Replace file uploader with 'Upload Folder' button
            if st.button("Upload Folder"):
                folder_path = select_folder()
                if folder_path:
                    with st.spinner('Processing files...'):
                        csv_files = get_csv_files(folder_path)
                        if csv_files:
                            try:
                                # Parse folder name
                                folder_name = os.path.basename(folder_path)
                                match = re.match(r'(\d{2}-\d{2}-\d{4})_(.+)_(.+)', folder_name)
                                if match:
                                    st.session_state.folder_date = match.group(1)
                                    st.session_state.depot_name = match.group(2)
                                    st.session_state.coach_name = match.group(3)
                                    print(st.session_state.folder_date, "##",st.session_state.depot_name,"##", st.session_state.coach_name)
                                else:
                                    st.warning("Folder name does not match the expected pattern")

                                # Use cached processing
                                st.session_state.data_handler = process_folder(folder_path)
                                
                                if len(st.session_state.data_handler.ecl_freq_summary) == 0:
                                    st.error("No data found in the CSV files!")
                                else:
                                    st.success("Files processed successfully")
                                    with st.expander("Processed Files"):
                                        for file in csv_files:
                                            st.write(file.name)
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                        else:
                            st.error("No CSV files found in folder")
                else:
                    st.info("👆 Please select a folder")

            show_help()
            show_credits()
        
        # Render content based on active tab
        with tabs[0]:
            render_brakes_log()
        with tabs[1]:
            render_dump_log()
            pass
        with tabs[2]:
            render_summary()
            pass
        with tabs[3]:  # Add settings tab
            render_settings()

def main():
    gui = StreamlitGUI()
    gui.render()

if __name__ == "__main__":
    main()