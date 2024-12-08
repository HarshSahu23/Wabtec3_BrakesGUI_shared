import streamlit as st
from datetime import datetime

def render_folder_name_settings():
    """Render the folder name configuration section"""
    # st.subheader("Folder Name Configuration")
    
    # Create a container for the current config display
    config_container = st.empty()
    
    # Function to update the current config display
    def update_config_display():
        current_config = "Current Configuration: "
        if all([st.session_state.folder_date, st.session_state.depot_name, st.session_state.coach_name]):
            current_config += f"{st.session_state.folder_date}_{st.session_state.depot_name}_{st.session_state.coach_name}"
        else:
            current_config += "Not configured"
        config_container.info(current_config)
    
    # Show initial config
    update_config_display()

    # Date input
    date_value = None
    if st.session_state.folder_date:
        try:
            date_value = datetime.strptime(st.session_state.folder_date, "%d-%m-%Y")
        except:
            pass
            
    new_date = st.date_input(
        "Date",
        value=date_value,
        format="DD-MM-YYYY",
        
    )

    # Depot name input
    new_depot = st.text_input(
        "Depot Name",
        value=st.session_state.depot_name if st.session_state.depot_name else "",
    )

    # Coach name input
    new_coach = st.text_input(
        "Coach Name",
        value=st.session_state.coach_name if st.session_state.coach_name else "",
    )

    if st.button("Update Folder Configuration"):
        st.session_state.folder_date = new_date.strftime("%d-%m-%Y")
        st.session_state.depot_name = new_depot
        st.session_state.coach_name = new_coach
        update_config_display()  # Update the display immediately
        # st.experimental_rerun()  # Force a rerun to refresh the display

def render_settings():
    """Main settings panel render function"""
    st.title("Settings")
    
    # Section for folder name configuration
    with st.expander("### Folder Name Configuration", expanded=True):
        render_folder_name_settings()
    
    # Add more settings sections here as needed
