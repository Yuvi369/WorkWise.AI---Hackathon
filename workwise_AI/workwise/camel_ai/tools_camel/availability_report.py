import os
from datetime import datetime


def generate_html_report(results, output_file=r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec\availability_agent_report.html"):
    """
    Generates an HTML report for employee availability check results.
    
    Args:
        results (list): List of dictionaries containing employee availability data
        output_file (str): Name of the output HTML file
    
    Returns:
        str: Path to the generated HTML file
    """
    
    # Count statistics
    total_employees = len(results)
    available_count = sum(1 for r in results if r.get("status") == "available")
    unavailable_count = sum(1 for r in results if r.get("status") == "unavailable")
    error_count = sum(1 for r in results if r.get("status") == "error")
    
    # Get current timestamp
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Employee Availability Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .header {{
                text-align: center;
                color: #333;
                border-bottom: 2px solid #007bff;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .stats {{
                display: flex;
                justify-content: space-around;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }}
            .stat-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                min-width: 150px;
                margin: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .stat-number {{
                font-size: 2em;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .stat-label {{
                font-size: 0.9em;
                opacity: 0.9;
            }}
            .available {{
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            }}
            .unavailable {{
                background: linear-gradient(135deg, #ee5a24 0%, #ffc048 100%);
            }}
            .error {{
                background: linear-gradient(135deg, #c0392b 0%, #f39c12 100%);
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #007bff;
                color: white;
                font-weight: bold;
            }}
            tr:hover {{
                background-color: #f8f9fa;
            }}
            .status-badge {{
                padding: 5px 10px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: bold;
                text-transform: uppercase;
            }}
            .badge-available {{
                background-color: #28a745;
                color: white;
            }}
            .badge-unavailable {{
                background-color: #dc3545;
                color: white;
            }}
            .badge-error {{
                background-color: #6c757d;
                color: white;
            }}
            .footer {{
                margin-top: 30px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
                border-top: 1px solid #eee;
                padding-top: 20px;
            }}
            .message {{
                max-width: 300px;
                word-wrap: break-word;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏢 Employee Availability Report</h1>
                <p>Generated on: {report_time}</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{total_employees}</div>
                    <div class="stat-label">Total Employees</div>
                </div>
                <div class="stat-card available">
                    <div class="stat-number">{available_count}</div>
                    <div class="stat-label">Available</div>
                </div>
                <div class="stat-card unavailable">
                    <div class="stat-number">{unavailable_count}</div>
                    <div class="stat-label">Unavailable</div>
                </div>
                <div class="stat-card error">
                    <div class="stat-number">{error_count}</div>
                    <div class="stat-label">Errors</div>
                </div>
            </div>
            
            <h2>📊 Detailed Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Employee Name</th>
                        <th>Status</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Add table rows
    for result in results:
        status = result.get("status", "unknown")
        employee_name = result.get("employee_name", "Unknown")
        message = result.get("message", "No message available")
        
        # Determine badge class
        if status == "available":
            badge_class = "badge-available"
        elif status == "unavailable":
            badge_class = "badge-unavailable"
        else:
            badge_class = "badge-error"
        
        html_content += f"""
                    <tr>
                        <td><strong>{employee_name}</strong></td>
                        <td><span class="status-badge {badge_class}">{status}</span></td>
                        <td class="message">{message}</td>
                    </tr>
        """
    
    # Close HTML
    html_content += f"""
                </tbody>
            </table>
            
            <div class="footer">
                <p>📋 Report generated by WorkWise AI Employee Availability System</p>
                <p>For any queries, please contact the HR department</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Write to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        full_path = os.path.abspath(output_file)
        print(f"HTML report generated successfully: {full_path}")
        return full_path
        
    except Exception as e:
        print(f"Error generating HTML report: {str(e)}")
        return None


# Example usage
if __name__ == "__main__":
    # Sample results for testing
    sample_results = [
        {
            "employee_name": "Mark Jenkins",
            "status": "available",
            "message": "Employee available for assigning tickets"
        },
        {
            "employee_name": "Kenneth Simpson",
            "status": "unavailable",
            "message": "Selected employee is not available till 25-07-2025"
        },
        {
            "employee_name": "Anthony Wright",
            "status": "error",
            "message": "Employee 'Anthony Wright' not found in employee database"
        }
    ]
    
    # Generate report
    generate_html_report(sample_results, "sample_employee_report.html")