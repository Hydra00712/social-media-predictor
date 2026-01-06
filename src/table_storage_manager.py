"""
Azure Table Storage Manager
Manages social media posts and interactions using Azure Table Storage (FREE alternative to Cosmos DB)
Cost: $0.00 - Uses existing storage account
"""

from azure.data.tables import TableServiceClient, TableEntity
from azure.core.exceptions import ResourceExistsError
from datetime import datetime
import os
from azure_config import AZURE_CONFIG

class TableStorageManager:
    """Manage social media data in Azure Table Storage"""
    
    def __init__(self):
        """Initialize Table Storage client"""
        connection_string = AZURE_CONFIG['storage_connection_string']
        self.table_service = TableServiceClient.from_connection_string(connection_string)
        
        # Table names
        self.posts_table_name = "socialmediaposts"
        self.interactions_table_name = "interactions"
        
        # Get table clients
        self.posts_table = self.table_service.get_table_client(self.posts_table_name)
        self.interactions_table = self.table_service.get_table_client(self.interactions_table_name)
        
        print(f"✅ Connected to Azure Table Storage")
        print(f"   📊 Posts table: {self.posts_table_name}")
        print(f"   📊 Interactions table: {self.interactions_table_name}")
    
    def add_post(self, post_id, platform, content, predicted_engagement, actual_engagement=None):
        """
        Add a social media post to Table Storage
        
        Args:
            post_id: Unique post identifier
            platform: Social media platform (Instagram, Twitter, etc.)
            content: Post content/text
            predicted_engagement: ML predicted engagement score
            actual_engagement: Actual engagement score (optional)
        """
        entity = {
            'PartitionKey': platform,  # Partition by platform for better performance
            'RowKey': post_id,
            'Content': content,
            'PredictedEngagement': predicted_engagement,
            'ActualEngagement': actual_engagement if actual_engagement else 0.0,
            'CreatedAt': datetime.utcnow().isoformat(),
            'Platform': platform
        }
        
        try:
            self.posts_table.create_entity(entity=entity)
            print(f"✅ Post {post_id} added to Table Storage")
            return True
        except ResourceExistsError:
            print(f"⚠️  Post {post_id} already exists")
            return False
        except Exception as e:
            print(f"❌ Error adding post: {e}")
            return False
    
    def add_interaction(self, interaction_id, post_id, user_id, interaction_type, timestamp=None):
        """
        Add a user interaction (like, share, comment) to Table Storage
        
        Args:
            interaction_id: Unique interaction identifier
            post_id: Related post ID
            user_id: User who interacted
            interaction_type: Type of interaction (like, share, comment)
            timestamp: When the interaction occurred
        """
        entity = {
            'PartitionKey': post_id,  # Partition by post_id
            'RowKey': interaction_id,
            'PostId': post_id,
            'UserId': user_id,
            'Type': interaction_type,
            'Timestamp': timestamp if timestamp else datetime.utcnow().isoformat()
        }
        
        try:
            self.interactions_table.create_entity(entity=entity)
            print(f"✅ Interaction {interaction_id} added")
            return True
        except Exception as e:
            print(f"❌ Error adding interaction: {e}")
            return False
    
    def get_post(self, platform, post_id):
        """Retrieve a specific post"""
        try:
            entity = self.posts_table.get_entity(partition_key=platform, row_key=post_id)
            return entity
        except Exception as e:
            print(f"❌ Error retrieving post: {e}")
            return None
    
    def get_all_posts(self, platform=None):
        """Retrieve all posts, optionally filtered by platform"""
        try:
            if platform:
                # Filter by platform (partition key)
                filter_query = f"PartitionKey eq '{platform}'"
                entities = self.posts_table.query_entities(filter_query)
            else:
                # Get all posts
                entities = self.posts_table.list_entities()
            
            return list(entities)
        except Exception as e:
            print(f"❌ Error retrieving posts: {e}")
            return []
    
    def get_post_interactions(self, post_id):
        """Get all interactions for a specific post"""
        try:
            filter_query = f"PartitionKey eq '{post_id}'"
            entities = self.interactions_table.query_entities(filter_query)
            return list(entities)
        except Exception as e:
            print(f"❌ Error retrieving interactions: {e}")
            return []
    
    def update_actual_engagement(self, platform, post_id, actual_engagement):
        """Update the actual engagement score for a post"""
        try:
            entity = self.posts_table.get_entity(partition_key=platform, row_key=post_id)
            entity['ActualEngagement'] = actual_engagement
            entity['UpdatedAt'] = datetime.utcnow().isoformat()
            
            self.posts_table.update_entity(entity=entity, mode='replace')
            print(f"✅ Updated actual engagement for post {post_id}")
            return True
        except Exception as e:
            print(f"❌ Error updating engagement: {e}")
            return False
    
    def get_statistics(self):
        """Get statistics about stored data"""
        try:
            posts = list(self.posts_table.list_entities())
            interactions = list(self.interactions_table.list_entities())
            
            stats = {
                'total_posts': len(posts),
                'total_interactions': len(interactions),
                'platforms': list(set([p.get('Platform', 'Unknown') for p in posts]))
            }
            
            return stats
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    print("=" * 70)
    print("AZURE TABLE STORAGE - SOCIAL MEDIA DATA MANAGER")
    print("=" * 70)
    print()
    
    # Initialize manager
    manager = TableStorageManager()
    
    # Example: Add a post
    print("\n📝 Adding sample post...")
    manager.add_post(
        post_id="post_001",
        platform="Instagram",
        content="Check out our new product launch! #innovation",
        predicted_engagement=0.75
    )
    
    # Example: Add interactions
    print("\n👍 Adding sample interactions...")
    manager.add_interaction("int_001", "post_001", "user_123", "like")
    manager.add_interaction("int_002", "post_001", "user_456", "share")
    manager.add_interaction("int_003", "post_001", "user_789", "comment")
    
    # Example: Get statistics
    print("\n📊 Statistics:")
    stats = manager.get_statistics()
    print(f"   Total posts: {stats.get('total_posts', 0)}")
    print(f"   Total interactions: {stats.get('total_interactions', 0)}")
    print(f"   Platforms: {', '.join(stats.get('platforms', []))}")
    
    print("\n✅ Table Storage manager ready!")
    print("💰 Cost: $0.00 (uses existing storage account)")
