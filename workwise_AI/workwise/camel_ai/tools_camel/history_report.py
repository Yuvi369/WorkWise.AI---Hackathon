import os
from typing import List, Dict, Any

def generate_html_report(results: List[Dict], required_skills: List[str], output_file: str = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec\history_report.html"):
    """
    Generate an HTML report with employee analysis results
    """
    if not results:
        print("❌ No results to generate report")
        return
    
    # Get score color based on value
    def get_score_color(score):
        if score >= 80:
            return "#10B981"  # Green
        elif score >= 60:
            return "#F59E0B"  # Yellow
        elif score >= 40:
            return "#EF4444"  # Red
        else:
            return "#6B7280"  # Gray
    
    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Employee Skills Analysis Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }}
            h1 {{
                text-align: center;
                color: #1f2937;
                margin-bottom: 10px;
                font-size: 2.5em;
            }}
            .subtitle {{
                text-align: center;
                color: #6b7280;
                margin-bottom: 30px;
                font-size: 1.1em;
            }}
            .required-skills {{
                background: #f8fafc;
                border-left: 4px solid #3b82f6;
                padding: 15px;
                margin-bottom: 30px;
                border-radius: 8px;
            }}
            .required-skills h3 {{
                color: #1f2937;
                margin-bottom: 10px;
            }}
            .skill-tag {{
                display: inline-block;
                background: #3b82f6;
                color: white;
                padding: 4px 12px;
                margin: 2px;
                border-radius: 20px;
                font-size: 0.9em;
            }}
            .employee-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 25px;
                margin-top: 20px;
            }}
            .employee-card {{
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                border: 1px solid #e5e7eb;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                cursor: pointer;
            }}
            .employee-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            }}
            .employee-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }}
            .employee-name {{
                font-size: 1.4em;
                font-weight: 600;
                color: #1f2937;
            }}
            .score-circle {{
                width: 60px;
                height: 60px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 1.1em;
                color: white;
                position: relative;
            }}
            .score-circle:hover::after {{
                content: attr(data-tooltip);
                position: absolute;
                bottom: -35px;
                left: 50%;
                transform: translateX(-50%);
                background: #1f2937;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 0.8em;
                white-space: nowrap;
                z-index: 10;
            }}
            .employee-stats {{
                display: flex;
                gap: 20px;
                margin-bottom: 15px;
                font-size: 0.9em;
                color: #6b7280;
            }}
            .stat {{
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            .skills-section {{
                margin-top: 15px;
            }}
            .skills-title {{
                font-size: 0.9em;
                font-weight: 600;
                margin-bottom: 8px;
                color: #374151;
            }}
            .matching-skills {{
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                margin-bottom: 10px;
            }}
            .matching-skill {{
                background: #10b981;
                color: white;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 0.8em;
            }}
            .missing-skills {{
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
            }}
            .missing-skill {{
                background: #ef4444;
                color: white;
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 0.8em;
            }}
            .recommendation {{
                margin-top: 15px;
                padding: 10px;
                border-radius: 8px;
                text-align: center;
                font-weight: 600;
            }}
            .strong-match {{ background: #d1fae5; color: #065f46; }}
            .good-match {{ background: #fef3c7; color: #92400e; }}
            .partial-match {{ background: #fecaca; color: #991b1b; }}
            .poor-match {{ background: #f3f4f6; color: #374151; }}
            .reasoning {{
                margin-top: 10px;
                padding: 10px;
                background: #f8fafc;
                border-radius: 8px;
                font-size: 0.9em;
                color: #4b5563;
                font-style: italic;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎯 Employee Skills Analysis</h1>
            <p class="subtitle">Skills matching analysis for {len(results)} employees</p>
            
            <div class="required-skills">
                <h3>🔍 Required Skills</h3>
                <div>
                    {' '.join([f'<span class="skill-tag">{skill}</span>' for skill in required_skills])}
                </div>
            </div>
            
            <div class="employee-grid">
    """
    
    # Generate employee cards
    for emp in results:
        score = emp.get('score', 0)
        score_color = get_score_color(score)
        
        # Recommendation styling
        rec_class = emp.get('recommendation', 'Poor Match').lower().replace(' ', '-')
        
        matching_skills_html = ''.join([
            f'<span class="matching-skill">{skill}</span>' 
            for skill in emp.get('matching_skills', [])
        ])
        
        missing_skills_html = ''.join([
            f'<span class="missing-skill">{skill}</span>' 
            for skill in emp.get('missing_skills', [])
        ])
        
        html_content += f"""
                <div class="employee-card">
                    <div class="employee-header">
                        <div class="employee-name">{emp['employee_name']}</div>
                        <div class="score-circle" style="background-color: {score_color}" 
                             data-tooltip="Score: {score}/100">
                            {score}%
                        </div>
                    </div>
                    
                    <div class="employee-stats">
                        <div class="stat">
                            <span>📋</span>
                            <span>{emp.get('ticket_count', 0)} tickets</span>
                        </div>
                        <div class="stat">
                            <span>✅</span>
                            <span>{len(emp.get('matching_skills', []))} matches</span>
                        </div>
                        <div class="stat">
                            <span>❌</span>
                            <span>{len(emp.get('missing_skills', []))} missing</span>
                        </div>
                    </div>
                    
                    <div class="skills-section">
                        {f'<div class="skills-title">✅ Matching Skills</div><div class="matching-skills">{matching_skills_html}</div>' if matching_skills_html else ''}
                        {f'<div class="skills-title">❌ Missing Skills</div><div class="missing-skills">{missing_skills_html}</div>' if missing_skills_html else ''}
                    </div>
                    
                    <div class="recommendation {rec_class}">
                        🎯 {emp.get('recommendation', 'No recommendation')}
                    </div>
                    
                    {f'<div class="reasoning">💡 {emp.get("reasoning", "")}</div>' if emp.get("reasoning") else ''}
                </div>
        """
    
    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    
    # Write to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ HTML report generated: {output_file}")
        return output_file
    except Exception as e:
        print(f"❌ Error generating HTML report: {e}")
        return None