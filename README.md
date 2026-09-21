# Smart Resource Utilization System

An intelligent web-based system that analyzes historical resource usage data (electricity) to identify patterns, predict future consumption, and suggest optimization strategies to reduce wastage and improve efficiency.

> Developed and maintained by **Deepak Kumar**.

**GitHub repository:** [not-Deepak/smart-resource-utilization-system](https://github.com/not-Deepak/smart-resource-utilization-system)

## 🌟 Project Overview

This project demonstrates the application of Machine Learning and Data Analytics to solve real-world resource management problems. The system processes electricity consumption data, trains a predictive model, and provides actionable insights through an intuitive web interface.

**Suitable for:** College projects, research papers, technical presentations, and portfolio demonstrations.

## ✨ Key Features

### 1. **Data Management**
- CSV dataset upload and validation
- Automatic data cleaning and preprocessing
- Data preview with tabular visualization
- Sample dataset included for demonstration

### 2. **Interactive Analytics Dashboard**
- **Real-time Statistics:** Total consumption, average usage, peak consumption
- **Hourly Usage Trends:** Line chart showing consumption patterns throughout the day
- **Department-wise Analysis:** Bar chart comparing consumption across departments
- **Weekday vs Weekend Comparison:** Doughnut chart visualizing usage differences

### 3. **Machine Learning Predictions**
- Linear Regression model for consumption forecasting
- 24-hour usage predictions for weekdays and weekends
- Model performance metrics (R² score, RMSE, accuracy percentage)
- Interactive prediction visualization

### 4. **Optimization Recommendations**
- Peak usage optimization strategies
- Weekend energy management tips
- Department-specific recommendations
- Night-time power management insights
- Equipment efficiency suggestions
- Potential savings percentages for each recommendation

### 5. **Modern User Interface**
- Responsive design for all screen sizes
- Smooth animations and transitions
- Professional color scheme and typography
- Drag-and-drop file upload
- Loading indicators and user feedback
- Clean, intuitive navigation

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **Scikit-learn** - Machine learning (Linear Regression)

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with modern design patterns
- **JavaScript (ES6+)** - Interactive functionality
- **Chart.js** - Data visualizations

### Data
- **CSV** - Dataset format
- Sample dataset with 192+ records included

## 📁 Project Structure

```
smart-resource-utilization-system/
├── backend/
│   ├── app.py              # Flask application with REST API
│   └── model.py            # ML model and data processing
├── frontend/
│   ├── templates/
│   │   └── index.html      # Main web interface
│   └── static/
│       ├── css/
│       │   └── style.css   # Styling
│       └── js/
│           └── app.js      # Frontend logic and Chart.js
├── dataset/
│   └── resource_usage.csv  # Sample electricity usage data
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Clone or Download the Project
```bash
cd smart-resource-utilization
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
cd backend
python app.py
```

### Step 4: Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## 📊 Usage Guide

### Quick Start with Sample Data
1. Click the **"Try Sample Data"** button on the home page
2. The system will automatically load and analyze the included dataset
3. Explore the analytics dashboard, predictions, and recommendations

### Using Your Own Data
1. Navigate to the **"Upload Data"** section
2. Click **"Browse Files"** or drag and drop a CSV file
3. Ensure your CSV has these columns:
   - `timestamp` - Date and time of measurement
   - `department` - Department or area name
   - `usage_kwh` - Usage in kilowatt-hours
   - `hour` - Hour of day (0-23)
   - `is_weekend` - 1 for weekend, 0 for weekday
4. Click **"Analyze Data"** after upload
5. View insights in Analytics, Predictions, and Recommendations sections

### Generating Predictions
1. Complete data analysis first
2. Go to **"Predictions"** section
3. Select weekday or weekend
4. Click **"Predict Next 24 Hours"**
5. View the forecast chart

## 📈 Dataset Format

Your CSV file should follow this structure:

```csv
timestamp,department,usage_kwh,day_of_week,hour,is_weekend
2024-01-01 00:00:00,IT,45.2,Monday,0,0
2024-01-01 01:00:00,IT,42.1,Monday,1,0
...
```

### Column Descriptions
- **timestamp**: ISO format datetime (YYYY-MM-DD HH:MM:SS)
- **department**: String identifier for department/area
- **usage_kwh**: Numeric value (float/integer)
- **day_of_week**: Day name (optional, for reference)
- **hour**: Integer 0-23
- **is_weekend**: Binary (0 or 1)

## 🧮 Machine Learning Model

### Algorithm: Linear Regression
- **Features**: Hour of day, Weekend indicator
- **Target**: Usage in kWh
- **Training Split**: 80% training, 20% testing
- **Evaluation Metrics**: Mean Squared Error (MSE), R² Score, RMSE

### Model Pipeline
1. Data preprocessing and cleaning
2. Feature selection
3. Train-test split
4. Model training
5. Performance evaluation
6. Prediction generation

## 🎯 Key Insights Generated

The system provides:
- Total and average consumption metrics
- Peak usage hours identification
- Department-wise consumption breakdown
- Weekday vs weekend patterns
- 24-hour consumption forecasts
- Actionable optimization recommendations with savings estimates

## 🎓 Educational Value

### Suitable For:
- **College Projects**: Demonstrates full-stack development and ML integration
- **Research Papers**: Real-world application of predictive analytics
- **Technical Presentations**: Visual and easy to explain
- **Portfolio**: Showcases multiple technical skills

### Concepts Demonstrated:
- Full-stack web development
- RESTful API design
- Machine learning implementation
- Data preprocessing and cleaning
- Data visualization
- Responsive web design
- User experience design

## 🔧 Customization

### Modifying the ML Model
Edit `backend/model.py` to:
- Add more features
- Try different algorithms (Random Forest, Neural Networks)
- Adjust training parameters

### Changing the UI
Edit `frontend/static/css/style.css` to:
- Modify color scheme
- Adjust layout and spacing
- Add custom animations

### Adding New Features
- Extend `backend/app.py` for new API endpoints
- Update `frontend/static/js/app.js` for new functionality
- Modify `frontend/templates/index.html` for new sections

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/api/upload` | POST | Upload CSV file |
| `/api/analyze` | POST | Analyze data and train model |
| `/api/predict` | POST | Generate predictions |
| `/api/recommendations` | GET | Get optimization recommendations |
| `/api/load-sample` | POST | Load sample dataset |
| `/api/status` | GET | Get system status |

## 🐛 Troubleshooting

### Common Issues

**Issue: Module not found error**
```bash
pip install -r requirements.txt
```

**Issue: Port 5000 already in use**
Edit `backend/app.py` and change the port:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

**Issue: Charts not displaying**
- Ensure you have internet connection (Chart.js loads from CDN)
- Check browser console for JavaScript errors
- Clear browser cache and reload

## 💡 Future Enhancements

Potential improvements for advanced versions:
- Database integration (PostgreSQL/MongoDB)
- User authentication and multi-user support
- Real-time data streaming
- Advanced ML models (LSTM, Prophet)
- Export reports to PDF
- Email notifications for anomalies
- Mobile app version
- Integration with IoT sensors

## 📄 License

This project is created for educational purposes. Feel free to use and modify for your college projects and learning.

## 👤 Project Owner

**Deepak Kumar**  
GitHub: [@not-Deepak](https://github.com/not-Deepak)

## 🙏 Acknowledgments

- Flask framework for backend development
- Scikit-learn for machine learning capabilities
- Chart.js for beautiful data visualizations
- Python community for excellent libraries

## 📧 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments for detailed explanations
3. Consult Flask and Scikit-learn documentation

---

**Note for Viva/Presentation:**
- Explain the ML model clearly (Linear Regression)
- Highlight the data preprocessing steps
- Demonstrate the live application
- Discuss potential real-world applications
- Show understanding of full-stack development
- Explain design choices (why Flask, why Chart.js, etc.)

**Good luck with your project presentation! 🎓✨**
