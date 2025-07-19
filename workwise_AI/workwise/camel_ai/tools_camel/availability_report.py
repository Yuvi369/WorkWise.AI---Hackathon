import os
from datetime import datetime
from typing import List, Dict, Any

def generate_html_report(results: List[Dict], output_file: str = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec\availability_agent_report.html"):
   
    if not results:
        print("❌ No results to generate report")
        return None
    
    # Count statistics
    total_employees = len(results)
    available_count = sum(1 for r in results if r.get("status") == "available")
    unavailable_count = sum(1 for r in results if r.get("status") in ["unavailable", "error"])
    
    # Get current timestamp
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Employee Availability Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #0d1117;
                min-height: 100vh;
                padding: 20px;
                position: relative;
                overflow-x: hidden;
            }}
            body::before {{
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
                            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%),
                            radial-gradient(circle at 40% 80%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
                pointer-events: none;
                z-index: 0;
            }}
            .container {{
                max-width: 800px;
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin: 0 auto;
                position: relative;
                z-index: 1;
            }}
            .header {{
                text-align: center;
                color: #58a6ff;
                margin-bottom: 20px;
                padding: 15px;
            }}
            .header h1 {{
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 5px;
                text-shadow: 0 1px 2px rgba(0,0,0,0.5);
            }}
            .header p {{
                font-size: 0.9rem;
                opacity: 0.8;
                margin-bottom: 10px;
                color: #c9d1d9;
            }}
            .close-btn {{
                position: absolute;
                top: 15px;
                right: 20px;
                width: 30px;
                height: 30px;
                background: #ff4757;
                border-radius: 50%;
                border: none;
                color: white;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                box-shadow: 0 1px 4px rgba(255, 71, 87, 0.4);
            }}
            .close-btn:hover {{
                background: #ff3742;
                transform: scale(1.1);
                box-shadow: 0 2px 6px rgba(255, 71, 87, 0.6);
            }}
            .employee-cards {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 20px;
            }}
            .employee-card {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(8px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 15px;
                color: white;
                transition: all 0.3s ease;
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }}
            .employee-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }}
            .employee-card:hover::before {{
                opacity: 1;
            }}
            .employee-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 20px rgba(0,0,0,0.3);
                border-color: rgba(255, 255, 255, 0.2);
            }}
            .employee-card.available {{
                border-left: 3px solid #2ed573;
            }}
            .employee-card.unavailable {{
                border-left: 3px solid #ff4757;
            }}
            .status-badge {{
                position: absolute;
                top: 15px;
                right: 15px;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 10px;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .badge-available {{
                background: linear-gradient(135deg, #2ed573 0%, #17c0eb 100%);
                color: white;
            }}
            .badge-unavailable {{
                background: linear-gradient(135deg, #ff4757 0%, #ff3838 100%);
                color: white;
            }}
            .employee-name {{
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 10px;
                color: #fff;
            }}
            .employee-details {{
                display: flex;
                flex-direction: column;
                gap: 10px;
            }}
            .detail-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .detail-label {{
                font-weight: 500;
                color: rgba(255, 255, 255, 0.6);
                font-size: 0.8rem;
            }}
            .detail-value {{
                font-weight: 400;
                color: white;
                font-size: 0.9rem;
            }}
            .summary-section {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(8px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 15px;
                text-align: center;
                color: white;
                margin-top: 20px;
            }}
            .summary-title {{
                font-size: 1.5rem;
                font-weight: 800;
                margin-bottom: 15px;
                color: #58a6ff;
            }}
            .summary-stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 20px;
            }}
            .stat-item {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 5px;
            }}
            .stat-number {{
                font-size: 1.5rem;
                font-weight: 700;
                line-height: 1;
            }}
            .stat-number.total {{
                color: #70a1ff;
            }}
            .stat-number.available {{
                color: #2ed573;
            }}
            .stat-number.unavailable {{
                color: #ff4757;
            }}
            .stat-label {{
                font-size: 0.9rem;
                font-weight: 500;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                color: rgba(255, 255, 255, 0.6);
            }}
            .message-section {{
                margin-top: 10px;
                padding: 10px;
                background: rgba(255, 255, 255, 0.03);
                border-radius: 8px;
                border-left: 2px solid #70a1ff;
            }}
            .message-text {{
                font-size: 0.8rem;
                color: rgba(255, 255, 255, 0.8);
                line-height: 1.3;
            }}
            @media (max-width: 768px) {{
                .employee-cards {{
                    grid-template-columns: 1fr;
                }}
                .header h1 {{
                    font-size: 2rem;
                }}
                .summary-stats {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <button class="close-btn" onclick="closeReport()">×</button>
        <div class="container">
            <div class="header">
                <h1>🏢 Employee Availability Report</h1>
                <div style="font-size: 0.9rem; opacity: 0.8;">Generated on: {report_time}</div>
            </div>
            <div class="employee-cards">
    """
    
    # Generate employee cards and details for showDetails
    employee_details = {}
    for result in results:
        employee_name = result.get("employee_name", "Unknown")
        status = result.get("status", "unknown")
        message = result.get("message", "No message available")
        
        # Map status to template terms
        card_class = "available" if status == "available" else "unavailable"
        badge_class = "badge-available" if status == "available" else "badge-unavailable"
        detail_value = "Ready for Assignment" if status == "available" else "On Leave" if status == "unavailable" else "Error"
        
        # Generate employee ID for showDetails
        employee_id = employee_name.lower().replace(" ", "_")
        
        # Store details for JavaScript
        employee_details[employee_id] = f"{employee_name} - {detail_value}: {message}"
        
        html_content += f"""
                <div class="employee-card {card_class}" onclick="showDetails('{employee_id}')">
                    <div class="status-badge {badge_class}">{card_class.capitalize()}</div>
                    <div class="employee-name">{employee_name}</div>
                    <div class="employee-details">
                        <div class="detail-row">
                            <span class="detail-label">Availability:</span>
                            <span class="detail-value">{detail_value}</span>
                        </div>
                    </div>
                    <div class="message-section">
                        <div class="message-text">{message}</div>
                    </div>
                </div>
        """
    
    # Close employee-cards and add summary
    html_content += f"""
            </div>
            <div class="summary-section">
                <div class="summary-title">Assignment Summary</div>
                <div class="summary-stats">
                    <div class="stat-item">
                        <div class="stat-number total">{total_employees}</div>
                        <div class="stat-label">Total Employees</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number available">{available_count}</div>
                        <div class="stat-label">Available</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number unavailable">{unavailable_count}</div>
                        <div class="stat-label">Unavailable</div>
                    </div>
                </div>
            </div>
        </div>
    """
    
    # Add JavaScript
    html_content += """
        <script>
            function showDetails(employeeId) {
                const employees = {
    """
    for emp_id, details in employee_details.items():
        html_content += f'                "{emp_id}": "{details}",\n'
    
    html_content += """
                };
                alert(employees[employeeId] || "Employee details not found");
            }
            
            function closeReport() {
                if(confirm("Are you sure you want to close this report?")) {
                    window.close();
                }
            }
            
            window.addEventListener('load', function() {
                const cards = document.querySelectorAll('.employee-card');
                cards.forEach((card, index) => {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.transition = 'all 0.6s ease';
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, index * 200);
                });
            });
        </script>
    </body>
    </html>
    """
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ HTML report generated: {output_file}")
        return os.path.abspath(output_file)
    except Exception as e:
        print(f"❌ Error generating HTML report: {e}")
        return None

# Example usage
if __name__ == "__main__":
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
    
    report_path = generate_html_report(sample_results)
    print(f"Report generated: {report_path}")