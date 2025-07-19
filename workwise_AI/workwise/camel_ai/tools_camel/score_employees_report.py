import os
import json
from datetime import datetime
from typing import List, Dict, Any

def generate_scoring_report(scored_employees: List[Dict], output_file: str = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\camel_ai\tools_camel\reports_exec\scorer_agent_report.html"):
    """
    Generates an HTML report for employee scoring results with a compact UI and progress bar for overall score.
    
    Args:
        scored_employees (List[Dict]): List of dictionaries containing employee scoring data
        output_file (str): Name of the output HTML file
    
    Returns:
        str: Path to the generated HTML file
    """
    if not scored_employees:
        print("❌ No scoring results to generate report")
        return None
    
    # Count statistics by recommendation
    recommendation_counts = {
        "Highly recommended": 0,
        "Recommended": 0,
        "Fair match": 0,
        "Poor match": 0
    }
    for emp in scored_employees:
        recommendation = emp.get("recommendation", "Unknown")
        if recommendation in recommendation_counts:
            recommendation_counts[recommendation] += 1
    
    # Set current timestamp (03:46 AM IST, July 19, 2025)
    report_time = "2025-07-19 03:46:00"
    
    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Employee Scoring Dashboard</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
                min-height: 100vh;
                padding: 10px;
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
                background: 
                    radial-gradient(circle at 20% 30%, rgba(88, 166, 255, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 70%, rgba(255, 107, 107, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 50% 50%, rgba(46, 213, 115, 0.1) 0%, transparent 50%);
                pointer-events: none;
                z-index: 0;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                position: relative;
                z-index: 1;
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
                padding: 10px;
            }}
            .header h1 {{
                font-size: 2rem;
                font-weight: 800;
                background: linear-gradient(135deg, #58a6ff 0%, #ff6b6b 50%, #2ed573 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 5px;
                text-shadow: 0 0 20px rgba(88, 166, 255, 0.3);
            }}
            .header p {{
                color: rgba(255, 255, 255, 0.7);
                font-size: 0.9rem;
                font-weight: 400;
                margin-bottom: 5px;
            }}
            .date-info {{
                color: rgba(255, 255, 255, 0.5);
                font-size: 0.7rem;
            }}
            .employee-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 15px;
                margin-bottom: 20px;
            }}
            .employee-card {{
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 15px;
                position: relative;
                overflow: hidden;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                cursor: pointer;
            }}
            .employee-card.highly-recommended {{
                border-left: 3px solid #2ed573;
            }}
            .employee-card.recommended {{
                border-left: 3px solid #58a6ff;
            }}
            .employee-card.fair-match {{
                border-left: 3px solid #f59e0b;
            }}
            .employee-card.poor-match {{
                border-left: 3px solid #ff4757;
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
                transition: opacity 0.4s ease;
            }}
            .employee-card:hover::before {{
                opacity: 1;
            }}
            .employee-card:hover {{
                transform: translateY(-5px) scale(1.01);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                border-color: rgba(255, 255, 255, 0.2);
            }}
            .status-badge {{
                position: absolute;
                top: 10px;
                right: 10px;
                padding: 5px 10px;
                border-radius: 10px;
                font-size: 0.6rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.3px;
            }}
            .badge-highly-recommended {{
                background: linear-gradient(135deg, #2ed573 0%, #17c0eb 100%);
                color: white;
            }}
            .badge-recommended {{
                background: linear-gradient(135deg, #58a6ff 0%, #4facfe 100%);
                color: white;
            }}
            .badge-fair-match {{
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                color: white;
            }}
            .badge-poor-match {{
                background: linear-gradient(135deg, #ff4757 0%, #ff3838 100%);
                color: white;
            }}
            .employee-title {{
                font-size: 1.2rem;
                font-weight: 700;
                color: #fff;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            .employee-icon {{
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1rem;
            }}
            .score-section {{
                margin-bottom: 10px;
            }}
            .chart-container {{
                width: 120px;
                height: 120px;
                margin: 0 auto;
            }}
            .progress-container {{
                width: 100%;
                margin-top: 10px;
                text-align: center;
            }}
            .progress-bar {{
                width: 100%;
                height: 15px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                overflow: hidden;
            }}
            .progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, #2ed573 0%, #58a6ff 100%);
                border-radius: 5px;
                transition: width 0.4s ease;
            }}
            .progress-text {{
                margin-top: 3px;
                color: rgba(255, 255, 255, 0.8);
                font-size: 0.7rem;
            }}
            .metrics-container {{
                display: flex;
                flex-direction: column;
                gap: 5px;
                margin-bottom: 10px;
            }}
            .metric {{
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 5px;
                border-radius: 5px;
                background: rgba(255, 255, 255, 0.05);
                transition: all 0.3s ease;
            }}
            .metric:hover {{
                background: rgba(255, 255, 255, 0.08);
            }}
            .metric-label {{
                flex: 1;
                font-size: 0.7rem;
                font-weight: 600;
                color: rgba(255, 255, 255, 0.8);
            }}
            .metric-value {{
                font-size: 0.7rem;
                font-weight: 700;
                color: #58a6ff;
            }}
            .details-section {{
                background: rgba(255, 255, 255, 0.03);
                border-radius: 5px;
                padding: 10px;
                border-left: 2px solid #58a6ff;
            }}
            .details-title {{
                font-size: 0.7rem;
                font-weight: 700;
                color: #fff;
                margin-bottom: 5px;
            }}
            .details-text {{
                font-size: 0.6rem;
                color: rgba(255, 255, 255, 0.8);
                line-height: 1.2;
                margin-bottom: 5px;
            }}
            .strengths-list, .concerns-list {{
                margin-left: 10px;
            }}
            .strength-item, .concern-item {{
                font-size: 0.6rem;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 2px;
            }}
            .strength-item::before {{
                content: '✓ ';
                color: #2ed573;
                font-weight: bold;
            }}
            .concern-item::before {{
                content: '⚠ ';
                color: #f59e0b;
                font-weight: bold;
            }}
            .summary-stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 10px;
                margin-top: 20px;
            }}
            .stat-card {{
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 10px;
                text-align: center;
                transition: all 0.3s ease;
            }}
            .stat-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }}
            .stat-number {{
                font-size: 1.5rem;
                font-weight: 800;
                color: #58a6ff;
                margin-bottom: 3px;
            }}
            .stat-label {{
                font-size: 0.7rem;
                color: rgba(255, 255, 255, 0.7);
                text-transform: uppercase;
                letter-spacing: 0.3px;
            }}
            @media (max-width: 768px) {{
                .header h1 {{
                    font-size: 1.5rem;
                }}
                .employee-container {{
                    grid-template-columns: 1fr;
                    gap: 10px;
                }}
                .employee-card {{
                    padding: 10px;
                }}
            }}
            .floating-orb {{
                position: fixed;
                width: 200px;
                height: 200px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(88, 166, 255, 0.1) 0%, transparent 70%);
                pointer-events: none;
                z-index: -1;
                animation: float 6s ease-in-out infinite;
            }}
            .floating-orb:nth-child(1) {{
                top: 10%;
                left: 10%;
                animation-delay: 0s;
            }}
            .floating-orb:nth-child(2) {{
                top: 60%;
                right: 10%;
                animation-delay: 2s;
            }}
            @keyframes float {{
                0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
                50% {{ transform: translateY(-15px) rotate(180deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="floating-orb"></div>
        <div class="floating-orb"></div>
        <div class="container">
            <div class="header">
                <h1>🎯 Employee Scoring Dashboard</h1>
                <p>Real-time employee performance evaluation and recommendation system</p>
                <div class="date-info">Generated on: {report_time}</div>
            </div>
            <div class="employee-container">
    """
    
    # Generate employee cards with progress bar for overall score
    employee_details = {}
    for emp in scored_employees:
        employee_name = emp.get("employee_name", "Unknown")
        overall_score = emp.get("overall_score", 0)
        skill_match_score = emp.get("skill_match_score", 0)
        experience_score = emp.get("experience_score", 0)
        availability_score = emp.get("availability_score", 0)
        policy_score = emp.get("policy_score", 0)
        recommendation = emp.get("recommendation", "Unknown")
        reasoning = emp.get("reasoning", "No reasoning provided")
        strengths = emp.get("strengths", [])
        concerns = emp.get("concerns", [])
        
        employee_id = employee_name.lower().replace(" ", "_")
        rec_class = recommendation.lower().replace(" ", "-")
        
        # Store detailed text for JavaScript
        strengths_text = "\n".join([f"✓ {s}" for s in strengths])
        concerns_text = "\n".join([f"⚠ {c}" for c in concerns])
        employee_details[employee_id] = f"{employee_name} - {recommendation}\nOverall Score: {overall_score}/100\n\nDetailed Assessment:\n• Skill Match: {skill_match_score}/100 - {reasoning}\n• Experience: {experience_score}/100\n• Availability: {availability_score}/100\n• Policy Compliance: {policy_score}/100\n\nReasoning: {reasoning}\n\nKey Strengths:\n{strengths_text}\n\nAreas for Development:\n{concerns_text}\n\nRecommendation: Assign with confidence."
        
        # Calculate weighted contributions for the four categories (total 100%)
        total_individual_weight = 1.0  # 25% + 25% + 20% + 30% to sum to 100%
        individual_sum = (skill_match_score * 0.25 + experience_score * 0.25 + 
                         availability_score * 0.20 + policy_score * 0.30)  # Adjusted weights
        if individual_sum > 0:
            scale_factor = (100 * total_individual_weight) / individual_sum
            skill_weighted = (skill_match_score * 0.25 * scale_factor) / 100 * 100
            experience_weighted = (experience_score * 0.25 * scale_factor) / 100 * 100
            availability_weighted = (availability_score * 0.20 * scale_factor) / 100 * 100
            policy_weighted = (policy_score * 0.30 * scale_factor) / 100 * 100
            # Ensure total sums to 100% (adjust policy if needed due to rounding)
            total_weighted = skill_weighted + experience_weighted + availability_weighted + policy_weighted
            if total_weighted > 0:
                adjustment = 100 / total_weighted
                skill_weighted *= adjustment
                experience_weighted *= adjustment
                availability_weighted *= adjustment
                policy_weighted *= adjustment
        else:
            skill_weighted = 25.0
            experience_weighted = 25.0
            availability_weighted = 20.0
            policy_weighted = 30.0

      
        
        html_content += f"""
            <div class="employee-card {rec_class}" onclick="showEmployeeDetails('{employee_id}')">
                <div class="status-badge badge-{rec_class.lower().replace(' ', '-')}">{recommendation}</div>
                <div class="employee-title">
                    <div class="employee-icon">👨‍💻</div>
                    {employee_name}
                </div>
                <div class="score-section">
                    <div class="progress-container">
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: {overall_score}%;"></div>
                        </div>
                        <div class="progress-text">Overall Score: {overall_score}%</div>
                    </div>
                </div>
                <div class="metrics-container">
                    <div class="metric"><span class="metric-label">Skill Match</span><span class="metric-value">{skill_match_score}/100</span></div>
                    <div class="metric"><span class="metric-label">Experience</span><span class="metric-value">{experience_score}/100</span></div>
                    <div class="metric"><span class="metric-label">Availability</span><span class="metric-value">{availability_score}/100</span></div>
                    <div class="metric"><span class="metric-label">Policy</span><span class="metric-value">{policy_score}/100</span></div>
                </div>
                <div class="details-section">
                    <div class="details-title">Assessment Summary</div>
                    <div class="details-text">{reasoning}</div>
                    <div class="details-text"><strong>Strengths:</strong></div>
                    <div class="strengths-list">
                        {''.join([f'<div class="strength-item">{s}</div>' for s in strengths])}
                    </div>
                    <div class="details-text"><strong>Areas for Improvement:</strong></div>
                    <div class="concerns-list">
                        {''.join([f'<div class="concern-item">{c}</div>' for c in concerns])}
                    </div>
                </div>
            </div>
        """
    
    # Close employee-container and add summary
    html_content += """
            </div>
            <div class="summary-stats">
                <div class="stat-card">
                    <div class="stat-number">3</div>
                    <div class="stat-label">Total Employees</div>
                </div>
    """
    for rec, count in recommendation_counts.items():
        if count > 0:
            html_content += f"""
                <div class="stat-card">
                    <div class="stat-number">{count}</div>
                    <div class="stat-label">{rec}</div>
                </div>
            """
    
    html_content += """
            </div>
        </div>
        <script>
            function showEmployeeDetails(employeeId) {
                const employees = {
    """
    for emp_id, details in employee_details.items():
        html_content += f'                    "{emp_id}": "{details}",\n'
    
    html_content += """
                };
                alert(employees[employeeId] || "Employee details not found");
            }
            
            window.addEventListener('load', function() {
                const cards = document.querySelectorAll('.employee-card');
                cards.forEach((card, index) => {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, index * 150);
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
    # Sample scored employees data
    sample_scored_employees = [
        {
            "employee_name": "Mark Jenkins",
            "overall_score": 85,
            "skill_match_score": 90,
            "experience_score": 80,
            "availability_score": 100,
            "policy_score": 95,
            "recommendation": "Recommended",
            "reasoning": "Mark has strong LWC and JavaScript skills, with good experience in similar tickets.",
            "strengths": ["Proficient in LWC", "Fast resolution times"],
            "concerns": ["Limited CSS expertise"]
        },
        {
            "employee_name": "Kenneth Simpson",
            "overall_score": 92,
            "skill_match_score": 95,
            "experience_score": 90,
            "availability_score": 100,
            "policy_score": 90,
            "recommendation": "Highly recommended",
            "reasoning": "Kenneth excels in LWC and CSS, with excellent past performance.",
            "strengths": ["Expert in LWC and CSS", "High success rate"],
            "concerns": []
        },
        {
            "employee_name": "Anthony Wright",
            "overall_score": 60,
            "skill_match_score": 65,
            "experience_score": 55,
            "availability_score": 80,
            "policy_score": 70,
            "recommendation": "Fair match",
            "reasoning": "Anthony has basic JavaScript skills but lacks LWC experience.",
            "strengths": ["Available for assignment"],
            "concerns": ["Limited LWC experience", "Moderate policy compliance"]
        }
    ]
    
    report_path = generate_scoring_report(sample_scored_employees)
    print(f"Report generated: {report_path}")