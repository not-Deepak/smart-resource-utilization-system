"""
Machine Learning Model Module for Resource Usage Prediction
Handles data preprocessing, model training, and predictions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


class ResourcePredictor:
    """
    Machine Learning model for predicting resource usage
    Uses Linear Regression to forecast electricity consumption
    """
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
        self.feature_columns = ['hour', 'is_weekend']
        
    def preprocess_data(self, df):
        """
        Clean and preprocess the dataset
        
        Args:
            df: Raw pandas DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Make a copy to avoid modifying original
        df = df.copy()
        
        # Convert timestamp to datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Handle missing values
        df = df.dropna()
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Ensure numeric columns are proper type
        numeric_columns = ['usage_kwh', 'hour', 'is_weekend']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove any rows with invalid data
        df = df.dropna()
        
        return df
    
    def get_analytics(self, df):
        """
        Generate comprehensive analytics from the dataset
        
        Args:
            df: Preprocessed pandas DataFrame
            
        Returns:
            Dictionary containing various analytics
        """
        analytics = {}
        
        # Overall statistics
        analytics['total_consumption'] = float(df['usage_kwh'].sum())
        analytics['average_consumption'] = float(df['usage_kwh'].mean())
        analytics['max_consumption'] = float(df['usage_kwh'].max())
        analytics['min_consumption'] = float(df['usage_kwh'].min())
        
        # Hourly trends
        hourly_avg = df.groupby('hour')['usage_kwh'].mean().to_dict()
        analytics['hourly_trends'] = {int(k): float(v) for k, v in hourly_avg.items()}
        
        # Department-wise consumption
        if 'department' in df.columns:
            dept_consumption = df.groupby('department')['usage_kwh'].sum().to_dict()
            analytics['department_consumption'] = {str(k): float(v) for k, v in dept_consumption.items()}
            
            dept_avg = df.groupby('department')['usage_kwh'].mean().to_dict()
            analytics['department_average'] = {str(k): float(v) for k, v in dept_avg.items()}
        
        # Weekday vs Weekend comparison
        weekend_avg = df[df['is_weekend'] == 1]['usage_kwh'].mean()
        weekday_avg = df[df['is_weekend'] == 0]['usage_kwh'].mean()
        
        analytics['weekend_average'] = float(weekend_avg) if not pd.isna(weekend_avg) else 0
        analytics['weekday_average'] = float(weekday_avg) if not pd.isna(weekday_avg) else 0
        
        # Peak usage analysis
        peak_hour_data = df.loc[df['usage_kwh'].idxmax()]
        analytics['peak_usage'] = {
            'hour': int(peak_hour_data['hour']),
            'consumption': float(peak_hour_data['usage_kwh']),
            'department': str(peak_hour_data['department']) if 'department' in df.columns else 'N/A'
        }
        
        # Low usage analysis
        low_hour_data = df.loc[df['usage_kwh'].idxmin()]
        analytics['low_usage'] = {
            'hour': int(low_hour_data['hour']),
            'consumption': float(low_hour_data['usage_kwh'])
        }
        
        return analytics
    
    def train_model(self, df):
        """
        Train the Linear Regression model
        
        Args:
            df: Preprocessed pandas DataFrame
            
        Returns:
            Dictionary with training metrics
        """
        # Prepare features and target
        X = df[self.feature_columns]
        y = df['usage_kwh']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        return {
            'mse': float(mse),
            'rmse': float(np.sqrt(mse)),
            'r2_score': float(r2),
            'accuracy_percentage': float(r2 * 100)
        }
    
    def predict_usage(self, hour, is_weekend):
        """
        Predict resource usage for given parameters
        
        Args:
            hour: Hour of day (0-23)
            is_weekend: 1 if weekend, 0 if weekday
            
        Returns:
            Predicted usage in kWh
        """
        if not self.is_trained:
            raise Exception("Model not trained yet. Please train the model first.")
        
        # Prepare input
        input_data = pd.DataFrame({
            'hour': [hour],
            'is_weekend': [is_weekend]
        })
        
        prediction = self.model.predict(input_data)[0]
        return float(max(0, prediction))  # Ensure non-negative
    
    def predict_next_24_hours(self, is_weekend):
        """
        Predict usage for next 24 hours
        
        Args:
            is_weekend: 1 if weekend, 0 if weekday
            
        Returns:
            List of predictions for each hour
        """
        predictions = []
        for hour in range(24):
            pred = self.predict_usage(hour, is_weekend)
            predictions.append({
                'hour': hour,
                'predicted_usage': round(pred, 2)
            })
        return predictions
    
    def get_recommendations(self, analytics):
        """
        Generate optimization recommendations based on analytics
        
        Args:
            analytics: Analytics dictionary from get_analytics()
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        
        # Peak usage recommendation
        peak_hour = analytics['peak_usage']['hour']
        recommendations.append({
            'title': 'Peak Usage Optimization',
            'description': f'Peak consumption occurs at hour {peak_hour}. Consider shifting non-critical operations to off-peak hours.',
            'potential_savings': '15-20%',
            'priority': 'High',
            'icon': '⚡'
        })
        
        # Weekend vs Weekday recommendation
        if analytics['weekend_average'] > analytics['weekday_average'] * 0.5:
            recommendations.append({
                'title': 'Weekend Energy Management',
                'description': 'Weekend consumption is high. Implement automated systems to reduce unnecessary usage during weekends.',
                'potential_savings': '10-15%',
                'priority': 'Medium',
                'icon': '📅'
            })
        
        # Department-specific recommendation
        if 'department_consumption' in analytics:
            max_dept = max(analytics['department_consumption'].items(), key=lambda x: x[1])
            recommendations.append({
                'title': f'{max_dept[0]} Department Optimization',
                'description': f'{max_dept[0]} department has the highest consumption. Conduct an energy audit to identify wastage areas.',
                'potential_savings': '12-18%',
                'priority': 'High',
                'icon': '🏢'
            })
        
        # Night-time usage recommendation
        if any(analytics['hourly_trends'].get(h, 0) > analytics['average_consumption'] * 0.3 
               for h in range(0, 6)):
            recommendations.append({
                'title': 'Night-time Power Management',
                'description': 'Significant consumption detected during night hours (0-6 AM). Review and optimize lighting, HVAC, and equipment schedules.',
                'potential_savings': '8-12%',
                'priority': 'Medium',
                'icon': '🌙'
            })
        
        # General efficiency recommendation
        recommendations.append({
            'title': 'Energy-Efficient Equipment',
            'description': 'Upgrade to energy-efficient equipment and implement smart power management systems.',
            'potential_savings': '20-30%',
            'priority': 'High',
            'icon': '💡'
        })
        
        # HVAC optimization
        recommendations.append({
            'title': 'HVAC System Optimization',
            'description': 'Optimize HVAC settings based on occupancy patterns. Use smart thermostats and zone-based control.',
            'potential_savings': '15-25%',
            'priority': 'High',
            'icon': '❄️'
        })
        
        return recommendations


def load_and_analyze_data(file_path):
    """
    Convenience function to load data and perform complete analysis
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Tuple of (preprocessed_df, analytics, model, training_metrics)
    """
    # Load data
    df = pd.read_csv(file_path)
    
    # Initialize predictor
    predictor = ResourcePredictor()
    
    # Preprocess
    df = predictor.preprocess_data(df)
    
    # Get analytics
    analytics = predictor.get_analytics(df)
    
    # Train model
    training_metrics = predictor.train_model(df)
    
    return df, analytics, predictor, training_metrics
