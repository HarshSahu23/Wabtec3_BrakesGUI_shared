import random
import plotly.graph_objects as go
import plotly.express as px
from functools import lru_cache
from datetime import datetime
import streamlit as st
from PIL import Image

# Extended color palette
base_colors = (
    px.colors.qualitative.Set3 +
    px.colors.qualitative.Pastel1 +
    px.colors.qualitative.Set1 +
    px.colors.qualitative.Pastel2 +
    px.colors.qualitative.Set2
)
logo_path = "wabtec-logo-red.png"
wabtec_logo = Image.open(logo_path)

def annotate_folder_stats(fig):
    # Moved from the function that draws charts to this one
    # Add logo in the top right corner
    fig.add_layout_image(
        dict(
            source=wabtec_logo,
            xref="paper",
            yref="paper",
            x=0,
            y=1.2,
            sizex=0.12,
            sizey=0.1,
            xanchor="left",
            yanchor="top",
            layer="above"
        )
    )    

    annotations = [
        {"label": "Depot Name:", "value": st.session_state.depot_name},
        {"label": "Coach Num:", "value": st.session_state.coach_name},
        {"label": "Analysis Time:", "value":  datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}
    ]
        
    num_annotations = len(annotations)
    spacing = 1 / num_annotations
    
    for i, anno in enumerate(annotations, start=1):
        x_pos = spacing * i
        fig.add_annotation(
            x=x_pos - spacing / 2,
            y=1.03,
            xref='paper',
            yref='paper',
            text=anno["label"],
            showarrow=False,
            xanchor='right',
            yanchor='bottom',
            font=dict(size=14, color='grey'),
        )
        fig.add_annotation(
            x=x_pos - spacing / 2 + spacing / 100,
            y=1.03,
            xref='paper',
            yref='paper',
            text=anno["value"],
            showarrow=False,
            xanchor='left',
            yanchor='bottom',
            font=dict(size=14, color='indigo'),
        )

def get_color(i):
    """Generate a repeating color from the base palette."""
    return base_colors[i % len(base_colors)]

@lru_cache(maxsize=128)
def calculate_percentages(total, frequencies):
    """Cache percentage calculations for better performance."""
    return [(freq / total) * 100 for freq in frequencies]

def create_bar_chart(filtered_data, get_color_func, session_state):
    """Create an interactive bar chart using Plotly"""
    # Generate colors for each bar
    colors = [get_color_func(i) for i in range(len(filtered_data))]
    
    fig = go.Figure()
    
    # Calculate total for percentages
    total = filtered_data['Frequency'].sum()
    frequencies = filtered_data['Frequency'].tolist()
    
    # Get cached percentages
    percentages = calculate_percentages(total, tuple(frequencies))
    
    if session_state.axes_swapped:
        fig.add_trace(go.Bar(
            y=filtered_data['Description'],
            x=filtered_data['Frequency'],
            orientation='h',
            marker_color=colors,
            hovertemplate='<b>Error:</b> %{y}<br>' +
                         '<b>Frequency:</b> %{x}<br>' +
                         '<extra></extra>'
        ))
        
        # Add annotations based on user preference
        for i, (value, percentage) in enumerate(zip(frequencies, percentages)):
            annotation_text = f'{percentage:.1f}%' if session_state.show_percentage else f'{value:,}'
            fig.add_annotation(
                y=i,
                x=value,
                text=annotation_text,
                showarrow=False,
                xshift=10
            )
    else:
        fig.add_trace(go.Bar(
            x=filtered_data['Description'],
            y=filtered_data['Frequency'],
            marker_color=colors,
            hovertemplate='<b>Error:</b> %{x}<br>' +
                         '<b>Frequency:</b> %{y}<br>' +
                         '<extra></extra>'
        ))
        
        # Add annotations based on user preference
        for i, (value, percentage) in enumerate(zip(frequencies, percentages)):
            annotation_text = f'{percentage:.1f}%' if session_state.show_percentage else f'{value:,}'
            fig.add_annotation(
                x=i,
                y=value,
                text=annotation_text,
                showarrow=False,
                yshift=10
            )
    
    fig.update_layout(
        title={
            'text': 'Error Frequency Distribution',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Frequency' if session_state.axes_swapped else 'Error Description',
        yaxis_title='Error Description' if session_state.axes_swapped else 'Frequency',
        showlegend=False,
        xaxis_tickangle=-45 if not session_state.axes_swapped else 0,
        margin=dict(t=110, l=50 if not session_state.axes_swapped else 200, r=50, b=100),
        height=600,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        bargap=0.2,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    annotate_folder_stats(fig)

    # Add grid lines for better readability
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    
    return fig

def create_pie_chart(filtered_data, get_color_func):
    """Create an interactive pie chart using Plotly"""
    
    # Generate colors for each slice
    colors = [get_color_func(i) for i in range(len(filtered_data))]
    
    fig = go.Figure()
    
    fig.add_trace(go.Pie(
        labels=filtered_data['Description'],
        values=filtered_data['Frequency'],
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>Error:</b> %{label}<br>' +
                     '<b>Frequency:</b> %{value}<br>' +
                     '<b>Percentage:</b> %{percent}<br>' +
                     '<extra></extra>',
        marker=dict(colors=colors)
    ))
    
    fig.update_layout(
        title={
            'text': 'Error Distribution by Percentage',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        height=600,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.0
        ),
        margin=dict(t=110, l=50, r=50, b=50),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    annotate_folder_stats(fig)
    
    return fig

def create_treemap(filtered_data):
    """Create an interactive treemap using Plotly"""
    
    # For treemap, we'll use a continuous color scale instead of discrete colors
    fig = px.treemap(
        filtered_data,
        path=['Description'],
        values='Frequency',
        color='Frequency',
        color_continuous_scale=px.colors.sequential.Viridis,  # Changed to Viridis for better distinction
        title='Error Distribution Treemap',
    )
    fig.update_layout(
        title={
            'text': 'Error Distribution Treemap',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )
    
    fig.update_layout(
        height=600,
        margin=dict(t=110, l=25, r=25, b=25),
    )

    annotate_folder_stats(fig)
    
    return fig

random_offset = random.randint(1, 100)


# function moved to summary_viz.py