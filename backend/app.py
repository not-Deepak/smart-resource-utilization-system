"""
Flask Backend Application for Smart Resource Utilization System
Provides REST API endpoints for data upload, analysis, predictions, and recommendations
"""

from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from model import ResourcePredictor

app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Configure upload folder
UPLOAD_FOLDER = '../dataset'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variables to store current data and model
current_data = None
current_predictor = None
current_analytics = None


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render main application page"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and initial data processing
    
    Returns:
        JSON with upload status and data preview
    """
    global current_data, current_predictor, current_analytics
    
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only CSV files are allowed'}), 400
        
        # Read CSV file
        df = pd.read_csv(file)
        
        # Initialize predictor
        predictor = ResourcePredictor()
        
        # Store original row count
        original_rows = len(df)
        
        # Preprocess data
        df = predictor.preprocess_data(df)
        cleaned_rows = len(df)
        
        # Check if data is valid
        if cleaned_rows == 0:
            return jsonify({'error': 'No valid data found in file'}), 400
        
        # Store in global variables
        current_data = df
        current_predictor = predictor
        
        # Generate preview (first 10 rows)
        preview_data = df.head(10).to_dict(orient='records')
        
        return jsonify({
            'success': True,
            'message': 'File uploaded and processed successfully',
            'rows_original': original_rows,
            'rows_cleaned': cleaned_rows,
            'columns': list(df.columns),
            'preview': preview_data
        })
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    """
    Perform comprehensive data analysis
    
    Returns:
        JSON with analytics results
    """
    global current_data, current_predictor, current_analytics
    
    try:
        if current_data is None or current_predictor is None:
            return jsonify({'error': 'No data loaded. Please upload a file first.'}), 400
        
        # Get analytics
        analytics = current_predictor.get_analytics(current_data)
        current_analytics = analytics
        
        # Train model
        training_metrics = current_predictor.train_model(current_data)
        
        return jsonify({
            'success': True,
            'analytics': analytics,
            'training_metrics': training_metrics
        })
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing data: {str(e)}'}), 500


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Generate predictions for specified parameters
    
    Request body:
        hour (optional): Specific hour (0-23)
        is_weekend: 0 for weekday, 1 for weekend
        
    Returns:
        JSON with prediction results
    """
    global current_predictor
    
    try:
        if current_predictor is None or not current_predictor.is_trained:
            return jsonify({'error': 'Model not trained. Please analyze data first.'}), 400
        
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'No data provided'}), 400
        
        is_weekend = int(data.get('is_weekend', 0))
        
        # If specific hour is provided
        if 'hour' in data:
            hour = int(data['hour'])
            if not 0 <= hour <= 23:
                return jsonify({'error': 'Hour must be between 0 and 23'}), 400
            
            prediction = current_predictor.predict_usage(hour, is_weekend)
            return jsonify({
                'success': True,
                'hour': hour,
                'is_weekend': is_weekend,
                'predicted_usage': round(prediction, 2)
            })
        
        # Otherwise predict for next 24 hours
        predictions = current_predictor.predict_next_24_hours(is_weekend)
        
        return jsonify({
            'success': True,
            'is_weekend': is_weekend,
            'predictions': predictions
        })
    
    except Exception as e:
        return jsonify({'error': f'Error making prediction: {str(e)}'}), 500


@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """
    Get optimization recommendations
    
    Returns:
        JSON with list of recommendations
    """
    global current_predictor, current_analytics
    
    try:
        if current_predictor is None or current_analytics is None:
            return jsonify({'error': 'No analysis available. Please analyze data first.'}), 400
        
        recommendations = current_predictor.get_recommendations(current_analytics)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({'error': f'Error generating recommendations: {str(e)}'}), 500


@app.route('/api/load-sample', methods=['POST'])
def load_sample_data():
    """
    Load the sample dataset for demonstration
    
    Returns:
        JSON with sample data load status
    """
    global current_data, current_predictor, current_analytics
    
    try:
        # Path to sample dataset
        sample_path = os.path.join(app.config['UPLOAD_FOLDER'], 'resource_usage.csv')
        
        if not os.path.exists(sample_path):
            return jsonify({'error': 'Sample dataset not found'}), 404
        
        # Load and process data
        df = pd.read_csv(sample_path)
        
        # Initialize predictor
        predictor = ResourcePredictor()
        
        # Preprocess
        df = predictor.preprocess_data(df)
        
        # Store in global variables
        current_data = df
        current_predictor = predictor
        
        # Get analytics and train model
        analytics = predictor.get_analytics(df)
        training_metrics = predictor.train_model(df)
        current_analytics = analytics
        
        return jsonify({
            'success': True,
            'message': 'Sample data loaded successfully',
            'rows': len(df),
            'analytics': analytics,
            'training_metrics': training_metrics
        })
    
    except Exception as e:
        return jsonify({'error': f'Error loading sample data: {str(e)}'}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Get current application status
    
    Returns:
        JSON with status information
    """
    global current_data, current_predictor
    
    status = {
        'data_loaded': current_data is not None,
        'model_trained': current_predictor is not None and current_predictor.is_trained if current_predictor else False,
        'rows': len(current_data) if current_data is not None else 0
    }
    
    return jsonify(status)


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Run application
    print("=" * 60)
    print("Smart Resource Utilization System - Backend Server")
    print("=" * 60)
    print("Server starting on http://127.0.0.1:5000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=5000)
