# tools_camel/score_employee_tool.py

import json
from typing import List, Dict, Any

def score_employee(employees: List[str], agent_outputs: Dict[str, Any], ticket_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate comprehensive scores for employees based on all agent outputs.
    
    Args:
        employees: List of employee names to evaluate
        agent_outputs: Dictionary containing outputs from all agents
        ticket_info: Dictionary containing ticket information
        
    Returns:
        Dictionary with employee scores and analysis
    """
    
    print("🔢 Starting employee scoring calculation...")
    print(f"👥 Evaluating employees: {employees}")
    print(f"📊 Agent outputs available: {list(agent_outputs.keys())}")
    
    scores = {}
    max_possible_score = 100
    
    for employee in employees:
        print(f"\n🔍 Scoring employee: {employee}")
        
        # Initialize score components
        skill_match_score = 0
        history_score = 0
        similarity_score = 0
        bonus_score = 0
        
        # 1. Skill Matching Score (40% weight)
        skill_match_score = _calculate_skill_match_score(employee, agent_outputs, ticket_info)
        print(f"  ✅ Skill Match Score: {skill_match_score}/40")
        
        # 2. History Performance Score (35% weight)
        history_score = _calculate_history_score(employee, agent_outputs)
        print(f"  📚 History Score: {history_score}/35")
        
        # 3. Similarity Score (20% weight)
        similarity_score = _calculate_similarity_score(employee, agent_outputs)
        print(f"  🎯 Similarity Score: {similarity_score}/20")
        
        # 4. Bonus Score (5% weight)
        bonus_score = _calculate_bonus_score(employee, agent_outputs, ticket_info)
        print(f"  🌟 Bonus Score: {bonus_score}/5")
        
        # Calculate total score
        total_score = skill_match_score + history_score + similarity_score + bonus_score
        
        # Determine confidence level
        confidence = _determine_confidence(total_score, agent_outputs, employee)
        
        scores[employee] = {
            "total_score": round(total_score, 2),
            "skill_match": skill_match_score,
            "history_performance": history_score,
            "similarity": similarity_score,
            "bonus": bonus_score,
            "confidence": confidence,
            "percentage": round((total_score / max_possible_score) * 100, 1)
        }
        
        print(f"  🎯 Total Score: {total_score:.2f}/{max_possible_score} ({scores[employee]['percentage']}%)")
        print(f"  🎭 Confidence: {confidence}")
    
    # Sort employees by score
    sorted_employees = sorted(scores.items(), key=lambda x: x[1]['total_score'], reverse=True)
    
    result = {
        "scores": scores,
        "ranking": [emp[0] for emp in sorted_employees],
        "top_recommendation": {
            "employee": sorted_employees[0][0],
            "score": sorted_employees[0][1]['total_score'],
            "confidence": sorted_employees[0][1]['confidence']
        } if sorted_employees else None,
        "analysis_metadata": {
            "total_employees_evaluated": len(employees),
            "agents_consulted": list(agent_outputs.keys()),
            "scoring_criteria": ["skill_match", "history_performance", "similarity", "bonus"]
        }
    }
    
    print(f"\n🏆 Top Recommendation: {result['top_recommendation']['employee']} with score {result['top_recommendation']['score']}")
    return result

def _calculate_skill_match_score(employee: str, agent_outputs: Dict[str, Any], ticket_info: Dict[str, Any]) -> float:
    """Calculate skill matching score (max 40 points)"""
    
    required_skills = ticket_info.get('skills', [])
    if not required_skills:
        return 20.0  # Default moderate score if no skills specified
    
    # Get enriched/normalized skills from ticket analyzer
    ticket_analysis = agent_outputs.get('ticket_analyzer', {})
    all_skills = []
    
    if 'normalized_skills' in ticket_analysis:
        all_skills.extend(ticket_analysis['normalized_skills'])
    if 'enriched_skills' in ticket_analysis:
        all_skills.extend(ticket_analysis['enriched_skills'])
    
    # Get employee's historical skills from history analyzer
    history_analysis = agent_outputs.get('history_analyzer', {})
    employee_skills = []
    
    if 'history_found' in history_analysis and employee in history_analysis['history_found']:
        employee_history = history_analysis['history_found'][employee]
        for record in employee_history:
            if 'skills_used' in record:
                employee_skills.extend(record['skills_used'])
    
    # Calculate skill overlap
    skill_matches = 0
    for skill in required_skills + all_skills:
        if any(skill.lower() in emp_skill.lower() or emp_skill.lower() in skill.lower() 
               for emp_skill in employee_skills):
            skill_matches += 1
    
    total_skills = len(set(required_skills + all_skills))
    if total_skills == 0:
        return 20.0
    
    skill_percentage = skill_matches / total_skills
    return min(skill_percentage * 40, 40.0)

def _calculate_history_score(employee: str, agent_outputs: Dict[str, Any]) -> float:
    """Calculate history performance score (max 35 points)"""
    
    history_analysis = agent_outputs.get('history_analyzer', {})
    
    if 'history_found' not in history_analysis or employee not in history_analysis['history_found']:
        return 15.0  # Default score for no history
    
    employee_history = history_analysis['history_found'][employee]
    if not employee_history:
        return 15.0
    
    # Calculate average success rate
    success_rates = []
    for record in employee_history:
        if 'success_rate' in record:
            success_rates.append(record['success_rate'])
    
    if not success_rates:
        return 20.0  # Moderate score if no success rate data
    
    avg_success_rate = sum(success_rates) / len(success_rates)
    
    # Number of projects factor
    project_count_bonus = min(len(employee_history) * 2, 10)  # Max 10 bonus points
    
    history_score = (avg_success_rate * 25) + project_count_bonus
    return min(history_score, 35.0)

def _calculate_similarity_score(employee: str, agent_outputs: Dict[str, Any]) -> float:
    """Calculate similarity score (max 20 points)"""
    
    history_analysis = agent_outputs.get('history_analyzer', {})
    
    if 'calculated_similarity' not in history_analysis or employee not in history_analysis['calculated_similarity']:
        return 10.0  # Default moderate score
    
    similarity_value = history_analysis['calculated_similarity'][employee]
    return similarity_value * 20  # Convert to 20-point scale

def _calculate_bonus_score(employee: str, agent_outputs: Dict[str, Any], ticket_info: Dict[str, Any]) -> float:
    """Calculate bonus score for special factors (max 5 points)"""
    
    bonus = 0.0
    
    # High priority ticket bonus
    if ticket_info.get('priority', '').lower() == 'high':
        # Check if employee has high success rate
        history_analysis = agent_outputs.get('history_analyzer', {})
        if 'history_found' in history_analysis and employee in history_analysis['history_found']:
            employee_history = history_analysis['history_found'][employee]
            avg_success = sum(record.get('success_rate', 0) for record in employee_history) / len(employee_history)
            if avg_success > 0.9:
                bonus += 2.0
    
    # Skill diversity bonus
    ticket_analysis = agent_outputs.get('ticket_analyzer', {})
    if 'enriched_skills' in ticket_analysis:
        enriched_count = len(ticket_analysis['enriched_skills'])
        if enriched_count >= 3:
            bonus += 1.5
    
    # Recent activity bonus (if we had timestamp data)
    bonus += 1.5  # Default recent activity bonus
    
    return min(bonus, 5.0)

def _determine_confidence(total_score: float, agent_outputs: Dict[str, Any], employee: str) -> str:
    """Determine confidence level based on score and data availability"""
    
    # High confidence: score > 80 and good data
    if total_score >= 80:
        return "high"
    
    # Low confidence: score < 50 or limited data
    elif total_score < 50:
        return "low"
    
    # Medium confidence: everything else
    else:
        return "medium"

if __name__ == "__main__":
    # Test the score_employee function
    print("🧪 Testing score_employee function")
    print("=" * 50)
    
    # Test data
    test_employees = ["Mark Jenkins", "Kenneth Green", "Amanda Lewis"]
    
    test_agent_outputs = {
        "ticket_analyzer": {
            "normalized_skills": ["Python", "JavaScript", "Lightning Web Components", "CSS3"],
            "enriched_skills": ["Frontend Development", "Component Architecture", "Responsive Design"]
        },
        "history_analyzer": {
            "history_found": {
                "Mark Jenkins": [
                    {"ticket": "UI Component Fix", "skills_used": ["JavaScript", "CSS3"], "success_rate": 0.95},
                    {"ticket": "LWC Development", "skills_used": ["Lightning Web Components", "JavaScript"], "success_rate": 0.88}
                ],
                "Kenneth Green": [
                    {"ticket": "Backend API", "skills_used": ["Python", "API Development"], "success_rate": 0.92}
                ],
                "Amanda Lewis": [
                    {"ticket": "Vue.js Dashboard", "skills_used": ["Vue.js", "JavaScript", "CSS3"], "success_rate": 0.90}
                ]
            },
            "calculated_similarity": {
                "Mark Jenkins": 0.85,
                "Kenneth Green": 0.60,
                "Amanda Lewis": 0.78
            }
        }
    }
    
    test_ticket_info = {
        "name": "Fix button layout issues and apply responsive design in LWC component",
        "description": "Fix button layout issues and apply responsive design in LWC component.",
        "skills": ["Lightning Web Components", "CSS3", "JavaScript"],
        "priority": "high"
    }
    
    # Run the test
    result = score_employee(test_employees, test_agent_outputs, test_ticket_info)
    
    print("\n" + "=" * 50)
    print("📊 SCORING RESULTS:")
    print("=" * 50)
    print(json.dumps(result, indent=2))