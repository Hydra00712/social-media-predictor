"""
MONITORING DASHBOARD
====================
Real-time monitoring of API performance, predictions, and alerts
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_setup import DatabaseManager

# Page config
st.set_page_config(
    page_title="Monitoring Dashboard",
    page_icon="📊",
    layout="wide"
)

# Initialize database
@st.cache_resource
def get_db():
    return DatabaseManager()

db = get_db()

# Title
st.title("📊 Monitoring Dashboard")
st.markdown("### Real-time system monitoring and analytics")

# Auto-refresh
if st.sidebar.checkbox("Auto-refresh (5s)", value=False):
    st.rerun()

# ============================================================================
# METRICS OVERVIEW
# ============================================================================
st.header("📈 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

try:
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Total posts
    cursor.execute("SELECT COUNT(*) as count FROM posts")
    total_posts = cursor.fetchone()['count']
    
    # Total predictions
    cursor.execute("SELECT COUNT(*) as count FROM predictions")
    total_predictions = cursor.fetchone()['count']
    
    # Average engagement
    cursor.execute("SELECT AVG(predicted_engagement) as avg FROM predictions")
    avg_engagement = cursor.fetchone()['avg'] or 0
    
    # Recent predictions (last hour)
    cursor.execute("""
        SELECT COUNT(*) as count FROM predictions 
        WHERE datetime(prediction_time) > datetime('now', '-1 hour')
    """)
    recent_predictions = cursor.fetchone()['count']
    
    with col1:
        st.metric("Total Posts", f"{total_posts:,}")
    
    with col2:
        st.metric("Total Predictions", f"{total_predictions:,}")
    
    with col3:
        st.metric("Avg Engagement", f"{avg_engagement:.4f}")
    
    with col4:
        st.metric("Last Hour", f"{recent_predictions}")

except Exception as e:
    st.error(f"Error loading metrics: {e}")

# ============================================================================
# PREDICTIONS OVER TIME
# ============================================================================
st.header("📊 Predictions Over Time")

try:
    # Get predictions with timestamps
    df_predictions = pd.read_sql_query("""
        SELECT 
            datetime(pr.prediction_time) as time,
            pr.predicted_engagement,
            p.platform
        FROM predictions pr
        JOIN posts p ON pr.post_id = p.id
        ORDER BY pr.prediction_time DESC
        LIMIT 100
    """, conn)
    
    if len(df_predictions) > 0:
        # Line chart
        fig = px.line(
            df_predictions, 
            x='time', 
            y='predicted_engagement',
            color='platform',
            title='Predicted Engagement Over Time'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No predictions yet. Make some predictions to see the chart!")

except Exception as e:
    st.error(f"Error loading predictions: {e}")

# ============================================================================
# PLATFORM DISTRIBUTION
# ============================================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📱 Platform Distribution")
    try:
        df_platforms = pd.read_sql_query("""
            SELECT platform, COUNT(*) as count
            FROM posts
            GROUP BY platform
            ORDER BY count DESC
        """, conn)
        
        if len(df_platforms) > 0:
            fig = px.pie(df_platforms, values='count', names='platform', title='Posts by Platform')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet")
    except Exception as e:
        st.error(f"Error: {e}")

with col2:
    st.subheader("😊 Sentiment Distribution")
    try:
        df_sentiment = pd.read_sql_query("""
            SELECT sentiment_label, COUNT(*) as count
            FROM posts
            WHERE sentiment_label IS NOT NULL
            GROUP BY sentiment_label
            ORDER BY count DESC
        """, conn)
        
        if len(df_sentiment) > 0:
            fig = px.bar(df_sentiment, x='sentiment_label', y='count', title='Posts by Sentiment')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet")
    except Exception as e:
        st.error(f"Error: {e}")

# ============================================================================
# RECENT ACTIVITY
# ============================================================================
st.header("🕐 Recent Activity")

try:
    df_recent = pd.read_sql_query("""
        SELECT 
            p.platform,
            p.text_content,
            pr.predicted_engagement,
            datetime(pr.prediction_time) as time
        FROM predictions pr
        JOIN posts p ON pr.post_id = p.id
        ORDER BY pr.prediction_time DESC
        LIMIT 10
    """, conn)
    
    if len(df_recent) > 0:
        st.dataframe(df_recent, use_container_width=True)
    else:
        st.info("No recent activity")

except Exception as e:
    st.error(f"Error: {e}")

# ============================================================================
# SYSTEM LOGS
# ============================================================================
st.header("📝 System Logs")

try:
    df_logs = pd.read_sql_query("""
        SELECT 
            log_level,
            component,
            message,
            datetime(created_at) as time
        FROM monitoring_logs
        ORDER BY created_at DESC
        LIMIT 20
    """, conn)
    
    if len(df_logs) > 0:
        st.dataframe(df_logs, use_container_width=True)
    else:
        st.info("No logs yet")

except Exception as e:
    st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

