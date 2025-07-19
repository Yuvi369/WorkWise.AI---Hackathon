import os
from datetime import datetime

def generate_html_report(result_data, output_file= r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec\similarity_agent_report.html"):
    """
    Generate an HTML report from the ticket assignment result dictionary.
    
    Args:
        result_data (dict): Dictionary containing ticket assignment results with keys:
            - current_ticket: dict with 'name', 'description', 'skills_required'
            - top_matches: list of dicts with 'employee_name', 'similarity_score', 'ticket_count'
            - all_employees_count: int
            - recommendations: list of strings
        output_file (str): Output HTML file name
    
    Returns:
        str: Path to the generated HTML file
    """
    
    # Extract data from dictionary
    current_ticket = result_data.get('current_ticket', {})
    ticket_name = current_ticket.get('name', 'Unknown Ticket')
    ticket_description = current_ticket.get('description', 'No description available')
    skills_required = current_ticket.get('skills_required', [])
    
    top_matches = result_data.get('top_matches', [])
    all_employees_count = result_data.get('all_employees_count', 0)
    recommendations = result_data.get('recommendations', [])
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Build skills HTML
    skills_html = ""
    for skill in skills_required:
        skills_html += f'<span class="skill-tag">{skill}</span>'
    
    # Build matches HTML
    matches_html = ""
    for match in top_matches:
        employee_name = match.get('employee_name', 'Unknown')
        similarity_score = match.get('similarity_score', 0)
        ticket_count = match.get('ticket_count', 0)
        
        similarity_percent = similarity_score * 100
        similarity_color = "rgba(255,255,255,0.9)" if similarity_percent >= 5 else "rgba(255,255,255,0.7)"
        
        matches_html += f"""
        <div class="match-item">
            <div class="match-info">
                <span class="emoji">👤</span>
                <span class="match-name">{employee_name}</span>
            </div>
            <div class="match-stats">
                <div class="similarity-score" style="color: {similarity_color};">{similarity_percent:.1f}%</div>
                <div class="past-tickets">{ticket_count} past tickets</div>
            </div>
        </div>
        """
    
    # Build recommendations HTML
    recommendations_html = ""
    for rec in recommendations:
        if "❌" in rec:
            icon = "❌"
            rec_class = "warning"
        elif "💼" in rec:
            icon = "💼"
            rec_class = "suggestion"
        else:
            icon = "💡"
            rec_class = "info"
        
        rec_text = rec.replace("❌", "").replace("💼", "").replace("💡", "").strip()
        recommendations_html += f"""
        <div class="recommendation-item {rec_class}">
            <span class="emoji">{icon}</span>
            <span class="rec-text">{rec_text}</span>
        </div>
        """
    
    # Calculate statistics
    best_match_score = max([match.get('similarity_score', 0) * 100 for match in top_matches], default=0)
    total_experience = sum([match.get('ticket_count', 0) for match in top_matches])
    
    # HTML template
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ticket Assignment Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        
        .timestamp {{
            opacity: 0.9;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 30px;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}
        
        .current-ticket {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }}
        
        .matches-section {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }}
        
        .recommendations-section {{
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
            color: white;
        }}
        
        .section h2 {{
            margin-top: 0;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.8em;
        }}
        
        .emoji {{
            font-size: 1.2em;
        }}
        
        .ticket-title {{
            font-size: 1.3em;
            font-weight: 600;
            background: rgba(255,255,255,0.2);
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }}
        
        .ticket-description {{
            font-size: 1.1em;
            background: rgba(255,255,255,0.15);
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            line-height: 1.7;
        }}
        
        .skills-container {{
            margin-top: 15px;
        }}
        
        .skills-label {{
            font-weight: 600;
            margin-bottom: 10px;
            display: block;
        }}
        
        .skill-tag {{
            display: inline-block;
            background: rgba(255,255,255,0.25);
            padding: 5px 12px;
            border-radius: 20px;
            margin: 3px;
            font-size: 0.9em;
            font-weight: 500;
        }}
        
        .match-item {{
            background: rgba(255,255,255,0.15);
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s ease;
        }}
        
        .match-item:hover {{
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
        }}
        
        .match-info {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .match-name {{
            font-weight: 600;
            font-size: 1.1em;
        }}
        
        .match-stats {{
            text-align: right;
        }}
        
        .similarity-score {{
            font-size: 1.2em;
            font-weight: 700;
        }}
        
        .past-tickets {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        .recommendation-item {{
            background: rgba(255,255,255,0.15);
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
        }}
        
        .recommendation-item:hover {{
            background: rgba(255,255,255,0.25);
            transform: translateY(-2px);
        }}
        
        .recommendation-item.warning {{
            border-left: 4px solid #ff6b6b;
        }}
        
        .recommendation-item.suggestion {{
            border-left: 4px solid #51cf66;
        }}
        
        .recommendation-item.info {{
            border-left: 4px solid #339af0;
        }}
        
        .rec-text {{
            font-size: 1.1em;
            flex: 1;
        }}
        
        .stats-summary {{
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: 700;
            display: block;
        }}
        
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        
        @media (max-width: 768px) {{
            .match-item {{
                flex-direction: column;
                gap: 10px;
                text-align: center;
            }}
            
            .recommendation-item {{
                flex-direction: column;
                text-align: center;
            }}
            
            .stats-summary {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Ticket Assignment Report</h1>
            <div class="timestamp">Generated on {timestamp}</div>
        </div>
        
        <div class="content">
            <div class="section current-ticket">
                <h2><span class="emoji">📋</span> Current Ticket</h2>
                <div class="ticket-title">{ticket_name}</div>
                <div class="ticket-description">{ticket_description}</div>
                <div class="skills-container">
                    <span class="skills-label">Required Skills:</span>
                    {skills_html}
                </div>
            </div>
            
            <div class="section matches-section">
                <h2><span class="emoji">🎯</span> Top Matches</h2>
                <div class="stats-summary">
                    <div class="stat-item">
                        <span class="stat-number">{len(top_matches)}</span>
                        <span class="stat-label">Candidates</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">{best_match_score:.1f}%</span>
                        <span class="stat-label">Best Match</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">{total_experience}</span>
                        <span class="stat-label">Total Experience</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">{all_employees_count}</span>
                        <span class="stat-label">Total Employees</span>
                    </div>
                </div>
                {matches_html}
            </div>
            
            <div class="section recommendations-section">
                <h2><span class="emoji">💡</span> Recommendations</h2>
                {recommendations_html}
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return os.path.abspath(output_file)

# Example usage:
if __name__ == "__main__":
    # Example result data
    sample_result = {
        'current_ticket': {
            'name': 'Database Backup Automation',
            'description': 'Set up automated daily backups for the production database to an S3 bucket.',
            'skills_required': ['AWS', 'S3', 'cloud computing', 'storage services', 'database management']
        },
        'top_matches': [
            {'employee_name': 'Mark Jenkins', 'similarity_score': 0.082, 'ticket_count': 11},
            {'employee_name': 'Angel Mason', 'similarity_score': 0.026, 'ticket_count': 6},
            {'employee_name': 'Shirley Walker', 'similarity_score': 0.021, 'ticket_count': 9},
            {'employee_name': 'Kenneth Simpson', 'similarity_score': 0.016, 'ticket_count': 3},
            {'employee_name': 'Lauren Ryan', 'similarity_score': 0.016, 'ticket_count': 2}
        ],
        'all_employees_count': 13,
        'recommendations': [
            '❌ No employees found with strong similarity to this ticket',
            '💼 Consider experienced employees: Mark Jenkins'
        ]
    }
    
    # Generate report
    report_path = generate_html_report(sample_result)
    print(f"Report generated: {report_path}")