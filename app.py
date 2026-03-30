import streamlit as st
import pandas as pd
import os
import plotly.express as px
from PIL import Image
import glob

# 1. UI CUSTOMIZATION (FIXED)
st.markdown("""
    <style>
    /* Dark Theme Professional Styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    .main {
        background-color: #0d1117;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #58a6ff;
    }
    div[data-testid="stMetricLabel"] {
        color: #8b949e;
    }
    .stSelectbox, .stSlider {
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Add a professional status badge to the sidebar
st.sidebar.success("● System Online: LILA BLACK Production")

# 1. PAGE CONFIG
st.set_page_config(layout="wide", page_title="LILA BLACK Analytics")
st.title("🎮 LILA BLACK: Player Journey Tool")

# 2. MAP SETTINGS (From your README)
MAP_CONFIGS = {
    "AmbroseValley": {"scale": 900, "origin_x": -370, "origin_z": -473, "img": "player_data/minimaps/AmbroseValley_Minimap.png"},
    "GrandRift": {"scale": 581, "origin_x": -290, "origin_z": -290, "img": "player_data/minimaps/GrandRift_Minimap.png"},
    "Lockdown": {"scale": 1000, "origin_x": -500, "origin_z": -500, "img": "player_data/minimaps/Lockdown_Minimap.jpg"}
}

# 3. DATA LOADING FUNCTION
@st.cache_data
def load_all_data():
    all_files = glob.glob("player_data/February_*/*")
    data_frames = []
    
    # Progress bar because 1,243 files take a second
    progress_bar = st.progress(0)
    for i, f in enumerate(all_files):
        try:
            df = pd.read_parquet(f)
            # Clean 'event' column from bytes to string
            df['event'] = df['event'].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
            # Add a 'is_bot' helper column based on ID type
            df['is_bot'] = df['user_id'].apply(lambda x: "Bot" if len(str(x)) < 10 else "Human")
            data_frames.append(df)
        except:
            continue
        if i % 100 == 0:
            progress_bar.progress(i / len(all_files))
    
    progress_bar.empty()
    return pd.concat(data_frames, ignore_index=True)

# LOAD THE DATA
try:
    with st.spinner("Loading production gameplay data..."):
        df = load_all_data()

    # 4. SIDEBAR FILTERS
    st.sidebar.header("Control Panel")
    selected_map = st.sidebar.selectbox("Select Map", list(MAP_CONFIGS.keys()))
    
    # Filter by map first
    map_df = df[df['map_id'] == selected_map]
    
    selected_match = st.sidebar.selectbox("Select Match ID", map_df['match_id'].unique())
    match_df = map_df[map_df['match_id'] == selected_match].sort_values('ts')

    # 5. COORDINATE CONVERSION (The Step 1 & 2 from your README)
    conf = MAP_CONFIGS[selected_map]
    
    # Convert World (x, z) -> Pixel (x, y)
    match_df['pixel_x'] = ((match_df['x'] - conf['origin_x']) / conf['scale']) * 1024
    match_df['u_v'] = (match_df['z'] - conf['origin_z']) / conf['scale']
    match_df['pixel_y'] = (1 - match_df['u_v']) * 1024

    # 6. VISUALIZATION CONTROLS
    st.subheader(f"Match Analysis: {selected_match}")
    
    viz_mode = st.radio("Visualization Mode", ["Player Journeys", "Death & Activity Heatmap"], horizontal=True)

    if viz_mode == "Player Journeys":
        # Timeline Slider
        time_step = st.select_slider("Match Timeline", options=match_df['ts'].unique())
        current_data = match_df[match_df['ts'] <= time_step]

        # Path Visualization
        fig = px.scatter(current_data, 
                         x='pixel_x', y='pixel_y', 
                         color='is_bot',
                         symbol='event',
                         hover_data=['user_id', 'event'],
                         color_discrete_map={"Human": "#00D4FF", "Bot": "#FF4B4B"})
        
        # Make the dots a bit bigger and easier to see
        fig.update_traces(marker=dict(size=8))
    
    else:
        # HEATMAP MODE: Fix the black box by making the heatmap transparent
        action_events = match_df[~match_df['event'].isin(['Position', 'BotPosition'])]
        
        if not action_events.empty:
            fig = px.density_heatmap(action_events, 
                                     x='pixel_x', y='pixel_y', 
                                     nbinsx=40, nbinsy=40,
                                     color_continuous_scale="Hot",
                                     range_color=[0, 3], # Adjust this if it's too dark
                                     title="High Activity / Combat Zones")
            
            # This is the magic line that fixes the black box:
            fig.update_layout(coloraxis_showscale=True, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            fig.update_traces(opacity=0.6) # Makes it see-through
        else:
            st.warning("No combat or loot events recorded in this match yet!")
            fig = px.scatter(x=[512], y=[512])

    # Add Map Background
    img = Image.open(conf['img'])
    fig.add_layout_image(
        dict(source=img, x=0, y=0, sizex=1024, sizey=1024, 
             xref="x", yref="y", sizing="stretch", layer="below")
    )

    # Clean up UI - FIXED: removed the problematic update_axes
    fig.update_xaxes(range=[0, 1024], visible=False, showgrid=False, zeroline=False)
    fig.update_yaxes(range=[1024, 0], visible=False, showgrid=False, zeroline=False) 
    fig.update_layout(width=800, height=800, margin=dict(l=0, r=0, t=40, b=0))

    st.plotly_chart(fig, use_container_width=True)

    # 7. QUICK STATS FOR LEVEL DESIGNERS
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Players", match_df['user_id'].nunique())
    col2.metric("Total Kills", len(match_df[match_df['event'].isin(['Kill', 'BotKill'])]))
    col3.metric("Loot Events", len(match_df[match_df['event'] == 'Loot']))

except Exception as e:
    st.error(f"Error: {e}")
    st.info("Check if your folder paths match the screenshot!")