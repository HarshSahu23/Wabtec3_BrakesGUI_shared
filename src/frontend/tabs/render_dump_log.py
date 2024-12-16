import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from frontend.utils.render_section_header import render_section_header
from frontend.utils.wsp_activity_log.summary import summary
from frontend.utils.wsp_activity_log.detailed_analysis import detailed_analysis

def render_dump_log():
    render_section_header(
        "Dump Log Analysis",
        "Review and analyze system dump logs for critical events and patterns.",
        "📊"
    )
    
    if not st.session_state.data_handler or st.session_state.data_handler.dmp.empty:
        st.warning("Please upload DMP log files to begin analysis")
        return

    summary()

    st.subheader("FILL ↔ VENT Analysis",divider="gray")
    # FILL/VENT Analysis begin
    fill_vent_events = st.session_state.data_handler.fill_vent_events

    if not fill_vent_events:
        st.warning("No FILL/VENT events to display.")
    else:
        # Prepare data for combo table
        fill_vent_data = {}
        empty_events = []
        max_length = 0
        for i in range(1, 5):
            key = f'FILL_{i}_VENT_{i}'
            events = fill_vent_events.get(key, [])
            if not events:
                empty_events.append(key)
                continue
            fill_instances = [j + 1 for j in range(len(events))]
            vent_counts = [event['vent_transition_count'] for event in events]
            fill_vent_data[f'FILL_{i} (instance)'] = fill_instances
            fill_vent_data[f'VENT_{i} (count)'] = vent_counts
            if len(events) > max_length:
                max_length = len(events)
        if fill_vent_data:
            # Pad shorter lists with empty strings
            for key in fill_vent_data:
                fill_vent_data[key] += [''] * (max_length - len(fill_vent_data[key]))
            # Create DataFrame
            table_df = pd.DataFrame(fill_vent_data)
            # Display table and empty events side by side
            col1, col2 = st.columns([3, 1])
            with col1:
                st.table(table_df.style.set_properties(**{'text-align': 'center'}).set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}]))
            with col2:
                if empty_events:
                    st.markdown("#### Empty FILL/VENT Events")
                    st.markdown(
                        '<ul style="list-style-type:none; padding-left: 0;">' +
                        ''.join([
                            f'<li style="margin-bottom: 10px; padding: 10px; background-color: #f8f9fa; text-align: center; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">{event}</li>'
                            for event in empty_events
                        ]) +
                        '</ul>',
                        unsafe_allow_html=True
                    )
        else:
            st.warning("No FILL/VENT events with data to display.")
    # FILL/VENT Analysis end
    
    st.subheader("FILL ↔ VENT Charts", divider="gray")
    # FILL/VENT Charts begin
    fill_vent_events = st.session_state.data_handler.fill_vent_events

    charts = []
    for i in range(1, 5):
        key = f'FILL_{i}_VENT_{i}'
        events = fill_vent_events.get(key, [])
        if not events:
            continue
        vent_counts = [event['vent_transition_count'] for event in events]
        fill_instances = [j + 1 for j in range(len(events))]

        df = pd.DataFrame({
            'Fill Instance': fill_instances,
            'Vent Count': vent_counts
        })

        # Define color gradient from green to red (pastel colors)
        max_count = max(vent_counts) if vent_counts else 1
        min_count = min(vent_counts) if vent_counts else 0
        colors = ['#8FBC8F', '#F0E68C', '#FA8072']  # Pastel green to red
        color_scale = [
            colors[int((vc - min_count) / (max_count - min_count) * (len(colors) - 1)) if max_count > min_count else 0]
            for vc in vent_counts
        ]

        fig = go.Figure(go.Bar(
            x=vent_counts,
            y=fill_instances,
            orientation='h',
            text=vent_counts,
            textposition='inside',
            marker=dict(color=color_scale),
            hovertemplate='Fill Instance: %{y}<br>Vent Count: %{x}<extra></extra>'
        ))
        fig.update_layout(
            title=f'{key}',
            xaxis_title='Vent Count',
            yaxis_title='Fill Instance',
            yaxis=dict(autorange='reversed'),
            height=300,
            margin=dict(l=50, r=50, t=50, b=50),
        )
        charts.append(fig)

    if charts:
        cols = st.columns(2)
        for idx, fig in enumerate(charts):
            with cols[idx % 2]:
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No FILL/VENT charts to display.")
    # FILL/VENT Charts end
    
    st.subheader("FILL ↔ VENT Time Series", divider="gray")
    # Time series visualization
    fill_vent_events = st.session_state.data_handler.fill_vent_events
    
    # Prepare data for time series
    time_series_data = []
    
    if fill_vent_events:
        # Process each FILL/VENT pair
        for i in range(1, 5):
            key = f'FILL_{i}_VENT_{i}'
            events = fill_vent_events.get(key, [])
            if not events:
                continue
                
            # Calculate timeline positions with duration scaling
            timeline_pos = 0
            time_positions = []
            event_durations = []
            vent_counts = []
            
            # Duration scaling factor (adjust as needed)
            DURATION_SCALE = 2.0
            
            # Process each event
            for event in events:
                duration = event['end_time'] - event['start_time']
                scaled_duration = duration * DURATION_SCALE
                
                time_positions.append(timeline_pos)
                event_durations.append(scaled_duration)
                vent_counts.append(event['vent_transition_count'])
                
                # Increment timeline position by base spacing + scaled duration
                timeline_pos += 1 + scaled_duration
            
            # Create color gradient based on event sequence
            num_points = len(events)
            colors = [
                f'rgb({int(255*idx/(num_points-1))}, 0, {int(255*(1-idx/(num_points-1)))})'
                for idx in range(num_points)
            ] if num_points > 1 else ['rgb(0, 0, 255)']
            
            fig_series = go.Scatter(
                x=time_positions,
                y=vent_counts,
                mode='lines+markers',
                name=key,
                line=dict(shape='spline', smoothing=1.3, width=2),
                marker=dict(
                    size=10,
                    color=colors,
                    line=dict(width=1, color='white')
                ),
                hovertemplate=(
                    'Event Duration: %{text:.2f}s<br>' +
                    'Vent Count: %{y}<extra></extra>'
                ),
                text=event_durations  # Add duration to hover text
            )
            time_series_data.append(fig_series)
        
        if time_series_data:
            fig = go.Figure(data=time_series_data)
            fig.update_layout(
                title='FILL/VENT Events Timeline (Event-spaced)',
                xaxis_title='Event Sequence (with scaled durations)',
                yaxis_title='Vent Transition Count',
                height=400,
                showlegend=True,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No time series data to display.")
    
    st.subheader("FILL ↔ VENT Time Series", divider="gray")
    # FILL/VENT Time series begin
    
    # Add additional analysis options
    with st.expander("Advanced Analysis Options"):
        # Filtered Data Table Section
        detailed_analysis()