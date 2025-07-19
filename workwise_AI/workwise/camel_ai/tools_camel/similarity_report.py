import os
from datetime import datetime

def generate_html_report(result_data, output_file= r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec\similarity_agent_report.html"):
    """
    Generate an HTML report from the ticket assignment result dictionary with minimized font sizes and box dimensions.
    
    Args:
        result_data (dict): Dictionary containing ticket assignment results with keys:
            - current_ticket: dict with 'name', 'description', 'skills_required'
            - top_matches: list of dicts with 'employee_name', 'similarity_score', 'ticket_count'
            - all_employees_count: int
            - recommendations: list of strings
        output_file (str): Output HTML file name (default: public/generat.html)
    
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
        skills_html += f'<div class="skill-tag">{skill}</div>'
    
    # Build matches HTML
    matches_html = ""
    for match in top_matches:
        employee_name = match.get('employee_name', 'Unknown')
        similarity_score = match.get('similarity_score', 0)
        ticket_count = match.get('ticket_count', 0)
        
        similarity_percent = similarity_score * 100
        initial = employee_name.split()[0][0] + (employee_name.split()[1][0] if len(employee_name.split()) > 1 else '')
        
        matches_html += f"""
        <div class="match-item">
            <div class="match-info">
                <div class="match-avatar">{initial}</div>
                <div class="match-name">{employee_name}</div>
            </div>
            <div class="match-stats">
                <div class="similarity-score">{similarity_percent:.1f}%</div>
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
            <div class="rec-icon">{icon}</div>
            <div class="rec-text">{rec_text}</div>
        </div>
        """
    
    # Calculate statistics
    best_match_score = max([match.get('similarity_score', 0) * 100 for match in top_matches], default=0)
    total_experience = sum([match.get('ticket_count', 0) for match in top_matches])
    
    # HTML template with minimized font sizes and box dimensions
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ticket Assignment Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0a0a;
            color: #ffffff;
            line-height: 1.6;
            overflow-x: hidden;
        }}

        .background-pattern {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 20%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.2) 0%, transparent 50%);
            z-index: -1;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 16px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 24px;
            position: relative;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%);
            transform: translate(-50%, -50%);
            z-index: -1;
            animation: pulse 4s ease-in-out infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.3; }}
            50% {{ transform: translate(-50%, -50%) scale(1.2); opacity: 0.6; }}
        }}

        .header h1 {{
            font-size: 1.75rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }}

        .timestamp {{
            font-size: 0.75rem;
            color: #a1a1aa;
            font-weight: 500;
        }}

        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}

        .section {{
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border-radius: 16px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .section::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.8), transparent);
            transform: translateX(-100%);
            transition: transform 0.6s ease;
        }}

        .section:hover::before {{
            transform: translateX(100%);
        }}

        .section:hover {{
            transform: translateY(-6px);
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(139, 92, 246, 0.3);
            box-shadow: 0 20px 40px rgba(139, 92, 246, 0.15);
        }}

        .full-width {{
            grid-column: 1 / -1;
        }}

        .section-title {{
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .section-icon {{
            width: 28px;
            height: 28px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.875rem;
        }}

        .ticket-info {{
            margin-bottom: 16px;
        }}

        .ticket-title {{
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: #f3f4f6;
        }}

        .ticket-description {{
            font-size: 0.875rem;
            color: #d1d5db;
            margin-bottom: 16px;
            line-height: 1.7;
        }}

        .skills-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 12px;
        }}

        .skill-tag {{
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
            border: 1px solid rgba(139, 92, 246, 0.3);
            color: #e2e8f0;
            padding: 4px 10px;
            border-radius: 16px;
            font-size: 0.7rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }}

        .skill-tag:hover {{
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(59, 130, 246, 0.3) 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(139, 92, 246, 0.3);
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }}

        .stat-card:hover {{
            background: rgba(255, 255, 255, 0.08);
            transform: translateY(-4px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }}

        .stat-number {{
            font-size: 1.25rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            display: block;
            margin-bottom: 6px;
        }}

        .stat-label {{
            font-size: 0.7rem;
            color: #9ca3af;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .match-item {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}

        .match-item::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.1), transparent);
            transition: left 0.6s ease;
        }}

        .match-item:hover::before {{
            left: 100%;
        }}

        .match-item:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(139, 92, 246, 0.4);
            transform: translateX(6px);
            box-shadow: 0 6px 24px rgba(139, 92, 246, 0.2);
        }}

        .match-info {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .match-avatar {{
            width: 36px;
            height: 36px;
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            color: white;
            font-weight: 600;
        }}

        .match-name {{
            font-size: 0.875rem;
            font-weight: 600;
            color: #f3f4f6;
        }}

        .similarity-score {{
            font-size: 1rem;
            font-weight: 800;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .past-tickets {{
            font-size: 0.7rem;
            color: #9ca3af;
            margin-top: 4px;
        }}

        .recommendation-item {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}

        .recommendation-item::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(239, 68, 68, 0.1), transparent);
            transition: left 0.6s ease;
        }}

        .recommendation-item.warning::before {{
            background: linear-gradient(90deg, transparent, rgba(239, 68, 68, 0.1), transparent);
        }}

        .recommendation-item.suggestion::before {{
            background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
        }}

        .recommendation-item:hover::before {{
            left: 100%;
        }}

        .recommendation-item:hover {{
            background: rgba(255, 255, 255, 0.08);
            transform: translateX(6px);
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
        }}

        .recommendation-item.warning {{
            border-left: 3px solid #ef4444;
        }}

        .recommendation-item.suggestion {{
            border-left: 3px solid #3b82f6;
        }}

        .rec-icon {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            flex-shrink: 0;
        }}

        .recommendation-item.warning .rec-icon {{
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%);
        }}

        .recommendation-item.suggestion .rec-icon {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.2) 100%);
        }}

        .rec-text {{
            font-size: 0.75rem;
            color: #e2e8f0;
            font-weight: 500;
        }}

        @media (max-width: 768px) {{
            .grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 1.25rem;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .match-item,
            .recommendation-item {{
                flex-direction: column;
                text-align: center;
                gap: 10px;
            }}
            
            .match-stats {{
                text-align: center;
            }}
        }}

        @media (max-width: 480px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .container {{
                padding: 12px;
            }}
            
            .section {{
                padding: 16px;
            }}
        }}

        .floating-elements {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }}

        .floating-element {{
            position: absolute;
            background: rgba(139, 92, 246, 0.1);
            border-radius: 50%;
            animation: float 20s infinite linear;
        }}

        .floating-element:nth-child(1) {{ left: 10%; width: 15px; height: 15px; animation-delay: 0s; }}
        .floating-element:nth-child(2) {{ left: 20%; width: 12px; height: 12px; animation-delay: 2s; }}
        .floating-element:nth-child(3) {{ left: 30%; width: 18px; height: 18px; animation-delay: 4s; }}
        .floating-element:nth-child(4) {{ left: 40%; width: 14px; height: 14px; animation-delay: 6s; }}
        .floating-element:nth-child(5) {{ left: 50%; width: 16px; height: 16px; animation-delay: 8s; }}
        .floating-element:nth-child(6) {{ left: 60%; width: 13px; height: 13px; animation-delay: 10s; }}
        .floating-element:nth-child(7) {{ left: 70%; width: 17px; height: 17px; animation-delay: 12s; }}
        .floating-element:nth-child(8) {{ left: 80%; width: 15px; height: 15px; animation-delay: 14s; }}
        .floating-element:nth-child(9) {{ left: 90%; width: 16px; height: 16px; animation-delay: 16s; }}

        @keyframes float {{
            0% {{ transform: translateY(100vh) rotate(0deg); }}
            100% {{ transform: translateY(-100px) rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div class="background-pattern"></div>
    <div class="floating-elements">
        <div class="floating-element"></div>
        <div class="floating-element"></div>
        <div class="floating-element"></div>
        <div class="floating-element"></div>
        <div class="floating-element"></div>
        <div class="floating-element"></div>
        <div class="floating-element"></div>
        <div class="floating-element"></div>
        <div class="floating-element"></div>
    </div>

    <div class="container">
        <div class="header">
            <h1>Ticket Assignment Report</h1>
            <div class="timestamp">Generated on {timestamp}</div>
        </div>

        <div class="grid">
            <div class="section">
                <div class="section-title">
                    <div class="section-icon">📋</div>
                    Current Ticket
                </div>
                <div class="ticket-info">
                    <div class="ticket-title">{ticket_name}</div>
                    <div class="ticket-description">{ticket_description}</div>
                    <div class="skills-container">
                        {skills_html}
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">
                    <div class="section-icon">📊</div>
                    Quick Stats
                </div>
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">{len(top_matches)}</span>
                        <span class="stat-label">Candidates</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{best_match_score:.1f}%</span>
                        <span class="stat-label">Best Match</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{total_experience}</span>
                        <span class="stat-label">Experience</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{all_employees_count}</span>
                        <span class="stat-label">Employees</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="section full-width">
            <div class="section-title">
                <div class="section-icon">🎯</div>
                Top Matches
            </div>
            {matches_html}
        </div>

        <div class="section full-width">
            <div class="section-title">
                <div class="section-icon">💡</div>
                Recommendations
            </div>
            {recommendations_html}
        </div>
    </div>
</body>
</html>
"""
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
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