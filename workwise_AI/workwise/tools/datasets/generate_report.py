import json
import re

def generate_html_report(employee_data, output_file: str = r"workwise_AI\workwise\tools\reports\policy_agent_report.html"):
    """
    Generate an HTML report with employee cards showing assignment status.
    
    Args:
        employee_data (list): List of employee dictionaries
        output_file (str): Output HTML file name
    """
    
    def extract_decision_and_flag(rag_response):
        """Extract the decision text and flag from the RAG response"""
        try:
            # Find JSON in the response
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', rag_response, re.DOTALL)
            if json_match:
                json_data = json.loads(json_match.group(1))
                decision = json_data.get('decision', 'No decision found')
                flag = json_data.get('flag', 0)
                return decision, flag
            else:
                return 'No decision found', 0
        except:
            return 'Error parsing decision', 0
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Employee Assignment Report</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                color: white;
                margin-bottom: 30px;
            }
            
            .header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .cards-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .employee-card {
                background: white;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .employee-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.2);
            }
            
            .status-flag {
                position: absolute;
                top: 0;
                right: 0;
                padding: 8px 15px;
                color: white;
                font-weight: bold;
                font-size: 0.9em;
                border-radius: 0 15px 0 15px;
            }
            
            .status-accepted {
                background: linear-gradient(135deg, #4CAF50, #45a049);
            }
            
            .status-failed {
                background: linear-gradient(135deg, #f44336, #da190b);
            }
            
            .employee-info h3 {
                color: #333;
                margin-bottom: 10px;
                font-size: 1.3em;
            }
            
            .employee-details {
                color: #666;
                line-height: 1.6;
            }
            
            .employee-details span {
                display: block;
                margin-bottom: 5px;
            }
            
            .detail-label {
                font-weight: 600;
                color: #444;
            }
            
            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.5);
                backdrop-filter: blur(5px);
            }
            
            .modal-content {
                background-color: white;
                margin: 5% auto;
                padding: 30px;
                border-radius: 20px;
                width: 90%;
                max-width: 600px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                position: relative;
                max-height: 80vh;
                overflow-y: auto;
            }
            
            .close {
                position: absolute;
                right: 20px;
                top: 20px;
                font-size: 30px;
                font-weight: bold;
                cursor: pointer;
                color: #aaa;
                transition: color 0.3s ease;
            }
            
            .close:hover {
                color: #333;
            }
            
            .modal-header {
                margin-bottom: 25px;
                padding-bottom: 15px;
                border-bottom: 2px solid #eee;
            }
            
            .modal-title {
                color: #333;
                font-size: 1.8em;
                margin-bottom: 10px;
            }
            
            .modal-info {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            
            .modal-info span {
                display: block;
                margin-bottom: 8px;
                font-size: 1.1em;
            }
            
            .decision-section {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 20px;
                border-radius: 8px;
            }
            
            .decision-title {
                color: #856404;
                font-size: 1.2em;
                font-weight: 600;
                margin-bottom: 10px;
            }
            
            .decision-text {
                color: #533f03;
                line-height: 1.6;
                font-size: 1.05em;
            }
            
            .summary {
                background: white;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                text-align: center;
            }
            
            .summary h2 {
                color: #333;
                margin-bottom: 15px;
            }
            
            .summary-stats {
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
                gap: 20px;
            }
            
            .stat-item {
                flex: 1;
                min-width: 150px;
            }
            
            .stat-number {
                font-size: 2.5em;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .stat-accepted {
                color: #4CAF50;
            }
            
            .stat-failed {
                color: #f44336;
            }
            
            .stat-total {
                color: #2196F3;
            }
            
            .stat-label {
                color: #666;
                font-size: 1.1em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Employee Assignment Report</h1>
                <p>Click on any employee card to view detailed information</p>
            </div>
            
            <div class="cards-container">
    """
    
    # Generate cards for each employee
    accepted_count = 0
    failed_count = 0
    
    for i, employee in enumerate(employee_data):
        decision, flag = extract_decision_and_flag(employee['rag_response'])
        status = "accepted" if flag == 1 else "failed"
        status_text = "ACCEPTED" if flag == 1 else "FAILED"
        
        # Count for summary
        if flag == 1:
            accepted_count += 1
        else:
            failed_count += 1
        
        # Sanitize employee data to prevent XSS
        employee_name = employee['employee_name'].replace('<', '&lt;').replace('>', '&gt;')
        employee_designation = employee['employee_designation'].replace('<', '&lt;').replace('>', '&gt;')
        employee_department = employee['employee_department'].replace('<', '&lt;').replace('>', '&gt;')
        employee_availability = employee['employee_availability'].replace('<', '&lt;').replace('>', '&gt;')
        
        html_content += f"""
                <div class="employee-card" onclick="openModal({i})">
                    <div class="status-flag status-{status}">{status_text}</div>
                    <div class="employee-info">
                        <h3>{employee_name}</h3>
                        <div class="employee-details">
                            <span><span class="detail-label">Designation:</span> {employee_designation}</span>
                            <span><span class="detail-label">Department:</span> {employee_department}</span>
                            <span><span class="detail-label">Availability:</span> {employee_availability}</span>
                        </div>
                    </div>
                </div>
        """
    
    # Calculate summary statistics
    total_employees = len(employee_data)
    
    html_content += f"""
            </div>
            
            <div class="summary">
                <h2>Assignment Summary</h2>
                <div class="summary-stats">
                    <div class="stat-item">
                        <div class="stat-number stat-total">{total_employees}</div>
                        <div class="stat-label">Total Employees</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number stat-accepted">{accepted_count}</div>
                        <div class="stat-label">Accepted</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number stat-failed">{failed_count}</div>
                        <div class="stat-label">Failed</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Modal for detailed information -->
        <div id="employeeModal" class="modal">
            <div class="modal-content">
                <span class="close" onclick="closeModal()">×</span>
                <div id="modalBody"></div>
            </div>
        </div>
        
        <script>
            const employeeData = {json.dumps(employee_data, ensure_ascii=False)};
            
            function extractDecision(ragResponse) {{
                try {{
                    const jsonMatch = ragResponse.match(/```json\\s*(\\{{.*?\\}})\\s*```/s);
                    if (jsonMatch) {{
                        const jsonData = JSON.parse(jsonMatch[1]);
                        return jsonData.decision || 'No decision found';
                    }}
                    return 'No decision found';
                }} catch (error) {{
                    return 'Error parsing decision';
                }}
            }}
            
            function openModal(index) {{
                const employee = employeeData[index];
                const decision = extractDecision(employee.rag_response);
                const status = employee.rag_flag === 1 ? 'accepted' : 'failed';
                const statusText = employee.rag_flag === 1 ? 'ACCEPTED' : 'FAILED';
                
                const modalBody = document.getElementById('modalBody');
                modalBody.innerHTML = `
                    <div class="modal-header">
                        <h2 class="modal-title">${{employee.employee_name}}</h2>
                        <div class="status-flag status-${{status}}">${{statusText}}</div>
                    </div>
                    
                    <div class="modal-info">
                        <span><span class="detail-label">Document Name:</span> ${{employee.pdf_name}}</span>
                        <span><span class="detail-label">Page Number:</span> ${{employee.pg_no}}</span>
                        <span><span class="detail-label">Designation:</span> ${{employee.employee_designation}}</span>
                        <span><span class="detail-label">Department:</span> ${{employee.employee_department}}</span>
                        <span><span class="detail-label">Availability:</span> ${{employee.employee_availability}}</span>
                    </div>
                    
                    <div class="decision-section">
                        <div class="decision-title">Decision Reason:</div>
                        <div class="decision-text">${{decision}}</div>
                    </div>
                `;
                
                document.getElementById('employeeModal').style.display = 'block';
            }}
            
            function closeModal() {{
                document.getElementById('employeeModal').style.display = 'none';
            }}
            
            // Close modal when clicking outside of it
            window.onclick = function(event) {{
                const modal = document.getElementById('employeeModal');
                if (event.target === modal) {{
                    closeModal();
                }}
            }}
            
            // Close modal with Escape key
            document.addEventListener('keydown', function(event) {{
                if (event.key === 'Escape') {{
                    closeModal();
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    # Write the HTML content to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML report generated successfully: {output_file}")
        return output_file
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        return None

# Example usage:
if __name__ == "__main__":
    # Corrected sample data
    sample_data = [
        {
            'employee_name': 'Alexander Rush', 
            'employee_designation': 'Intern', 
            'employee_department': 'Development', 
            'employee_availability': 'Available', 
            'pdf_name': 'Document_3.pdf', 
            'pg_no': 4, 
            'rag_flag': 0, 
            'rag_response': '```json\n{\n  "decision": "Employee cannot be assigned because Frontend interns may only fix internal UI bugs, not client-facing bugs.",\n  "flag": 0\n}\n```'
        }, 
        {
            'employee_name': 'Erik Ellison', 
            'employee_designation': 'Senior Developer', 
            'employee_department': 'Development', 
            'employee_availability': 'Available', 
            'pdf_name': 'Document_3.pdf', 
            'pg_no': 4, 
            'rag_flag': 1,  # Corrected to match rag_response flag
            'rag_response': '```json\n{\n  "decision": "Employee can be assigned as the ticket is a UI Production fix, the employee is a Senior Developer in the Development department, and is available.",\n  "flag": 1\n}\n```'
        }
    ]
    
    # Generate the report
    generate_html_report(sample_data)