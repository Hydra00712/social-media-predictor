"""
Data Balancing & Class Imbalance Handling
==========================================
Handles imbalanced data using SMOTE and other techniques
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataBalancer:
    """Handle imbalanced datasets using various techniques"""
    
    def __init__(self, strategy='smote', random_state=42):
        """
        Initialize data balancer
        
        Args:
            strategy: 'smote', 'adasyn', 'combined', 'undersample', or None
            random_state: Random seed for reproducibility
        """
        self.strategy = strategy
        self.random_state = random_state
        self.balancer = None
        self.original_distribution = None
        self.balanced_distribution = None
        
        logger.info(f"✅ DataBalancer initialized with strategy: {strategy}")
    
    def analyze_imbalance(self, y, feature_name='target'):
        """
        Analyze class imbalance in the dataset
        
        Args:
            y: Target variable (array or Series)
            feature_name: Name of the feature being analyzed
        
        Returns:
            dict: Imbalance statistics
        """
        try:
            # Get class distribution
            unique, counts = np.unique(y, return_counts=True)
            distribution = dict(zip(unique, counts))
            
            # Calculate imbalance ratio
            max_count = max(counts)
            min_count = min(counts)
            imbalance_ratio = max_count / min_count
            
            # Calculate percentages
            total = sum(counts)
            percentages = {k: (v / total) * 100 for k, v in distribution.items()}
            
            analysis = {
                'feature': feature_name,
                'class_distribution': distribution,
                'class_percentages': percentages,
                'total_samples': total,
                'imbalance_ratio': imbalance_ratio,
                'is_imbalanced': imbalance_ratio > 1.5,  # Threshold for imbalance
                'majority_class': max(distribution, key=distribution.get),
                'minority_class': min(distribution, key=distribution.get),
                'majority_count': max_count,
                'minority_count': min_count,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"📊 Class distribution analysis complete")
            logger.info(f"   Imbalance ratio: {imbalance_ratio:.2f}:1")
            logger.info(f"   Majority class: {analysis['majority_class']} ({analysis['majority_count']} samples)")
            logger.info(f"   Minority class: {analysis['minority_class']} ({analysis['minority_count']} samples)")
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Error analyzing imbalance: {e}")
            return None
    
    def balance_data(self, X, y):
        """
        Balance the dataset using the specified strategy
        
        Args:
            X: Features (array or DataFrame)
            y: Target variable (array or Series)
        
        Returns:
            tuple: (X_balanced, y_balanced)
        """
        try:
            # Store original distribution
            self.original_distribution = self.analyze_imbalance(y)
            
            logger.info(f"🔄 Balancing data with {self.strategy} strategy...")
            
            if self.strategy == 'smote':
                # SMOTE: Synthetic Minority Over-sampling Technique
                self.balancer = SMOTE(random_state=self.random_state)
                X_balanced, y_balanced = self.balancer.fit_resample(X, y)
                
                logger.info(f"✅ SMOTE applied: Generated synthetic samples for minority class")
                
            elif self.strategy == 'adasyn':
                # ADASYN: Adaptive Synthetic Sampling
                self.balancer = ADASYN(random_state=self.random_state)
                X_balanced, y_balanced = self.balancer.fit_resample(X, y)
                
                logger.info(f"✅ ADASYN applied: Adaptive sampling based on density")
                
            elif self.strategy == 'combined':
                # Combine undersampling and oversampling
                self.balancer = ImbPipeline([
                    ('undersample', RandomUnderSampler(random_state=self.random_state)),
                    ('smote', SMOTE(random_state=self.random_state))
                ])
                X_balanced, y_balanced = self.balancer.fit_resample(X, y)
                
                logger.info(f"✅ Combined strategy applied: Undersample + SMOTE")
                
            elif self.strategy == 'undersample':
                # Random undersampling
                self.balancer = RandomUnderSampler(random_state=self.random_state)
                X_balanced, y_balanced = self.balancer.fit_resample(X, y)
                
                logger.info(f"✅ Random undersampling applied")
                
            else:
                logger.warning(f"⚠️ Unknown strategy: {self.strategy}, returning original data")
                return X, y
            
            # Store balanced distribution
            self.balanced_distribution = self.analyze_imbalance(y_balanced)
            
            # Print balancing report
            self._print_balancing_report()
            
            return X_balanced, y_balanced
            
        except Exception as e:
            logger.error(f"❌ Error balancing data: {e}")
            return X, y
    
    def _print_balancing_report(self):
        """Print a report comparing original vs balanced distribution"""
        if not self.original_distribution or not self.balanced_distribution:
            return
        
        logger.info("\n" + "="*60)
        logger.info("📊 DATA BALANCING REPORT")
        logger.info("="*60)
        
        logger.info("\n🔴 BEFORE BALANCING:")
        orig = self.original_distribution
        for class_label, count in orig['class_distribution'].items():
            percentage = orig['class_percentages'].get(class_label, 0)
            logger.info(f"   Class {class_label}: {count:>6} samples ({percentage:>5.1f}%)")
        logger.info(f"   Imbalance ratio: {orig['imbalance_ratio']:.2f}:1")
        
        logger.info("\n🟢 AFTER BALANCING:")
        balanced = self.balanced_distribution
        for class_label, count in balanced['class_distribution'].items():
            percentage = balanced['class_percentages'].get(class_label, 0)
            logger.info(f"   Class {class_label}: {count:>6} samples ({percentage:>5.1f}%)")
        logger.info(f"   Imbalance ratio: {balanced['imbalance_ratio']:.2f}:1")
        
        logger.info("\n📈 IMPROVEMENT:")
        improvement = orig['imbalance_ratio'] - balanced['imbalance_ratio']
        improvement_pct = (improvement / orig['imbalance_ratio']) * 100
        logger.info(f"   Imbalance ratio improved by: {improvement:.2f} ({improvement_pct:.1f}%)")
        
        logger.info("="*60 + "\n")
    
    def get_balancing_report(self):
        """Return balancing report as dictionary"""
        return {
            'original_distribution': self.original_distribution,
            'balanced_distribution': self.balanced_distribution,
            'strategy_used': self.strategy,
            'improvement': {
                'imbalance_ratio_before': self.original_distribution['imbalance_ratio'],
                'imbalance_ratio_after': self.balanced_distribution['imbalance_ratio'],
                'ratio_improvement': self.original_distribution['imbalance_ratio'] - self.balanced_distribution['imbalance_ratio']
            } if self.original_distribution and self.balanced_distribution else None
        }


class StratifiedBalancer:
    """Balance data while preserving training/test split stratification"""
    
    @staticmethod
    def split_and_balance(X, y, test_size=0.2, balance_strategy='smote', random_state=42):
        """
        Split data into train/test while maintaining class distribution and balancing
        
        Args:
            X: Features
            y: Target
            test_size: Test set size (0-1)
            balance_strategy: Strategy for balancing training data
            random_state: Random seed
        
        Returns:
            dict: Train/test split with balancing info
        """
        try:
            # First, split with stratification to preserve class distribution
            X_train, X_test, y_train, y_test = train_test_split(
                X, y,
                test_size=test_size,
                random_state=random_state,
                stratify=y
            )
            
            logger.info("✅ Data split with stratification preserved")
            
            # Then, balance only the training data
            balancer = DataBalancer(strategy=balance_strategy, random_state=random_state)
            X_train_balanced, y_train_balanced = balancer.balance_data(X_train, y_train)
            
            report = balancer.get_balancing_report()
            
            result = {
                'X_train': X_train_balanced,
                'X_test': X_test,
                'y_train': y_train_balanced,
                'y_test': y_test,
                'train_size': len(X_train_balanced),
                'test_size': len(X_test),
                'balancing_report': report,
                'note': 'Test set NOT balanced (use for fair evaluation)'
            }
            
            logger.info(f"✅ Train/test split complete")
            logger.info(f"   Training set size: {result['train_size']} (balanced)")
            logger.info(f"   Test set size: {result['test_size']} (original distribution)")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error in stratified split and balance: {e}")
            return None


class ImbalanceMetrics:
    """Calculate metrics related to class imbalance"""
    
    @staticmethod
    def calculate_imbalance_metrics(y_true, y_pred=None):
        """
        Calculate various imbalance-related metrics
        
        Args:
            y_true: True labels
            y_pred: Predicted labels (optional)
        
        Returns:
            dict: Imbalance metrics
        """
        metrics = {}
        
        # Class distribution
        unique, counts = np.unique(y_true, return_counts=True)
        metrics['class_distribution'] = dict(zip(unique, counts))
        
        # Imbalance ratio
        metrics['imbalance_ratio'] = max(counts) / min(counts)
        
        # Class weights (for weighted loss functions)
        total = sum(counts)
        metrics['class_weights'] = {
            label: total / (len(unique) * count)
            for label, count in zip(unique, counts)
        }
        
        # Minority class frequency
        metrics['minority_class_frequency'] = min(counts) / total
        
        if y_pred is not None:
            # Per-class recall (important for imbalanced data)
            from sklearn.metrics import recall_score, precision_score, f1_score
            
            metrics['weighted_recall'] = recall_score(y_true, y_pred, average='weighted', zero_division=0)
            metrics['weighted_precision'] = precision_score(y_true, y_pred, average='weighted', zero_division=0)
            metrics['weighted_f1'] = f1_score(y_true, y_pred, average='weighted', zero_division=0)
            
            # Macro averages (equal weight per class)
            metrics['macro_recall'] = recall_score(y_true, y_pred, average='macro', zero_division=0)
            metrics['macro_precision'] = precision_score(y_true, y_pred, average='macro', zero_division=0)
            metrics['macro_f1'] = f1_score(y_true, y_pred, average='macro', zero_division=0)
        
        return metrics


if __name__ == '__main__':
    print("=" * 80)
    print("📊 DATA BALANCING TEST")
    print("=" * 80)
    
    # Create sample imbalanced data
    np.random.seed(42)
    X = np.random.randn(1000, 10)
    y = np.concatenate([
        np.zeros(900),   # Majority class: 90%
        np.ones(100)     # Minority class: 10%
    ])
    
    # Shuffle
    indices = np.random.permutation(len(y))
    X, y = X[indices], y[indices]
    
    print(f"\n📊 Original data shape: {X.shape}")
    
    # Test analysis
    balancer = DataBalancer(strategy='smote')
    
    print("\n🔴 ANALYZING IMBALANCE:")
    analysis = balancer.analyze_imbalance(y)
    print(f"   Imbalance ratio: {analysis['imbalance_ratio']:.2f}:1")
    print(f"   Is imbalanced: {analysis['is_imbalanced']}")
    
    # Test balancing
    print("\n🟢 APPLYING BALANCING:")
    X_balanced, y_balanced = balancer.balance_data(X, y)
    
    print(f"\n✅ Balanced data shape: {X_balanced.shape}")
    print(f"   Original samples: {len(y)}")
    print(f"   Balanced samples: {len(y_balanced)}")
    
    # Test stratified split
    print("\n🔄 STRATIFIED SPLIT WITH BALANCING:")
    result = StratifiedBalancer.split_and_balance(X, y, test_size=0.2)
    
    if result:
        print(f"   Train set: {result['train_size']} samples")
        print(f"   Test set: {result['test_size']} samples")
    
    print("\n✅ Data balancing test complete!")
    print("=" * 80)
