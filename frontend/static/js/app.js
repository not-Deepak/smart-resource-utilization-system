/**
 * Smart Resource Utilization System - Frontend JavaScript
 * Handles all interactive functionality, AJAX calls, and Chart.js visualizations
 */

// Global variables
let hourlyChart = null;
let departmentChart = null;
let weekdayChart = null;
let forecastChart = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeFileUpload();
});

/**
 * Navigation functionality
 */
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Scroll to section
            const targetId = this.getAttribute('href').substring(1);
            scrollToSection(targetId);
        });
    });
}

/**
 * Scroll to section smoothly
 */
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * File upload functionality
 */
function initializeFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.borderColor = 'var(--primary-color)';
        this.style.background = 'rgba(37, 99, 235, 0.05)';
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.style.borderColor = 'var(--border-color)';
        this.style.background = '';
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.style.borderColor = 'var(--border-color)';
        this.style.background = '';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect({ target: fileInput });
        }
    });
}

/**
 * Handle file selection
 */
function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (!file) return;
    
    // Validate file type
    if (!file.name.endsWith('.csv')) {
        showAlert('uploadStatus', 'Only CSV files are allowed', 'error');
        return;
    }
    
    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        showAlert('uploadStatus', 'File size exceeds 16MB limit', 'error');
        return;
    }
    
    // Upload file
    uploadFile(file);
}

/**
 * Upload file to server
 */
async function uploadFile(file) {
    showLoading(true);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showAlert('uploadStatus', data.message, 'success');
            displayDataPreview(data);
        } else {
            showAlert('uploadStatus', data.error || 'Upload failed', 'error');
        }
    } catch (error) {
        showAlert('uploadStatus', 'Error uploading file: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

/**
 * Display data preview
 */
function displayDataPreview(data) {
    const previewDiv = document.getElementById('dataPreview');
    const tableDiv = document.getElementById('previewTable');
    
    // Create table
    let html = '<div class="preview-table"><table>';
    
    // Header
    html += '<thead><tr>';
    data.columns.forEach(col => {
        html += `<th>${col}</th>`;
    });
    html += '</tr></thead>';
    
    // Body (first 10 rows)
    html += '<tbody>';
    data.preview.forEach(row => {
        html += '<tr>';
        data.columns.forEach(col => {
            html += `<td>${row[col] !== null ? row[col] : '-'}</td>`;
        });
        html += '</tr>';
    });
    html += '</tbody></table></div>';
    
    html += `<p class="mt-2"><strong>Rows:</strong> ${data.rows_cleaned} (${data.rows_original} original)</p>`;
    
    tableDiv.innerHTML = html;
    previewDiv.style.display = 'block';
}

/**
 * Analyze data
 */
async function analyzeData() {
    showLoading(true);
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayAnalytics(data.analytics, data.training_metrics);
            await loadRecommendations();
            scrollToSection('analytics');
        } else {
            showAlert('analyticsContent', data.error || 'Analysis failed', 'error');
        }
    } catch (error) {
        showAlert('analyticsContent', 'Error analyzing data: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

/**
 * Display analytics results
 */
function displayAnalytics(analytics, metrics) {
    // Update statistics cards
    document.getElementById('totalConsumption').textContent = 
        analytics.total_consumption.toFixed(2);
    document.getElementById('avgConsumption').textContent = 
        analytics.average_consumption.toFixed(2);
    document.getElementById('peakConsumption').textContent = 
        analytics.max_consumption.toFixed(2);
    document.getElementById('modelAccuracy').textContent = 
        metrics.accuracy_percentage.toFixed(1);
    
    // Show stats cards
    document.getElementById('analyticsContent').style.display = 'none';
    document.getElementById('statsCards').style.display = 'grid';
    document.getElementById('chartsContainer').style.display = 'grid';
    
    // Create charts
    createHourlyChart(analytics.hourly_trends);
    createDepartmentChart(analytics.department_consumption);
    createWeekdayChart(analytics.weekday_average, analytics.weekend_average);
}

/**
 * Create hourly usage chart
 */
function createHourlyChart(hourlyData) {
    const ctx = document.getElementById('hourlyChart').getContext('2d');
    
    // Destroy existing chart
    if (hourlyChart) hourlyChart.destroy();
    
    const hours = Object.keys(hourlyData).sort((a, b) => parseInt(a) - parseInt(b));
    const values = hours.map(h => hourlyData[h]);
    
    hourlyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: hours.map(h => `${h}:00`),
            datasets: [{
                label: 'Average Usage (kWh)',
                data: values,
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Usage (kWh)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day'
                    }
                }
            }
        }
    });
}

/**
 * Create department chart
 */
function createDepartmentChart(deptData) {
    const ctx = document.getElementById('departmentChart').getContext('2d');
    
    // Destroy existing chart
    if (departmentChart) departmentChart.destroy();
    
    const departments = Object.keys(deptData);
    const values = Object.values(deptData);
    
    const colors = [
        '#2563eb',
        '#10b981',
        '#f59e0b',
        '#ef4444',
        '#8b5cf6'
    ];
    
    departmentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: departments,
            datasets: [{
                label: 'Total Consumption (kWh)',
                data: values,
                backgroundColor: colors.slice(0, departments.length),
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Usage (kWh)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Department'
                    }
                }
            }
        }
    });
}

