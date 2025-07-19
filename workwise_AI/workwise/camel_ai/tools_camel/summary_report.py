import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

def generate_html(final_recommendation: Dict[str, Any], ticket_info: Dict[str, Any]) -> str:
    """
    Generate HTML report for employee recommendation
    
    Args:
        final_recommendation: Dictionary containing final recommendation from Gemini
        ticket_info: Dictionary containing ticket information
        
    Returns:
        HTML string for the report
    """
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract recommendation data
    success = final_recommendation.get("success", False)
    recommendation = final_recommendation.get("recommendation", {}) if success else {}
    
    # Helper function to create list items safely
    def create_list_items(items, default_text="None"):
        if not items:
            return f"<li>{default_text}</li>"
        return ''.join([f'<li>{str(item)}</li>' for item in items])
    
    # Helper function to safely get nested values
    def safe_get(dict_obj, key, default='N/A'):
        return dict_obj.get(key, default) if dict_obj else default
    
    # Create the HTML content
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Assignment Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .content {
            padding: 30px;
        }
        .section {
            margin-bottom: 30px;
            padding: 20px;
            border-left: 4px solid #667eea;
            background-color: #f8f9ff;
            border-radius: 0 8px 8px 0;
        }
        .section h2 {
            margin-top: 0;
            color: #667eea;
            font-size: 1.5em;
        }
        .ticket-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .info-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .info-card h3 {
            margin-top: 0;
            color: #555;
            font-size: 1.1em;
        }
        .recommendation-box {
            background: linear-gradient(135deg, #a8e6cf 0%, #88d8a3 100%);
            padding: 25px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            color: white;
        }
        .recommendation-box.error {
            background: linear-gradient(135deg, #ff8a80 0%, #ff5722 100%);
        }
        .confidence-score {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        .employee-name {
            font-size: 1.8em;
            font-weight: bold;
            margin: 15px 0;
        }
        .analysis-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .analysis-card {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        .analysis-card h4 {
            margin-top: 0;
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .skills-list, .factors-list {
            list-style: none;
            padding: 0;
        }
        .skills-list li, .factors-list li {
            background: #f0f4ff;
            margin: 5px 0;
            padding: 8px 12px;
            border-radius: 5px;
            border-left: 3px solid #667eea;
        }
        .footer {
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }
        .status-success {
            color: #28a745;
            font-weight: bold;
        }
        .status-error {
            color: #dc3545;
            font-weight: bold;
        }
        .json-view {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            border: 1px solid #e0e0e0;
            margin-top: 10px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Employee Assignment Report</h1>
            <p>Generated on """ + timestamp + """</p>
        </div>
        
        <div class="content">
            <!-- Ticket Information Section -->
            <div class="section">
                <h2>Ticket Information</h2>
                <div class="ticket-info">
                    <div class="info-card">
                        <h3>Ticket Details</h3>
                        <p><strong>Name:</strong> """ + str(safe_get(ticket_info, 'name')) + """</p>
                        <p><strong>ID:</strong> """ + str(safe_get(ticket_info, 'id')) + """</p>
                        <p><strong>Priority:</strong> """ + str(safe_get(ticket_info, 'priority')) + """</p>
                        <p><strong>Due Date:</strong> """ + str(safe_get(ticket_info, 'due_date')) + """</p>
                    </div>
                    
                    <div class="info-card">
                        <h3>Description</h3>
                        <p>""" + str(safe_get(ticket_info, 'description')) + """</p>
                    </div>
                    
                    <div class="info-card">
                        <h3>Required Skills</h3>
                        <ul class="skills-list">
                            """ + create_list_items(ticket_info.get('required_skills', [])) + """
                        </ul>
                    </div>
                    
                    <div class="info-card">
                        <h3>Suggested Employees</h3>
                        <ul class="skills-list">
                            """ + create_list_items(ticket_info.get('suggested_employees', [])) + """
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- Recommendation Section -->
            <div class="section">
                <h2>Final Recommendation</h2>
                """
    
    # Add recommendation box based on success status
    if success:
        if recommendation.get('recommended_employee') != 'PARSING_ERROR':
            html_content += """
                <div class="recommendation-box">
                    <p class='status-success'>Analysis Successful</p>
                    <div class="employee-name">Recommended: """ + str(recommendation.get('recommended_employee', 'N/A')) + """</div>
                    <div class="confidence-score">""" + str(recommendation.get('confidence_score', 0.0)) + """</div>
                    <p>Confidence Score</p>
                </div>"""
            
            # Add analysis details if available
            if 'reasoning' in recommendation:
                reasoning = recommendation['reasoning']
                html_content += """
                <div class="analysis-grid">
                    <div class="analysis-card">
                        <h4>Primary Factors</h4>
                        <ul class="factors-list">
                            """ + create_list_items(reasoning.get('primary_factors', [])) + """
                        </ul>
                    </div>
                    
                    <div class="analysis-card">
                        <h4>Skill Analysis</h4>
                        <p>""" + str(reasoning.get('skill_analysis', 'N/A')) + """</p>
                    </div>
                    
                    <div class="analysis-card">
                        <h4>Availability Analysis</h4>
                        <p>""" + str(reasoning.get('availability_analysis', 'N/A')) + """</p>
                    </div>
                    
                    <div class="analysis-card">
                        <h4>Risk Assessment</h4>
                        <p>""" + str(reasoning.get('risk_assessment', 'N/A')) + """</p>
                    </div>
                    
                    <div class="analysis-card">
                        <h4>Alternative Options</h4>
                        <p>""" + str(reasoning.get('alternative_options', 'N/A')) + """</p>
                    </div>
                </div>"""
            
            # Add assignment recommendations if available
            if 'assignment_recommendations' in recommendation:
                assign_rec = recommendation['assignment_recommendations']
                html_content += """
            </div>
            
            <div class="section">
                <h2>Assignment Recommendations</h2>
                <div class="analysis-grid">
                    <div class="analysis-card">
                        <h4>Estimated Completion</h4>
                        <p>""" + str(assign_rec.get('estimated_completion_time', 'N/A')) + """</p>
                    </div>
                    
                    <div class="analysis-card">
                        <h4>Success Probability</h4>
                        <p>""" + str(assign_rec.get('success_probability', 'N/A')) + """</p>
                    </div>
                    
                    <div class="analysis-card">
                        <h4>Monitoring Points</h4>
                        <ul class="factors-list">
                            """ + create_list_items(assign_rec.get('monitoring_points', [])) + """
                        </ul>
                    </div>
                    
                    <div class="analysis-card">
                        <h4>Support Needed</h4>
                        <ul class="factors-list">
                            """ + create_list_items(assign_rec.get('support_needed', [])) + """
                        </ul>
                    </div>
                </div>"""
        else:
            html_content += """
                <div class="recommendation-box error">
                    <p class='status-error'>Parsing Error</p>
                    <div class="employee-name">Error: """ + str(final_recommendation.get('error', 'Unknown Error')) + """</div>
                </div>"""
    else:
        html_content += """
                <div class="recommendation-box error">
                    <p class='status-error'>Analysis Failed</p>
                    <div class="employee-name">Error: """ + str(final_recommendation.get('error', 'Unknown Error')) + """</div>
                </div>"""
    
    # Add raw data section and footer
    html_content += """
            </div>
            
            <!-- Raw Data Section -->
            <div class="section">
                <h2>Raw Analysis Data</h2>
                <div class="json-view">""" + json.dumps(final_recommendation, indent=2, ensure_ascii=False) + """</div>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by WorkWise AI Employee Assignment System</p>
            <p>Report ID: """ + str(safe_get(ticket_info, 'id')) + """ | Timestamp: """ + timestamp + """</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def save_html_report(html_content: str, filename: str = None, custom_path: str = None) -> str:
    """
    Save HTML content to file
    
    Args:
        html_content: HTML string to save
        filename: Optional filename, if not provided, generates timestamp-based name
        custom_path: Optional custom directory path to save the file
        
    Returns:
        Full path of saved report
    """
    # Set the default path to your desired location
    if custom_path is None:
        custom_path = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec"
    
    # Create directory if it doesn't exist
    Path(custom_path).mkdir(parents=True, exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        filename = "summary_report.html"  # Use your desired filename
    
    # Create full file path
    full_path = os.path.join(custom_path, filename)
    
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML report saved as: {full_path}")
        return full_path
    except Exception as e:
        print(f"Error saving HTML report: {e}")
        return None

def save_html_report_fixed_location(html_content: str) -> str:
    """
    Save HTML content to the specific location you want
    
    Args:
        html_content: HTML string to save
        
    Returns:
        Full path of saved report
    """
    # Your specific path
    file_path = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec\summary_report.html"
    
    # Create directory if it doesn't exist
    directory = os.path.dirname(file_path)
    Path(directory).mkdir(parents=True, exist_ok=True)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML report saved as: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error saving HTML report: {e}")
        return None