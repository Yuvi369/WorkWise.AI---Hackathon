# tools_camel/log_data_tool.py

import json
from datetime import datetime
from typing import Dict, Any, List

def log_data(overall_agents_result: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summarize the entire process based on all agent results and input data.
    
    Args:
        overall_agents_result: Dictionary containing results from all agents
        input_data: Dictionary containing original input data (ticket, employees, etc.)
        
    Returns:
        Dictionary with comprehensive process summary
    """
    
    print("📝 Starting process summarization...")
    print(f"📊 Agents processed: {list(overall_agents_result.keys())}")
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract key information
    summary = {
        "execution_summary": _create_execution_summary(overall_agents_result, input_data),
        "process_flow": _create_process_flow(overall_agents_result),
        "key_insights": _extract_key_insights(overall_agents_result),
        "decision_rationale": _create_decision_rationale(overall_agents_result),
        "performance_metrics": _calculate_performance_metrics(overall_agents_result),
        "recommendations": _generate_recommendations(overall_agents_result, input_data),
        "metadata": {
            "timestamp": timestamp,
            "total_agents": len(overall_agents_result),
            "process_status": "completed",
            "data_quality": _assess_data_quality(overall_agents_result)
        }
    }
    
    print("✅ Process summarization completed")
    return summary

def _create_execution_summary(overall_agents_result: Dict[str, Any], input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create high-level execution summary"""
    
    # Extract ticket information
    ticket_info = input_data.get('ticket_info', {})
    employees = input_data.get('employees', [])
    
    # Get final recommendation
    final_recommendation = None
    if 'employee_scorer' in overall_agents_result:
        scorer_result = overall_agents_result['employee_scorer']
        if isinstance(scorer_result, dict) and 'top_recommendation' in scorer_result:
            final_recommendation = scorer_result['top_recommendation']
    
    return {
        "ticket_analyzed": ticket_info.get('name', 'N/A'),
        "employees_evaluated": len(employees),
        "employee_list": employees,
        "final_recommendation": final_recommendation,
        "process_outcome": "success" if final_recommendation else "partial",
        "total_processing_steps": len(overall_agents_result)
    }

def _create_process_flow(overall_agents_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create step-by-step process flow"""
    
    process_steps = []
    
    # Define typical agent order and their purposes
    agent_order = [
        ("ticket_analyzer", "Ticket Analysis & Skill Extraction"),
        ("history_analyzer", "Employee History & Similarity Analysis"),
        ("employee_scorer", "Final Scoring & Recommendation")
    ]
    
    step_number = 1
    for agent_name, description in agent_order:
        if agent_name in overall_agents_result:
            agent_result = overall_agents_result[agent_name]
            
            # Determine step status
            status = "completed" if agent_result and not isinstance(agent_result, dict) or not agent_result.get('error') else "failed"
            
            # Extract key outputs
            key_outputs = _extract_agent_outputs(agent_name, agent_result)
            
            process_steps.append({
                "step": step_number,
                "agent": agent_name,
                "description": description,
                "status": status,
                "key_outputs": key_outputs,
                "data_generated": len(str(agent_result)) if agent_result else 0
            })
            
            step_number += 1
    
    return process_steps

def _extract_agent_outputs(agent_name: str, agent_result: Any) -> List[str]:
    """Extract key outputs from each agent"""
    
    key_outputs = []
    
    if not agent_result:
        return ["No output generated"]
    
    if agent_name == "ticket_analyzer":
        if isinstance(agent_result, dict):
            if 'normalized_skills' in agent_result:
                key_outputs.append(f"Normalized {len(agent_result['normalized_skills'])} skills")
            if 'enriched_skills' in agent_result:
                key_outputs.append(f"Enriched with {len(agent_result['enriched_skills'])} additional skills")
    
    elif agent_name == "history_analyzer":
        if isinstance(agent_result, dict):
            if 'history_found' in agent_result:
                employees_with_history = len(agent_result['history_found'])
                key_outputs.append(f"Retrieved history for {employees_with_history} employees")
            if 'calculated_similarity' in agent_result:
                similarity_scores = len(agent_result['calculated_similarity'])
                key_outputs.append(f"Calculated similarity for {similarity_scores} employees")
    
    elif agent_name == "employee_scorer":
        if isinstance(agent_result, dict):
            if 'scores' in agent_result:
                scored_employees = len(agent_result['scores'])
                key_outputs.append(f"Scored {scored_employees} employees")
            if 'top_recommendation' in agent_result:
                top_emp = agent_result['top_recommendation']['employee']
                top_score = agent_result['top_recommendation']['score']
                key_outputs.append(f"Recommended {top_emp} (score: {top_score})")
    
    return key_outputs if key_outputs else ["Output generated"]

def _extract_key_insights(overall_agents_result: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key insights from all agents"""
    
    insights = {
        "skill_insights": {},
        "performance_insights": {},
        "matching_insights": {}
    }
    
    # Skill insights from ticket analyzer
    if 'ticket_analyzer' in overall_agents_result:
        ticket_result = overall_agents_result['ticket_analyzer']
        if isinstance(ticket_result, dict):
            insights["skill_insights"] = {
                "total_skills_identified": len(ticket_result.get('normalized_skills', [])) + len(ticket_result.get('enriched_skills', [])),
                "normalized_skills": ticket_result.get('normalized_skills', []),
                "enriched_skills": ticket_result.get('enriched_skills', [])
            }
    
    # Performance insights from history analyzer
    if 'history_analyzer' in overall_agents_result:
        history_result = overall_agents_result['history_analyzer']
        if isinstance(history_result, dict) and 'history_found' in history_result:
            employee_performance = {}
            for emp, history in history_result['history_found'].items():
                if history:
                    avg_success = sum(record.get('success_rate', 0) for record in history) / len(history)
                    employee_performance[emp] = {
                        "projects_completed": len(history),
                        "average_success_rate": round(avg_success, 3)
                    }
            insights["performance_insights"] = employee_performance
    
    # Matching insights from scorer
    if 'employee_scorer' in overall_agents_result:
        scorer_result = overall_agents_result['employee_scorer']
        if isinstance(scorer_result, dict) and 'scores' in scorer_result:
            score_distribution = {}
            for emp, score_data in scorer_result['scores'].items():
                score_distribution[emp] = {
                    "total_score": score_data['total_score'],
                    "strongest_area": max(score_data, key=lambda k: score_data[k] if isinstance(score_data[k], (int, float)) else 0),
                    "confidence": score_data.get('confidence', 'unknown')
                }
            insights["matching_insights"] = score_distribution
    
    return insights

def _create_decision_rationale(overall_agents_result: Dict[str, Any]) -> Dict[str, Any]:
    """Create rationale for the final decision"""
    
    rationale = {
        "decision_factors": [],
        "supporting_evidence": {},
        "alternative_considerations": []
    }
    
    # Get final recommendation
    if 'employee_scorer' in overall_agents_result:
        scorer_result = overall_agents_result['employee_scorer']
        if isinstance(scorer_result, dict) and 'top_recommendation' in scorer_result:
            recommended_emp = scorer_result['top_recommendation']['employee']
            
            rationale["decision_factors"].append(f"Selected {recommended_emp} based on comprehensive scoring")
            
            # Add supporting evidence
            if 'scores' in scorer_result and recommended_emp in scorer_result['scores']:
                emp_score = scorer_result['scores'][recommended_emp]
                rationale["supporting_evidence"] = {
                    "total_score": emp_score['total_score'],
                    "skill_match": emp_score.get('skill_match', 0),
                    "history_performance": emp_score.get('history_performance', 0),
                    "similarity": emp_score.get('similarity', 0),
                    "confidence_level": emp_score.get('confidence', 'unknown')
                }
    
    return rationale

def _calculate_performance_metrics(overall_agents_result: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate performance metrics for the process"""
    
    metrics = {
        "process_efficiency": {},
        "data_coverage": {},
        "quality_indicators": {}
    }
    
    # Process efficiency
    successful_agents = sum(1 for result in overall_agents_result.values() 
                          if result and not (isinstance(result, dict) and result.get('error')))
    
    metrics["process_efficiency"] = {
        "agents_successful": successful_agents,
        "agents_total": len(overall_agents_result),
        "success_rate": round(successful_agents / len(overall_agents_result) * 100, 1) if overall_agents_result else 0
    }
    
    # Data coverage
    total_data_points = sum(len(str(result)) for result in overall_agents_result.values())
    metrics["data_coverage"] = {
        "total_data_generated": total_data_points,
        "average_per_agent": round(total_data_points / len(overall_agents_result), 1) if overall_agents_result else 0
    }
    
    return metrics

def _generate_recommendations(overall_agents_result: Dict[str, Any], input_data: Dict[str, Any]) -> List[str]:
    """Generate process improvement recommendations"""
    
    recommendations = []
    
    # Check for missing data
    if 'ticket_analyzer' not in overall_agents_result:
        recommendations.append("Consider implementing ticket analysis for better skill extraction")
    
    if 'history_analyzer' not in overall_agents_result:
        recommendations.append("Add employee history analysis for more accurate predictions")
    
    # Check data quality
    if 'employee_scorer' in overall_agents_result:
        scorer_result = overall_agents_result['employee_scorer']
        if isinstance(scorer_result, dict) and 'top_recommendation' in scorer_result:
            confidence = scorer_result['top_recommendation'].get('confidence', 'unknown')
            if confidence == 'low':
                recommendations.append("Low confidence score detected - consider gathering more employee data")
    
    # General recommendations
    recommendations.append("Regular model retraining recommended for improved accuracy")
    recommendations.append("Consider implementing feedback loops for continuous improvement")
    
    return recommendations

def _assess_data_quality(overall_agents_result: Dict[str, Any]) -> str:
    """Assess overall data quality"""
    
    if not overall_agents_result:
        return "poor"
    
    # Check for errors
    error_count = sum(1 for result in overall_agents_result.values() 
                     if isinstance(result, dict) and result.get('error'))
    
    if error_count == 0:
        return "excellent"
    elif error_count <= len(overall_agents_result) * 0.3:
        return "good"
    else:
        return "poor"

if __name__ == "__main__":
    # Test the log_data function
    print("🧪 Testing log_data function")
    print("=" * 50)
    
    # Test data - simulating complete agent results
    test_overall_results = {
        "ticket_analyzer": {
            "normalized_skills": ["Python", "JavaScript", "Lightning Web Components", "CSS3"],
            "enriched_skills": ["Frontend Development", "Component Architecture"]
        },
        "history_analyzer": {
            "history_found": {
                "Mark Jenkins": [
                    {"ticket": "UI Component Fix", "skills_used": ["JavaScript", "CSS3"], "success_rate": 0.95}
                ],
                "Kenneth Green": [
                    {"ticket": "Backend API", "skills_used": ["Python"], "success_rate": 0.92}
                ]
            },
            "calculated_similarity": {
                "Mark Jenkins": 0.85,
                "Kenneth Green": 0.60
            }
        },
        "employee_scorer": {
            "scores": {
                "Mark Jenkins": {"total_score": 87.5, "confidence": "high"},
                "Kenneth Green": {"total_score": 72.3, "confidence": "medium"}
            },
            "top_recommendation": {
                "employee": "Mark Jenkins",
                "score": 87.5,
                "confidence": "high"
            }
        }
    }
    
    test_input_data = {
        "ticket_info": {
            "name": "Fix button layout issues in LWC component",
            "skills": ["Lightning Web Components", "CSS3", "JavaScript"],
            "priority": "high"
        },
        "employees": ["Mark Jenkins", "Kenneth Green"]
    }
    
    # Run the test
    result = log_data(test_overall_results, test_input_data)
    
    print("\n" + "=" * 50)
    print("📋 PROCESS SUMMARY:")
    print("=" * 50)
    print(json.dumps(result, indent=2))