/**
 * Create weekday vs weekend chart
 */
function createWeekdayChart(weekdayAvg, weekendAvg) {
    const ctx = document.getElementById('weekdayChart').getContext('2d');
    
    // Destroy existing chart
    if (weekdayChart) weekdayChart.destroy();
    
    weekdayChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Weekday Average', 'Weekend Average'],
            datasets: [{
                data: [weekdayAvg, weekendAvg],
                backgroundColor: ['#2563eb', '#10b981'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed.toFixed(2) + ' kWh';
                        }
                    }
                }
            }
        }
    });
}

/**
 * Generate predictions
 */
async function generatePredictions() {
    const isWeekend = document.querySelector('input[name="dayType"]:checked').value;
    
    showLoading(true);
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_weekend: parseInt(isWeekend) })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayPredictions(data.predictions, isWeekend);
            scrollToSection('predictions');
        } else {
            showAlert('predictionsContent', data.error || 'Prediction failed', 'error');
        }
    } catch (error) {
        showAlert('predictionsContent', 'Error generating predictions: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

/**
 * Display prediction results
 */
function displayPredictions(predictions, isWeekend) {
    document.getElementById('predictionsContent').innerHTML = 
        `<div class="alert alert-success">
            <span class="alert-icon">✓</span>
            <span>Predictions generated successfully for ${isWeekend == 1 ? 'weekend' : 'weekday'}</span>
        </div>`;
    
    document.getElementById('predictionChart').style.display = 'block';
    
    createForecastChart(predictions);
}

/**
 * Create forecast chart
 */
function createForecastChart(predictions) {
    const ctx = document.getElementById('forecastChart').getContext('2d');
    
    // Destroy existing chart
    if (forecastChart) forecastChart.destroy();
    
    const hours = predictions.map(p => p.hour);
    const values = predictions.map(p => p.predicted_usage);
    
    forecastChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: hours.map(h => `${h}:00`),
            datasets: [{
                label: 'Predicted Usage (kWh)',
                data: values,
                backgroundColor: 'rgba(16, 185, 129, 0.8)',
                borderColor: '#10b981',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Predicted Usage (kWh)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Hour of Day'
                    }
                }
            }
        }
    });
}

/**
 * Load recommendations
 */
async function loadRecommendations() {
    try {
        const response = await fetch('/api/recommendations');
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayRecommendations(data.recommendations);
        }
    } catch (error) {
        console.error('Error loading recommendations:', error);
    }
}

/**
 * Display recommendations
 */
function displayRecommendations(recommendations) {
    const grid = document.getElementById('recommendationsGrid');
    const content = document.getElementById('recommendationsContent');
    
    content.style.display = 'none';
    grid.style.display = 'grid';
    
    grid.innerHTML = recommendations.map(rec => `
        <div class="recommendation-card priority-${rec.priority.toLowerCase()}">
            <div class="recommendation-header">
                <div class="recommendation-icon">${rec.icon}</div>
                <div>
                    <h3 class="recommendation-title">${rec.title}</h3>
                </div>
            </div>
            <p class="recommendation-description">${rec.description}</p>
            <div class="recommendation-footer">
                <span class="savings-badge">💰 ${rec.potential_savings}</span>
                <span class="priority-badge ${rec.priority.toLowerCase()}">${rec.priority} Priority</span>
            </div>
        </div>
    `).join('');
}

/**
 * Load sample data
 */
async function loadSampleData() {
    showLoading(true);
    
    try {
        const response = await fetch('/api/load-sample', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showAlert('uploadStatus', 'Sample data loaded successfully!', 'success');
            
            // Display analytics automatically
            displayAnalytics(data.analytics, data.training_metrics);
            await loadRecommendations();
            
            // Hide upload area, show success message
            document.getElementById('dataPreview').innerHTML = `
                <div class="alert alert-success">
                    <span class="alert-icon">✓</span>
                    <span>Sample dataset loaded with ${data.rows} rows. Scroll down to view analytics!</span>
                </div>
            `;
            document.getElementById('dataPreview').style.display = 'block';
            
            scrollToSection('analytics');
        } else {
            alert('Error loading sample data: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Error loading sample data: ' + error.message);
    } finally {
        showLoading(false);
    }
}

/**
 * Show alert message
 */
function showAlert(elementId, message, type = 'info') {
    const element = document.getElementById(elementId);
    const iconMap = {
        info: 'ℹ️',
        success: '✓',
        error: '✕'
    };
    
    element.innerHTML = `
        <div class="alert alert-${type}">
            <span class="alert-icon">${iconMap[type]}</span>
            <span>${message}</span>
        </div>
    `;
}

/**
 * Show/hide loading overlay
 */
function showLoading(show) {
    document.getElementById('loadingOverlay').style.display = show ? 'flex' : 'none';
}

/**
 * Format number with commas
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
