import os
from typing import List, Dict, Any

def generate_html_report(results: List[Dict], required_skills: List[str], output_file: str = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec\history_report.html"):

    if not results:
        print("❌ No results to generate report")
        return None
    
    # Get score color and gradient for score-circle
    def get_score_color(score):
        if score >= 80:
            return "linear-gradient(135deg, #10b981 0%, #059669 100%)"  # Green
        elif score >= 60:
            return "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"  # Yellow
        elif score >= 40:
            return "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)"  # Red
        else:
            return "linear-gradient(135deg, #6b7280 0%, #4b5563 100%)"  # Gray
    
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
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
                color: #ffffff;
                line-height: 1.6;
                overflow-x: hidden;
                min-height: 100vh;
            }}
            .background-pattern {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: 
                    radial-gradient(circle at 20% 30%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 70%, rgba(236, 72, 153, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 40% 80%, rgba(14, 165, 233, 0.15) 0%, transparent 50%);
                z-index: -1;
            }}
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                position: relative;
                z-index: 1;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
                position: relative;
            }}
            .header::before {{
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 200px;
                height: 200px;
                background: radial-gradient(circle, rgba(99, 102, 241, 0.2) 0%, transparent 70%);
                transform: translate(-50%, -50%);
                z-index: -1;
                animation: pulse 6s ease-in-out infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ transform: translate(-50%, -50%) scale(1); opacity: 0.2; }}
                50% {{ transform: translate(-50%, -50%) scale(1.1); opacity: 0.4; }}
            }}
            h1 {{
                font-size: 1.75rem;
                font-weight: 900;
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 8px;
                letter-spacing: -0.02em;
                text-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
            }}
            .subtitle {{
                font-size: 0.875rem;
                color: #94a3b8;
                font-weight: 500;
                margin-bottom: 20px;
            }}
            .required-skills {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-left: 3px solid #6366f1;
                padding: 12px;
                margin-bottom: 20px;
                border-radius: 6px;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            }}
            .required-skills:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 24px rgba(99, 102, 241, 0.2);
            }}
            .required-skills h3 {{
                color: #f1f5f9;
                margin-bottom: 8px;
                font-size: 1rem;
                font-weight: 700;
                display: flex;
                align-items: center;
                gap: 4px;
            }}
            .skill-tag {{
                display: inline-block;
                background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
                color: white;
                padding: 4px 10px;
                margin: 4px;
                border-radius: 16px;
                font-size: 0.7rem;
                font-weight: 600;
                box-shadow: 0 2px 10px rgba(99, 102, 241, 0.3);
                transition: all 0.3s ease;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            .skill-tag:hover {{
                transform: translateY(-1px) scale(1.05);
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
            }}
            .employee-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 16px;
            }}
            .employee-card {{
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border-radius: 12px;
                padding: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
                position: relative;
                overflow: hidden;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            }}
            .employee-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.8), transparent);
                transform: translateX(-100%);
                transition: transform 0.6s ease;
            }}
            .employee-card:hover::before {{
                transform: translateX(100%);
            }}
            .employee-card:hover {{
                transform: translateY(-4px);
                background: rgba(255, 255, 255, 0.08);
                box-shadow: 0 10px 30px rgba(99, 102, 241, 0.2);
                border-color: rgba(99, 102, 241, 0.3);
            }}
            .employee-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }}
            .employee-name {{
                font-size: 1rem;
                font-weight: 700;
                color: #f1f5f9;
                letter-spacing: -0.01em;
            }}
            .score-circle {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 800;
                font-size: 0.875rem;
                color: white;
                position: relative;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            }}
            .score-circle:hover {{
                transform: scale(1.1);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            }}
            .score-circle::after {{
                content: attr(data-tooltip);
                position: absolute;
                bottom: -30px;
                left: 50%;
                transform: translateX(-50%);
                background: #1f2937;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.7rem;
                white-space: nowrap;
                z-index: 10;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
            }}
            .score-circle:hover::after {{
                opacity: 1;
                visibility: visible;
                bottom: -25px;
            }}
            .employee-stats {{
                display: flex;
                gap: 16px;
                margin-bottom: 12px;
                font-size: 0.75rem;
                color: #cbd5e1;
            }}
            .stat {{
                display: flex;
                align-items: center;
                gap: 4px;
                background: rgba(255, 255, 255, 0.05);
                padding: 8px 10px;
                border-radius: 6px;
                transition: all 0.3s ease;
            }}
            .stat:hover {{
                background: rgba(255, 255, 255, 0.1);
                transform: translateY(-1px);
            }}
            .skills-section {{
                margin-top: 12px;
            }}
            .skills-title {{
                font-size: 0.75rem;
                font-weight: 700;
                margin-bottom: 6px;
                color: #e2e8f0;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            .matching-skills,
            .missing-skills {{
                display: flex;
                flex-wrap: wrap;
                gap: 4px;
                margin-bottom: 8px;
            }}
            .matching-skill {{
                background: rgba(16, 185, 129, 0.2);
                color: #10b981;
                border: 1px solid rgba(16, 185, 129, 0.3);
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 0.7rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            .matching-skill:hover {{
                background: rgba(16, 185, 129, 0.3);
                transform: translateY(-1px) scale(1.05);
            }}
            .missing-skill {{
                background: rgba(239, 68, 68, 0.2);
                color: #ef4444;
                border: 1px solid rgba(239, 68, 68, 0.3);
                padding: 3px 8px;
                border-radius: 12px;
                font-size: 0.7rem;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            .missing-skill:hover {{
                background: rgba(239, 68, 68, 0.3);
                transform: translateY(-1px) scale(1.05);
            }}
            .recommendation {{
                margin-top: 12px;
                padding: 8px;
                border-radius: 6px;
                text-align: center;
                font-weight: 700;
                font-size: 0.875rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            .recommendation::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
                transition: left 0.6s ease;
            }}
            .recommendation:hover::before {{
                left: 100%;
            }}
            .strong-match {{ 
                background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.2) 100%); 
                color: #10b981; 
                border: 1px solid rgba(16, 185, 129, 0.3);
            }}
            .good-match {{ 
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.2) 100%); 
                color: #f59e0b; 
                border: 1px solid rgba(245, 158, 11, 0.3);
            }}
            .partial-match {{ 
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%); 
                color: #ef4444; 
                border: 1px solid rgba(239, 68, 68, 0.3);
            }}
            .poor-match {{ 
                background: linear-gradient(135deg, rgba(107, 114, 128, 0.2) 0%, rgba(75, 85, 99, 0.2) 100%); 
                color: #6b7280; 
                border: 1px solid rgba(107, 114, 128, 0.3);
            }}
            .reasoning {{
                margin-top: 8px;
                padding: 8px;
                background: rgba(255, 255, 255, 0.03);
                border-radius: 6px;
                font-size: 0.75rem;
                color: #cbd5e1;
                font-style: italic;
                border-left: 3px solid #6366f1;
                transition: all 0.3s ease;
            }}
            .reasoning:hover {{
                background: rgba(255, 255, 255, 0.05);
                transform: translateX(2px);
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
                background: rgba(99, 102, 241, 0.1);
                border-radius: 50%;
                animation: float 25s infinite linear;
            }}
            .floating-element:nth-child(1) {{ left: 10%; width: 15px; height: 15px; animation-delay: 0s; }}
            .floating-element:nth-child(2) {{ left: 20%; width: 12px; height: 12px; animation-delay: 3s; }}
            .floating-element:nth-child(3) {{ left: 30%; width: 18px; height: 18px; animation-delay: 6s; }}
            .floating-element:nth-child(4) {{ left: 40%; width: 14px; height: 14px; animation-delay: 9s; }}
            .floating-element:nth-child(5) {{ left: 50%; width: 16px; height: 16px; animation-delay: 12s; }}
            .floating-element:nth-child(6) {{ left: 60%; width: 13px; height: 13px; animation-delay: 15s; }}
            .floating-element:nth-child(7) {{ left: 70%; width: 17px; height: 17px; animation-delay: 18s; }}
            .floating-element:nth-child(8) {{ left: 80%; width: 15px; height: 15px; animation-delay: 21s; }}
            .floating-element:nth-child(9) {{ left: 90%; width: 16px; height: 16px; animation-delay: 24s; }}
            @keyframes float {{
                0% {{ transform: translateY(100vh) rotate(0deg); opacity: 0; }}
                10% {{ opacity: 1; }}
                90% {{ opacity: 1; }}
                100% {{ transform: translateY(-100px) rotate(360deg); opacity: 0; }}
            }}
            @media (max-width: 768px) {{
                .employee-grid {{
                    grid-template-columns: 1fr;
                }}
                h1 {{
                    font-size: 1.25rem;
                }}
                .container {{
                    padding: 16px;
                }}
                .employee-card {{
                    padding: 12px;
                }}
                .employee-stats {{
                    flex-direction: column;
                    gap: 8px;
                }}
            }}
            @media (max-width: 480px) {{
                h1 {{
                    font-size: 1rem;
                }}
                .employee-header {{
                    flex-direction: column;
                    gap: 8px;
                    text-align: center;
                }}
                .required-skills {{
                    padding: 8px;
                }}
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
                <h1>🎯 Employee Skills Analysis</h1>
                <p class="subtitle">Advanced skills matching analysis for {len(results)} employees</p>
            </div>
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
        score_gradient = get_score_color(score)
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
                        <div class="score-circle" style="background: {score_gradient}" 
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
            'employee_name': 'Mark Jenkins',
            'score': 85,
            'ticket_count': 12,
            'matching_skills': ['Python', 'AWS', 'Docker'],
            'missing_skills': ['Kubernetes', 'Terraform'],
            'recommendation': 'Strong Match',
            'reasoning': 'Mark has extensive experience with Python and AWS, with 12 tickets completed, but lacks Kubernetes expertise.'
        },
        {
            'employee_name': 'Sarah Miller',
            'score': 65,
            'ticket_count': 8,
            'matching_skills': ['Python', 'Docker'],
            'missing_skills': ['AWS', 'Kubernetes', 'Terraform'],
            'recommendation': 'Good Match',
            'reasoning': 'Sarah has solid Python and Docker skills, but limited cloud experience.'
        },
        {
            'employee_name': 'John Doe',
            'score': 45,
            'ticket_count': 5,
            'matching_skills': ['Python'],
            'missing_skills': ['AWS', 'Docker', 'Kubernetes', 'Terraform'],
            'recommendation': 'Partial Match',
            'reasoning': 'John has basic Python skills but lacks experience in other required areas.'
        }
    ]
    
    sample_required_skills = ['Python', 'AWS', 'Docker', 'Kubernetes', 'Terraform']
    
    # Generate the report
    report_path = generate_html_report(sample_results, sample_required_skills)
    print(f"Report generated: {report_path}")