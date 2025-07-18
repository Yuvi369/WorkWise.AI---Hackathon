import os
import json
import math
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
from base_agent import BaseAgent, Tool, EmployeeProfile
import google.generativeai as genai

class GetEmployeeHistoryTool(Tool):
    def __init__(self):
        super().__init__("get_employee_history", "Retrieve employee work history and performance")
        
        # Mock database of employee history
        self.employee_history = {
            "EMP001": {
                "completed_tickets": [
                    {
                        "ticket_id": "TICK-100",
                        "title": "React Dashboard Development",
                        "skills_used": ["react", "javascript", "css"],
                        "completion_time": 25,
                        "estimated_time": 30,
                        "quality_score": 4.5,
                        "completion_date": "2024-01-15",
                        "category": "frontend"
                    },
                    {
                        "ticket_id": "TICK-101",
                        "title": "API Integration",
                        "skills_used": ["nodejs", "api", "javascript"],
                        "completion_time": 18,
                        "estimated_time": 20,
                        "quality_score": 4.8,
                        "completion_date": "2024-01-22",
                        "category": "backend"
                    }
                ],
                "performance_metrics": {
                    "avg_completion_ratio": 0.85,  # actual/estimated time
                    "avg_quality_score": 4.65,
                    "total_tickets": 15,
                    "success_rate": 0.95,
                    "preferred_categories": ["frontend", "backend"]
                }
            },
            "EMP002": {
                "completed_tickets": [
                    {
                        "ticket_id": "TICK-200",
                        "title": "Database Optimization",
                        "skills_used": ["sql", "database", "performance"],
                        "completion_time": 40,
                        "estimated_time": 35,
                        "quality_score": 4.2,
                        "completion_date": "2024-01-10",
                        "category": "database"
                    }
                ],
                "performance_metrics": {
                    "avg_completion_ratio": 1.1,
                    "avg_quality_score": 4.2,
                    "total_tickets": 8,
                    "success_rate": 0.88,
                    "preferred_categories": ["database", "backend"]
                }
            },
            "EMP003": {
                "completed_tickets": [
                    {
                        "ticket_id": "TICK-300",
                        "title": "Cloud Infrastructure Setup",
                        "skills_used": ["aws", "cloud", "devops"],
                        "completion_time": 50,
                        "estimated_time": 45,
                        "quality_score": 4.9,
                        "completion_date": "2024-01-05",
                        "category": "infrastructure"
                    }
                ],
                "performance_metrics": {
                    "avg_completion_ratio": 0.9,
                    "avg_quality_score": 4.9,
                    "total_tickets": 12,
                    "success_rate": 0.92,
                    "preferred_categories": ["infrastructure", "devops"]
                }
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        employee_id = params.get("employee_id")
        include_tickets = params.get("include_tickets", True)
        
        if employee_id not in self.employee_history:
            return {
                "status": "error",
                "error": f"Employee {employee_id} not found in history"
            }
        
        history = self.employee_history[employee_id]
        
        result = {
            "status": "success",
            "employee_id": employee_id,
            "performance_metrics": history["performance_metrics"]
        }
        
        if include_tickets:
            result["completed_tickets"] = history["completed_tickets"]
        
        return result

class CalculateSimilarityTool(Tool):
    def __init__(self):
        super().__init__("calculate_similarity", "Calculate similarity between tickets and employee history")
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        ticket_skills = params.get("ticket_skills", [])
        employee_history = params.get("employee_history", {})
        ticket_category = params.get("ticket_category", "")
        
        completed_tickets = employee_history.get("completed_tickets", [])
        performance_metrics = employee_history.get("performance_metrics", {})
        
        # Calculate skill similarity
        skill_similarity = self._calculate_skill_similarity(ticket_skills, completed_tickets)
        
        # Calculate category similarity
        category_similarity = self._calculate_category_similarity(ticket_category, completed_tickets)
        
        # Calculate performance factor
        performance_factor = self._calculate_performance_factor(performance_metrics)
        
        # Overall similarity score
        overall_similarity = (
            skill_similarity * 0.4 +
            category_similarity * 0.3 +
            performance_factor * 0.3
        )
        
        return {
            "status": "success",
            "skill_similarity": skill_similarity,
            "category_similarity": category_similarity,
            "performance_factor": performance_factor,
            "overall_similarity": overall_similarity,
            "recommendation_score": overall_similarity * 100,
            "similar_tickets": self._find_similar_tickets(ticket_skills, completed_tickets)
        }
    
    def _calculate_skill_similarity(self, ticket_skills: List[str], completed_tickets: List[Dict]) -> float:
        """Calculate similarity based on skills used in previous tickets"""
        if not completed_tickets:
            return 0.0
        
        all_employee_skills = set()
        for ticket in completed_tickets:
            all_employee_skills.update(ticket.get("skills_used", []))
        
        ticket_skills_set = set(skill.lower() for skill in ticket_skills)
        employee_skills_set = set(skill.lower() for skill in all_employee_skills)
        
        if not ticket_skills_set:
            return 0.0
        
        # Jaccard similarity
        intersection = len(ticket_skills_set & employee_skills_set)
        union = len(ticket_skills_set | employee_skills_set)
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_category_similarity(self, ticket_category: str, completed_tickets: List[Dict]) -> float:
        """Calculate similarity based on ticket categories"""
        if not completed_tickets:
            return 0.0
        
        category_counts = {}
        for ticket in completed_tickets:
            cat = ticket.get("category", "").lower()
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        ticket_cat_lower = ticket_category.lower()
        total_tickets = len(completed_tickets)
        
        if ticket_cat_lower in category_counts:
            return category_counts[ticket_cat_lower] / total_tickets
        
        return 0.0
    
    def _calculate_performance_factor(self, performance_metrics: Dict) -> float:
        """Calculate performance factor based on historical performance"""
        if not performance_metrics:
            return 0.5  # Default neutral score
        
        # Normalize metrics to 0-1 scale
        completion_ratio = min(1.0, 1.0 / performance_metrics.get("avg_completion_ratio", 1.0))
        quality_score = performance_metrics.get("avg_quality_score", 3.0) / 5.0
        success_rate = performance_metrics.get("success_rate", 0.5)
        
        return (completion_ratio + quality_score + success_rate) / 3.0
    
    def _find_similar_tickets(self, ticket_skills: List[str], completed_tickets: List[Dict]) -> List[Dict]:
        """Find tickets with similar skills"""
        similar_tickets = []
        ticket_skills_set = set(skill.lower() for skill in ticket_skills)
        
        for ticket in completed_tickets:
            ticket_skills_used = set(skill.lower() for skill in ticket.get("skills_used", []))
            similarity = len(ticket_skills_set & ticket_skills_used) / len(ticket_skills_set | ticket_skills_used) if ticket_skills_set | ticket_skills_used else 0
            
            if similarity > 0.3:  # Threshold for similarity
                similar_tickets.append({
                    "ticket_id": ticket["ticket_id"],
                    "title": ticket["title"],
                    "similarity": similarity,
                    "skills_used": ticket["skills_used"]
                })
        
        return sorted(similar_tickets, key=lambda x: x["similarity"], reverse=True)

class HistoryAnalyst(BaseAgent):
    def __init__(self):
        super().__init__(
            name="history_analyst",
            role="Employee History Analyst",
            specialization="analyzing employee work history and performance patterns"
        )
        
        # Add tools
        self.add_tool(GetEmployeeHistoryTool())
        self.add_tool(CalculateSimilarityTool())
    
    def analyze_employee_for_ticket(self, employee_id: str, ticket_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how well an employee matches a ticket based on history"""
        
        # Get employee history
        history_result = self.tools["get_employee_history"].execute({
            "employee_id": employee_id,
            "include_tickets": True
        })
        
        if history_result["status"] == "error":
            return {
                "employee_id": employee_id,
                "match_score": 0.0,
                "error": history_result["error"]
            }
        
        # Calculate similarity
        similarity_result = self.tools["calculate_similarity"].execute({
            "ticket_skills": ticket_requirements.get("required_skills", []),
            "employee_history": history_result,
            "ticket_category": ticket_requirements.get("category", "")
        })
        
        # Generate insights using LLM
        insights = self._generate_insights(employee_id, history_result, similarity_result, ticket_requirements)
        
        return {
            "employee_id": employee_id,
            "match_score": similarity_result["overall_similarity"],
            "recommendation_score": similarity_result["recommendation_score"],
            "skill_similarity": similarity_result["skill_similarity"],
            "category_similarity": similarity_result["category_similarity"],
            "performance_factor": similarity_result["performance_factor"],
            "similar_tickets": similarity_result["similar_tickets"],
            "performance_metrics": history_result["performance_metrics"],
            "insights": insights,
            "recommendation": "recommended" if similarity_result["overall_similarity"] > 0.6 else "not_recommended"
        }
    
    def _generate_insights(self, employee_id: str, history_result: Dict, similarity_result: Dict, ticket_requirements: Dict) -> Dict[str, Any]:
        """Generate insights about employee-ticket match"""
        
        performance_metrics = history_result["performance_metrics"]
        
        insights = {
            "strengths": [],
            "concerns": [],
            "recommendations": []
        }
        
        # Analyze strengths
        if similarity_result["skill_similarity"] > 0.7:
            insights["strengths"].append("High skill match with previous work")
        
        if performance_metrics["avg_quality_score"] > 4.5:
            insights["strengths"].append("Consistently high quality work")
        
        if performance_metrics["avg_completion_ratio"] < 0.9:
            insights["strengths"].append("Usually completes tasks faster than estimated")
        
        # Analyze concerns
        if similarity_result["skill_similarity"] < 0.3:
            insights["concerns"].append("Limited experience with required skills")
        
        if performance_metrics["avg_completion_ratio"] > 1.2:
            insights["concerns"].append("Tends to take longer than estimated")
        
        if performance_metrics["success_rate"] < 0.8:
            insights["concerns"].append("Lower than average success rate")
        
        # Generate recommendations
        if similarity_result["overall_similarity"] > 0.6:
            insights["recommendations"].append("Good match for this ticket")
        else:
            insights["recommendations"].append("Consider providing additional support or training")
        
        return insights

# Example usage
if __name__ == "__main__":
    # Test the History Analyst
    analyst = HistoryAnalyst()
    
    # Sample ticket requirements
    ticket_requirements = {
        "required_skills": ["react", "javascript", "api"],
        "category": "frontend",
        "priority": "high",
        "estimated_hours": 30
    }
    
    # Analyze multiple employees
    employees = ["EMP001", "EMP002", "EMP003"]
    
    print("📊 Employee History Analysis:")
    print("=" * 50)
    
    for emp_id in employees:
        result = analyst.analyze_employee_for_ticket(emp_id, ticket_requirements)
        print(f"\n👤 Employee: {emp_id}")
        print(f"Match Score: {result['match_score']:.2f}")
        print(f"Recommendation: {result['recommendation']}")
        print(f"Strengths: {', '.join(result['insights']['strengths'])}")
        if result['insights']['concerns']:
            print(f"Concerns: {', '.join(result['insights']['concerns'])}")
        print("-" * 30)