import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Configure page
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for ultra-modern shiny yellow and black theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700;800&display=swap');
    
    /* Main theme colors */
    :root {
        --primary-yellow: #FFD700;
        --secondary-yellow: #FFF700;
        --neon-yellow: #FFFF00;
        --dark-black: #0A0A0A;
        --medium-black: #1A1A1A;
        --light-black: #2A2A2A;
        --text-white: #FFFFFF;
        --accent-gray: #404040;
        --glow-yellow: rgba(255, 215, 0, 0.6);
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Global font styling */
    html, body, [class*="css"] {
        font-family: 'Exo 2', sans-serif !important;
    }
    
    /* Main app background with animated gradient */
    .stApp {
        background: linear-gradient(45deg, #0A0A0A, #1A1A1A, #0A0A0A);
        background-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Main container styling with enhanced glow */
    .main .block-container {
        padding: 2rem 1rem;
        background: linear-gradient(135deg, rgba(26, 26, 26, 0.95) 0%, rgba(42, 42, 42, 0.95) 100%);
        border-radius: 20px;
        margin: 1rem;
        box-shadow: 
            0 0 30px rgba(255, 215, 0, 0.3),
            0 0 60px rgba(255, 215, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 215, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar styling with neon glow */
    .css-1d391kg, .css-1cypcdb, .css-17eq0hr {
        background: linear-gradient(180deg, rgba(10, 10, 10, 0.98) 0%, rgba(26, 26, 26, 0.98) 100%) !important;
        border-right: 3px solid #FFD700 !important;
        box-shadow: 
            3px 0 20px rgba(255, 215, 0, 0.4),
            inset -1px 0 0 rgba(255, 215, 0, 0.2) !important;
        backdrop-filter: blur(15px) !important;
    }
    
    /* Enhanced title styling with glow animation */
    .main-title {
        font-family: 'Orbitron', monospace !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #FFD700, #FFF700, #FFFF00, #FFD700) !important;
        background-size: 300% 300% !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        text-align: center !important;
        margin: 2rem 0 !important;
        animation: titleGlow 3s ease-in-out infinite alternate, textShine 4s linear infinite !important;
        filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.8)) !important;
        letter-spacing: 2px !important;
    }
    
    @keyframes titleGlow {
        0% { filter: drop-shadow(0 0 20px rgba(255, 215, 0, 0.8)); }
        100% { filter: drop-shadow(0 0 40px rgba(255, 215, 0, 1)); }
    }
    
    @keyframes textShine {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
    
    /* Sidebar title with pulsing glow */
    .sidebar-title {
        font-family: 'Orbitron', monospace !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        color: #FFD700 !important;
        text-align: center !important;
        margin-bottom: 1.5rem !important;
        padding: 1.2rem !important;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 247, 0, 0.1)) !important;
        border-radius: 15px !important;
        border: 2px solid #FFD700 !important;
        box-shadow: 
            0 0 20px rgba(255, 215, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        animation: pulse 2s ease-in-out infinite alternate !important;
        letter-spacing: 1px !important;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1); }
        100% { box-shadow: 0 0 30px rgba(255, 215, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.2); }
    }
    
    /* Enhanced metric cards with 3D effect */
    .metric-card {
        background: linear-gradient(135deg, rgba(42, 42, 42, 0.9) 0%, rgba(64, 64, 64, 0.9) 100%) !important;
        padding: 2rem 1.5rem !important;
        border-radius: 20px !important;
        border: 2px solid transparent !important;
        background-clip: padding-box !important;
        text-align: center !important;
        margin: 0.8rem !important;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.5),
            0 0 20px rgba(255, 215, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.6),
            0 0 40px rgba(255, 215, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        border: 2px solid rgba(255, 215, 0, 0.6) !important;
    }
    
    .metric-title {
        color: #FFD700 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-family: 'Exo 2', sans-serif !important;
    }
    
    .metric-value {
        color: #FFFFFF !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        font-family: 'Orbitron', monospace !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.6) !important;
        letter-spacing: 2px !important;
    }
    
    /* Enhanced section headers with animated underline */
    .section-header {
        font-family: 'Orbitron', monospace !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #FFD700 !important;
        text-align: center !important;
        margin: 3rem 0 2rem 0 !important;
        padding: 1.5rem !important;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 247, 0, 0.1)) !important;
        border-radius: 15px !important;
        border-left: 5px solid #FFD700 !important;
        box-shadow: 
            0 5px 20px rgba(255, 215, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #FFD700, #FFF700, #FFD700);
        animation: slideIn 2s ease-in-out infinite;
    }
    
    @keyframes slideIn {
        0%, 100% { transform: translateX(-100%); }
        50% { transform: translateX(0); }
    }
    
    /* Enhanced chart containers with glass effect */
    .chart-container {
        background: linear-gradient(135deg, rgba(42, 42, 42, 0.8), rgba(26, 26, 26, 0.9)) !important;
        padding: 2rem !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        margin: 1.5rem 0 !important;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(255, 215, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .chart-container:hover {
        box-shadow: 
            0 15px 40px rgba(0, 0, 0, 0.5),
            0 0 30px rgba(255, 215, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Enhanced button styling with glow effect */
    .stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFF700, #FFD700) !important;
        background-size: 200% 200% !important;
        color: #1A1A1A !important;
        font-weight: 800 !important;
        font-family: 'Exo 2', sans-serif !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 1rem 2.5rem !important;
        font-size: 1.2rem !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 
            0 8px 25px rgba(255, 215, 0, 0.4),
            0 0 20px rgba(255, 215, 0, 0.2) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        animation: buttonGlow 3s ease-in-out infinite alternate !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    @keyframes buttonGlow {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05) !important;
        box-shadow: 
            0 15px 35px rgba(255, 215, 0, 0.6),
            0 0 40px rgba(255, 215, 0, 0.4) !important;
        background: linear-gradient(45deg, #FFF700, #FFFF00, #FFF700) !important;
    }
    
    /* Enhanced file uploader */
    .stFileUploader > div > div {
        background: linear-gradient(135deg, rgba(42, 42, 42, 0.8), rgba(26, 26, 26, 0.9)) !important;
        border: 2px dashed #FFD700 !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: #FFF700 !important;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.3) !important;
    }
    
    /* Enhanced selectbox */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, rgba(42, 42, 42, 0.9), rgba(26, 26, 26, 0.9)) !important;
        border: 2px solid rgba(255, 215, 0, 0.5) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Enhanced dataframe styling */
    .dataframe {
        background: linear-gradient(135deg, rgba(42, 42, 42, 0.95), rgba(26, 26, 26, 0.95)) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Enhanced success message */
    .success-message {
        background: linear-gradient(45deg, #FFD700, #FFF700) !important;
        color: #1A1A1A !important;
        padding: 1.2rem !important;
        border-radius: 15px !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin: 1rem 0 !important;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4) !important;
        animation: successPulse 2s ease-in-out infinite alternate !important;
        font-family: 'Exo 2', sans-serif !important;
        letter-spacing: 1px !important;
    }
    
    @keyframes successPulse {
        0% { box-shadow: 0 5px 20px rgba(255, 215, 0, 0.4); }
        100% { box-shadow: 0 8px 30px rgba(255, 215, 0, 0.6); }
    }
    
    /* Enhanced alert styling */
    .stAlert {
        background: rgba(255, 215, 0, 0.15) !important;
        border: 1px solid rgba(255, 215, 0, 0.5) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Custom subtitle styling */
    .custom-subtitle {
        font-family: 'Exo 2', sans-serif !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: #FFD700 !important;
        text-align: center !important;
        margin: 1rem 0 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
    }
    
    /* Welcome section styling */
    .welcome-section {
        text-align: center !important;
        padding: 3rem !important;
        background: linear-gradient(135deg, rgba(42, 42, 42, 0.9), rgba(26, 26, 26, 0.95)) !important;
        border-radius: 20px !important;
        border: 2px solid rgba(255, 215, 0, 0.3) !important;
        margin: 2rem 0 !important;
        box-shadow: 
            0 15px 40px rgba(0, 0, 0, 0.4),
            0 0 30px rgba(255, 215, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px) !important;
    }
    
    .welcome-title {
        color: #FFD700 !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.6) !important;
        letter-spacing: 2px !important;
    }
    
    .welcome-text {
        color: #FFFFFF !important;
        font-family: 'Exo 2', sans-serif !important;
        font-size: 1.3rem !important;
        margin-bottom: 1.5rem !important;
        line-height: 1.6 !important;
    }
    
    .instructions-box {
        background: rgba(255, 215, 0, 0.1) !important;
        padding: 2rem !important;
        border-radius: 15px !important;
        margin: 1.5rem 0 !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
    }
    
    .instructions-title {
        color: #FFD700 !important;
        font-family: 'Exo 2', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        letter-spacing: 1px !important;
    }
    
    .instructions-list {
        color: #FFFFFF !important;
        font-family: 'Exo 2', sans-serif !important;
        text-align: left !important;
        max-width: 600px !important;
        margin: 0 auto !important;
        line-height: 1.8 !important;
        font-size: 1.1rem !important;
    }
    
    .welcome-footer {
        color: #FFF700 !important;
        font-family: 'Exo 2', sans-serif !important;
        font-style: italic !important;
        font-size: 1.2rem !important;
        margin-top: 1.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Main title with modern styling
st.markdown('<h1 class="main-title">💬 WhatsApp Chat Analyzer</h1>', unsafe_allow_html=True)

# Sidebar with modern styling
st.sidebar.markdown('<div class="sidebar-title">🔧 Analysis Controls</div>', unsafe_allow_html=True)

# File uploader with custom styling
uploaded_file = st.sidebar.file_uploader("📁 Upload WhatsApp Chat Export", type=['txt'])

if uploaded_file is not None:
    try:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        df = preprocessor.preprocess(data)
        
        # Success message
        st.sidebar.markdown('<div class="success-message">✅ File uploaded successfully!</div>', unsafe_allow_html=True)
        
        # Fetch unique users
        user_list = df['user'].unique().tolist()

        # Safely remove 'group_notification' if it exists
        if 'group_notification' in user_list:
            user_list.remove('group_notification')

        user_list.sort()
        user_list.insert(0, "Overall")

        selected_user = st.sidebar.selectbox("👤 Select User for Analysis", user_list)
        
        # Add some spacing
        st.sidebar.markdown("<br>", unsafe_allow_html=True)

        if st.sidebar.button("🚀 Generate Analysis"):
            # Add loading animation
            with st.spinner('🔄 Analyzing your chat data...'):
                import time
                time.sleep(1)  # Brief pause for better UX
            # Stats Area with modern cards
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
            
            st.markdown('<div class="section-header">📊 Key Statistics</div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-title">💬 Total Messages</div>
                    <div class="metric-value">{num_messages:,}</div>
                </div>
                ''', unsafe_allow_html=True)
                
            with col2:
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-title">📝 Total Words</div>
                    <div class="metric-value">{words:,}</div>
                </div>
                ''', unsafe_allow_html=True)
                
            with col3:
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-title">📷 Media Shared</div>
                    <div class="metric-value">{num_media_messages:,}</div>
                </div>
                ''', unsafe_allow_html=True)
                
            with col4:
                st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-title">🔗 Links Shared</div>
                    <div class="metric-value">{num_links:,}</div>
                </div>
                ''', unsafe_allow_html=True)

            # Add section divider
            st.markdown('<hr style="border: 1px solid rgba(255, 215, 0, 0.3); margin: 3rem 0;">', unsafe_allow_html=True)

            # Monthly timeline with modern styling
            st.markdown('<div class="section-header">📈 Monthly Timeline</div>', unsafe_allow_html=True)
            timeline = helper.monthly_timeline(selected_user, df)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            fig.patch.set_facecolor('#1E1E1E')
            ax.set_facecolor('#2D2D2D')
            ax.plot(timeline['time'], timeline['message'], color='#FFD700', linewidth=3, marker='o', markersize=6)
            ax.set_xlabel('Time Period', color='#FFFFFF', fontsize=12)
            ax.set_ylabel('Number of Messages', color='#FFFFFF', fontsize=12)
            ax.tick_params(colors='#FFFFFF', rotation=45)
            ax.grid(True, alpha=0.3, color='#FFD700')
            plt.tight_layout()
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

            # Daily timeline with modern styling
            st.markdown('<div class="section-header">📅 Daily Timeline</div>', unsafe_allow_html=True)
            daily_timeline = helper.daily_timeline(selected_user, df)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            fig.patch.set_facecolor('#1E1E1E')
            ax.set_facecolor('#2D2D2D')
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='#FFF700', linewidth=2, alpha=0.8)
            ax.set_xlabel('Date', color='#FFFFFF', fontsize=12)
            ax.set_ylabel('Number of Messages', color='#FFFFFF', fontsize=12)
            ax.tick_params(colors='#FFFFFF', rotation=45)
            ax.grid(True, alpha=0.3, color='#FFD700')
            plt.tight_layout()
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

            # Add section divider
            st.markdown('<hr style="border: 1px solid rgba(255, 215, 0, 0.3); margin: 3rem 0;">', unsafe_allow_html=True)

            # Activity map with modern styling
            st.markdown('<div class="section-header">🗓️ Activity Patterns</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<h3 class="custom-subtitle">📊 Most Busy Days</h3>', unsafe_allow_html=True)
                busy_day = helper.week_activity_map(selected_user, df)
                
                fig, ax = plt.subplots(figsize=(8, 6))
                fig.patch.set_facecolor('#1E1E1E')
                ax.set_facecolor('#2D2D2D')
                bars = ax.bar(busy_day.index, busy_day.values, color='#FFD700', alpha=0.8, edgecolor='#FFF700', linewidth=2)
                ax.set_xlabel('Day of Week', color='#FFFFFF', fontsize=12)
                ax.set_ylabel('Number of Messages', color='#FFFFFF', fontsize=12)
                ax.tick_params(colors='#FFFFFF', rotation=45)
                ax.grid(True, alpha=0.3, color='#FFD700', axis='y')
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                           f'{int(height)}', ha='center', va='bottom', color='#FFFFFF', fontweight='bold')
                
                plt.tight_layout()
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<h3 class="custom-subtitle">📅 Most Busy Months</h3>', unsafe_allow_html=True)
                busy_month = helper.month_activity_map(selected_user, df)
                
                fig, ax = plt.subplots(figsize=(8, 6))
                fig.patch.set_facecolor('#1E1E1E')
                ax.set_facecolor('#2D2D2D')
                bars = ax.bar(busy_month.index, busy_month.values, color='#FFF700', alpha=0.8, edgecolor='#FFD700', linewidth=2)
                ax.set_xlabel('Month', color='#FFFFFF', fontsize=12)
                ax.set_ylabel('Number of Messages', color='#FFFFFF', fontsize=12)
                ax.tick_params(colors='#FFFFFF', rotation=45)
                ax.grid(True, alpha=0.3, color='#FFD700', axis='y')
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                           f'{int(height)}', ha='center', va='bottom', color='#FFFFFF', fontweight='bold')
                
                plt.tight_layout()
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)

            # Weekly Activity Heatmap
            st.markdown('<div class="section-header">🔥 Weekly Activity Heatmap</div>', unsafe_allow_html=True)
            user_heatmap = helper.activity_heatmap(selected_user, df)
            
            fig, ax = plt.subplots(figsize=(12, 8))
            fig.patch.set_facecolor('#1E1E1E')
            ax.set_facecolor('#2D2D2D')
            
            # Custom colormap for yellow-black theme
            colors = ['#1E1E1E', '#2D2D2D', '#404040', '#FFD700', '#FFF700']
            n_bins = 100
            cmap = plt.cm.colors.LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
            
            sns.heatmap(user_heatmap, cmap=cmap, annot=True, fmt='.0f', 
                       cbar_kws={'label': 'Message Count'}, ax=ax,
                       linewidths=0.5, linecolor='#FFD700')
            ax.set_xlabel('Time Period', color='#FFFFFF', fontsize=12)
            ax.set_ylabel('Day of Week', color='#FFFFFF', fontsize=12)
            ax.tick_params(colors='#FFFFFF')
            
            # Style the colorbar
            cbar = ax.collections[0].colorbar
            cbar.ax.yaxis.set_tick_params(color='#FFFFFF')
            cbar.ax.yaxis.label.set_color('#FFFFFF')
            
            plt.tight_layout()
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

            # Finding the busiest users in the group (Group level)
            if selected_user == 'Overall':
                st.markdown('<div class="section-header">👥 Most Active Users</div>', unsafe_allow_html=True)
                x, new_df = helper.most_busy_users(df)
                
                col1, col2 = st.columns(2)

                with col1:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    fig.patch.set_facecolor('#1E1E1E')
                    ax.set_facecolor('#2D2D2D')
                    bars = ax.bar(x.index, x.values, color='#FFD700', alpha=0.8, edgecolor='#FFF700', linewidth=2)
                    ax.set_xlabel('Users', color='#FFFFFF', fontsize=12)
                    ax.set_ylabel('Number of Messages', color='#FFFFFF', fontsize=12)
                    ax.tick_params(colors='#FFFFFF', rotation=45)
                    ax.grid(True, alpha=0.3, color='#FFD700', axis='y')
                    
                    # Add value labels on bars
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                               f'{int(height)}', ha='center', va='bottom', color='#FFFFFF', fontweight='bold')
                    
                    plt.tight_layout()
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with col2:
                    st.markdown('<h3 class="custom-subtitle">📊 User Statistics</h3>', unsafe_allow_html=True)
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.dataframe(new_df, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            # Add section divider
            st.markdown('<hr style="border: 1px solid rgba(255, 215, 0, 0.3); margin: 3rem 0;">', unsafe_allow_html=True)

            # WordCloud with modern styling
            st.markdown('<div class="section-header">☁️ Word Cloud</div>', unsafe_allow_html=True)
            df_wc = helper.create_wordcloud(selected_user, df)
            
            if df_wc is not None:
                fig, ax = plt.subplots(figsize=(12, 8))
                fig.patch.set_facecolor('#1E1E1E')
                ax.set_facecolor('#1E1E1E')
                ax.imshow(df_wc, interpolation='bilinear')
                ax.axis('off')
                plt.tight_layout()
                
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="chart-container"><p style="color: #FFD700; text-align: center; font-size: 1.2rem;">No valid words found for word cloud generation.</p></div>', unsafe_allow_html=True)

            # Most common words with modern styling
            st.markdown('<div class="section-header">🔤 Most Common Words</div>', unsafe_allow_html=True)
            most_common_df = helper.most_common_words(selected_user, df)

            if not most_common_df.empty:
                fig, ax = plt.subplots(figsize=(10, 8))
                fig.patch.set_facecolor('#1E1E1E')
                ax.set_facecolor('#2D2D2D')
                
                bars = ax.barh(most_common_df[0], most_common_df[1], color='#FFD700', alpha=0.8, edgecolor='#FFF700', linewidth=1)
                ax.set_xlabel('Frequency', color='#FFFFFF', fontsize=12)
                ax.set_ylabel('Words', color='#FFFFFF', fontsize=12)
                ax.tick_params(colors='#FFFFFF')
                ax.grid(True, alpha=0.3, color='#FFD700', axis='x')
                
                # Add value labels on bars
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2.,
                           f'{int(width)}', ha='left', va='center', color='#FFFFFF', fontweight='bold')
                
                plt.tight_layout()
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.pyplot(fig)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="chart-container"><p style="color: #FFD700; text-align: center; font-size: 1.2rem;">No common words found.</p></div>', unsafe_allow_html=True)

            # Emoji analysis with modern styling
            st.markdown('<div class="section-header">😊 Emoji Analysis</div>', unsafe_allow_html=True)
            emoji_df = helper.emoji_helper(selected_user, df)

            # Check if emoji_df is empty
            if not emoji_df.empty and emoji_df.shape[0] > 0:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown('<h3 class="custom-subtitle">📊 Emoji Statistics</h3>', unsafe_allow_html=True)
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.dataframe(emoji_df.head(10), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with col2:
                    st.markdown('<h3 class="custom-subtitle">🥧 Top Emojis Distribution</h3>', unsafe_allow_html=True)
                    
                    fig, ax = plt.subplots(figsize=(8, 8))
                    fig.patch.set_facecolor('#1E1E1E')
                    ax.set_facecolor('#2D2D2D')
                    
                    # Custom colors for pie chart
                    colors = ['#FFD700', '#FFF700', '#FFED4E', '#FFF176', '#FFEB3B', '#F9A825', '#F57F17', '#FF8F00', '#FF6F00', '#E65100']
                    
                    wedges, texts, autotexts = ax.pie(emoji_df[1].head(10), labels=emoji_df[0].head(10), 
                                                     autopct="%0.1f%%", colors=colors, 
                                                     textprops={'color': '#FFFFFF', 'fontsize': 10, 'fontweight': 'bold'},
                                                     startangle=90, explode=[0.05]*min(10, len(emoji_df)))
                    
                    # Style the percentage text
                    for autotext in autotexts:
                        autotext.set_color('#1E1E1E')
                        autotext.set_fontweight('bold')
                    
                    plt.tight_layout()
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.pyplot(fig)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="chart-container"><p style="color: #FFD700; text-align: center; font-size: 1.2rem;">😔 No emojis found in the chat.</p></div>', unsafe_allow_html=True)
                
    except Exception as e:
        st.sidebar.error(f"❌ Error processing file: {str(e)}")
        st.error("Please make sure you've uploaded a valid WhatsApp chat export file.")
        
else:
    # Welcome message when no file is uploaded
    st.markdown("""
    <div class="welcome-section">
        <h2 class="welcome-title">🚀 Welcome to WhatsApp Chat Analyzer!</h2>
        <p class="welcome-text">
            Upload your WhatsApp chat export file to get started with comprehensive analysis.
        </p>
        <div class="instructions-box">
            <h3 class="instructions-title">📋 How to Export WhatsApp Chat:</h3>
            <ol class="instructions-list">
                <li>Open WhatsApp and go to the chat you want to analyze</li>
                <li>Tap on the chat name at the top</li>
                <li>Scroll down and tap "Export Chat"</li>
                <li>Choose "Without Media" for faster processing</li>
                <li>Save the .txt file and upload it here</li>
            </ol>
        </div>
        <p class="welcome-footer">
            ✨ Get insights into your messaging patterns, most used words, emoji usage, and much more!
        </p>
    </div>
    """, unsafe_allow_html=True)
