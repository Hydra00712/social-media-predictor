"""
DATABASE SETUP - SQLite for Local Storage
==========================================
Stores: posts, predictions, experiments, logs
"""

import sqlite3
import json
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path='database/social_media.db'):
        """Initialize database connection"""
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.conn = None
        self.create_tables()
    
    def get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def create_tables(self):
        """Create all necessary tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Table 1: Posts (incoming social media posts)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                platform TEXT NOT NULL,
                language TEXT,
                text_content TEXT,
                hashtags TEXT,
                mentions TEXT,
                keywords TEXT,
                topic_category TEXT,
                sentiment_score REAL,
                sentiment_label TEXT,
                emotion_type TEXT,
                toxicity_score REAL,
                brand_name TEXT,
                product_name TEXT,
                campaign_name TEXT,
                campaign_phase TEXT,
                user_past_sentiment_avg REAL,
                user_engagement_growth REAL,
                buzz_change_rate REAL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table 2: Predictions (model predictions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                predicted_engagement REAL NOT NULL,
                model_version TEXT,
                prediction_time TEXT DEFAULT CURRENT_TIMESTAMP,
                processing_time_ms REAL,
                FOREIGN KEY (post_id) REFERENCES posts(id)
            )
        ''')
        
        # Table 3: Experiments (MLflow-style tracking)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_name TEXT NOT NULL,
                model_type TEXT NOT NULL,
                parameters TEXT,
                metrics TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table 4: Monitoring Logs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitoring_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_level TEXT NOT NULL,
                component TEXT NOT NULL,
                message TEXT NOT NULL,
                details TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table 5: API Requests (for monitoring)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT NOT NULL,
                method TEXT NOT NULL,
                status_code INTEGER,
                response_time_ms REAL,
                error_message TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table 6: Alerts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                resolved BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                resolved_at TEXT
            )
        ''')
        
        conn.commit()
        print("✅ Database tables created successfully")
    
    def insert_post(self, post_data):
        """Insert a new post"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO posts (
                timestamp, platform, language, text_content, hashtags, mentions,
                keywords, topic_category, sentiment_score, sentiment_label,
                emotion_type, toxicity_score, brand_name, product_name,
                campaign_name, campaign_phase, user_past_sentiment_avg,
                user_engagement_growth, buzz_change_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            post_data.get('timestamp'),
            post_data.get('platform'),
            post_data.get('language'),
            post_data.get('text_content'),
            post_data.get('hashtags'),
            post_data.get('mentions'),
            post_data.get('keywords'),
            post_data.get('topic_category'),
            post_data.get('sentiment_score'),
            post_data.get('sentiment_label'),
            post_data.get('emotion_type'),
            post_data.get('toxicity_score'),
            post_data.get('brand_name'),
            post_data.get('product_name'),
            post_data.get('campaign_name'),
            post_data.get('campaign_phase'),
            post_data.get('user_past_sentiment_avg'),
            post_data.get('user_engagement_growth'),
            post_data.get('buzz_change_rate')
        ))
        
        conn.commit()
        return cursor.lastrowid
    
    def insert_prediction(self, post_id, predicted_engagement, model_version, processing_time_ms):
        """Insert a prediction"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (post_id, predicted_engagement, model_version, processing_time_ms)
            VALUES (?, ?, ?, ?)
        ''', (post_id, predicted_engagement, model_version, processing_time_ms))
        
        conn.commit()
        return cursor.lastrowid
    
    def log_event(self, level, component, message, details=None):
        """Log a monitoring event"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO monitoring_logs (log_level, component, message, details)
            VALUES (?, ?, ?, ?)
        ''', (level, component, message, json.dumps(details) if details else None))
        
        conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None


if __name__ == '__main__':
    print("=" * 80)
    print("🗄️  INITIALIZING DATABASE")
    print("=" * 80)
    
    db = DatabaseManager()
    print("\n✅ Database initialized successfully!")
    print(f"📁 Location: {db.db_path}")
    
    db.close()
    print("\n" + "=" * 80)

