# skill_evaluator_agent.py

from base_agent import BaseAgent
from typing import Dict, List, Tuple, Optional
import pandas as pd
from datetime import datetime
import json

class SkillEvaluator(BaseAgent):
    def __init__(self):
        super().__init__(
            name="skill_evaluator",
            role="Employee-Task Compatibility Analyst",
            specialization="""You are the organization's intelligent decision engine for talent allocation.
                            Your expertise lies in transforming raw skill data into strategic workforce insights.
                            You excel at quantifying compatibility, identifying skill gaps, and generating 
                            data-driven recommendations that optimize both employee growth and project success.
                            You think like a data scientist and strategic HR leader combined.
                          """
        )

    def evaluate_employee_fit(self, normalized_skills: list, employee_fetched_results: dict, 
                             task_context: dict = None) -> dict:
        """
        Method 2: Comprehensive employee-task compatibility analysis
        
        Args:
            normalized_skills: Normalized skill requirements from Method 1
            employee_fetched_results: Employee profiles from Method 1
            task_context: Additional context about the task/ticket
        
        Returns:
            Detailed evaluation with scores, rankings, and strategic recommendations
        """
        
        if not employee_fetched_results:
            return {"error": "No employee data to evaluate", "recommendations": []}
        
        # Core evaluation components
        evaluation_results = {}
        compatibility_matrix = {}
        
        for employee_name, profile in employee_fetched_results.items():
            # Calculate multi-dimensional compatibility score
            compatibility_score = self._calculate_compatibility_score(
                normalized_skills, profile
            )
            
            # Perform detailed skill analysis
            skill_analysis = self._perform_skill_analysis(
                normalized_skills, profile
            )
            
            # Assess experience relevance
            experience_match = self._assess_experience_relevance(
                profile, normalized_skills, task_context
            )
            
            # Calculate learning curve estimation
            learning_curve = self._estimate_learning_curve(
                skill_analysis, profile
            )
            
            # Store comprehensive evaluation
            evaluation_results[employee_name] = {
                "compatibility_score": compatibility_score,
                "skill_analysis": skill_analysis,
                "experience_match": experience_match,
                "learning_curve": learning_curve,
                "overall_rating": self._calculate_overall_rating(
                    compatibility_score, experience_match, learning_curve
                )
            }
            
            # Build compatibility matrix for visualization
            compatibility_matrix[employee_name] = {
                skill: self._skill_proficiency_score(skill, profile)
                for skill in normalized_skills
            }
        
        # Generate strategic recommendations
        ranked_candidates = self._rank_candidates(evaluation_results)
        strategic_insights = self._generate_strategic_insights(
            evaluation_results, normalized_skills, task_context
        )
        
        # Risk and opportunity analysis
        risk_analysis = self._perform_risk_analysis(evaluation_results, normalized_skills)
        
        return {
            "evaluation_metadata": {
                "timestamp": datetime.now().isoformat(),
                "skills_evaluated": normalized_skills,
                "employees_analyzed": len(employee_fetched_results),
                "evaluation_criteria": ["skill_match", "experience", "learning_curve", "availability"]
            },
            "individual_evaluations": evaluation_results,
            "compatibility_matrix": compatibility_matrix,
            "candidate_rankings": ranked_candidates,
            "strategic_recommendations": strategic_insights,
            "risk_opportunity_analysis": risk_analysis,
            "execution_roadmap": self._create_execution_roadmap(ranked_candidates, evaluation_results)
        }
    
    def _calculate_compatibility_score(self, required_skills: list, employee_profile: dict) -> dict:
        """Calculate multi-dimensional compatibility score"""
        
        employee_skills = employee_profile.get('skills', [])
        employee_skills_lower = [skill.lower().strip() for skill in employee_skills]
        
        # Skill matching metrics
        exact_matches = 0
        partial_matches = 0
        skill_depth_score = 0
        
        for req_skill in required_skills:
            req_skill_clean = req_skill.lower().strip()
            
            # Check for exact matches
            if req_skill_clean in employee_skills_lower:
                exact_matches += 1
                skill_depth_score += 1.0
            else:
                # Check for partial/related matches
                partial_match = False
                for emp_skill in employee_skills_lower:
                    if (req_skill_clean in emp_skill or emp_skill in req_skill_clean or
                        self._check_skill_similarity(req_skill_clean, emp_skill)):
                        partial_matches += 1
                        skill_depth_score += 0.6
                        partial_match = True
                        break
                
                if not partial_match:
                    skill_depth_score += 0.0  # Missing skill
        
        # Calculate percentages
        total_skills = len(required_skills)
        exact_match_ratio = exact_matches / total_skills if total_skills > 0 else 0
        coverage_ratio = (exact_matches + partial_matches) / total_skills if total_skills > 0 else 0
        depth_score = skill_depth_score / total_skills if total_skills > 0 else 0
        
        return {
            "exact_matches": exact_matches,
            "partial_matches": partial_matches,
            "missing_skills": total_skills - exact_matches - partial_matches,
            "exact_match_ratio": round(exact_match_ratio, 3),
            "coverage_ratio": round(coverage_ratio, 3),
            "skill_depth_score": round(depth_score, 3),
            "overall_compatibility": round((exact_match_ratio * 0.6 + coverage_ratio * 0.4), 3)
        }
    
    def _check_skill_similarity(self, skill1: str, skill2: str) -> bool:
        """Check if two skills are similar/related"""
        # Technology families and related skills
        skill_families = {
            'python': ['py', 'python', 'django', 'flask', 'pandas'],
            'javascript': ['js', 'javascript', 'node', 'react', 'vue', 'angular'],
            'web': ['html', 'css', 'css3', 'html5', 'sass', 'scss'],
            'salesforce': ['lightning', 'apex', 'lwc', 'lightning web components']
        }
        
        for family, skills in skill_families.items():
            if skill1 in skills and skill2 in skills:
                return True
        
        return False
    
    def _perform_skill_analysis(self, required_skills: list, employee_profile: dict) -> dict:
        """Perform detailed skill gap and strength analysis"""
        
        employee_skills = [skill.lower().strip() for skill in employee_profile.get('skills', [])]
        
        analysis = {
            "core_strengths": [],
            "skill_gaps": [],
            "transferable_skills": [],
            "learning_priorities": [],
            "skill_categories": {}
        }
        
        for req_skill in required_skills:
            req_skill_clean = req_skill.lower().strip()
            
            if req_skill_clean in employee_skills:
                analysis["core_strengths"].append(req_skill)
            elif any(self._check_skill_similarity(req_skill_clean, emp_skill) 
                    for emp_skill in employee_skills):
                analysis["transferable_skills"].append(req_skill)
            else:
                analysis["skill_gaps"].append(req_skill)
                analysis["learning_priorities"].append({
                    "skill": req_skill,
                    "priority": "high" if req_skill_clean in ['python', 'javascript', 'java'] else "medium",
                    "estimated_learning_time": self._estimate_learning_time(req_skill)
                })
        
        return analysis
    
    def _assess_experience_relevance(self, employee_profile: dict, required_skills: list, 
                                   task_context: dict = None) -> dict:
        """Assess how relevant employee's experience is to the requirements"""
        
        experience = employee_profile.get('experience', [])
        projects = employee_profile.get('projects', [])
        
        if not experience and not projects:
            return {"relevance_score": 0.0, "relevant_experience": [], "notes": "No experience data available"}
        
        relevant_items = []
        relevance_score = 0.0
        
        # Analyze experience entries
        for exp_item in experience:
            exp_text = str(exp_item).lower()
            skill_mentions = sum(1 for skill in required_skills if skill.lower() in exp_text)
            if skill_mentions > 0:
                relevant_items.append({
                    "type": "experience",
                    "item": exp_item,
                    "skill_matches": skill_mentions
                })
                relevance_score += skill_mentions / len(required_skills)
        
        # Analyze project history
        for project in projects:
            project_text = str(project).lower()
            skill_mentions = sum(1 for skill in required_skills if skill.lower() in project_text)
            if skill_mentions > 0:
                relevant_items.append({
                    "type": "project",
                    "item": project,
                    "skill_matches": skill_mentions
                })
                relevance_score += skill_mentions / len(required_skills)
        
        return {
            "relevance_score": round(min(relevance_score, 1.0), 3),
            "relevant_experience": relevant_items[:5],  # Top 5 most relevant
            "experience_depth": "high" if relevance_score > 0.7 else "medium" if relevance_score > 0.3 else "low"
        }
    
    def _estimate_learning_curve(self, skill_analysis: dict, employee_profile: dict) -> dict:
        """Estimate learning curve and ramp-up time"""
        
        core_strengths = len(skill_analysis["core_strengths"])
        skill_gaps = len(skill_analysis["skill_gaps"])
        transferable_skills = len(skill_analysis["transferable_skills"])
        
        # Base calculation
        if skill_gaps == 0:
            ramp_up_time = "immediate"
            difficulty = "easy"
        elif transferable_skills > skill_gaps:
            ramp_up_time = "1-2 weeks"
            difficulty = "moderate"
        elif core_strengths > 0:
            ramp_up_time = "2-4 weeks"
            difficulty = "moderate"
        else:
            ramp_up_time = "4-8 weeks"
            difficulty = "challenging"
        
        return {
            "ramp_up_time": ramp_up_time,
            "difficulty_level": difficulty,
            "learning_support_needed": skill_gaps > 2,
            "mentoring_recommended": skill_gaps > 3,
            "training_priorities": [item["skill"] for item in skill_analysis.get("learning_priorities", [])]
        }
    
    def _calculate_overall_rating(self, compatibility_score: dict, experience_match: dict, 
                                learning_curve: dict) -> dict:
        """Calculate overall employee rating for the task"""
        
        # Weighted scoring
        weights = {
            "skill_compatibility": 0.4,
            "experience_relevance": 0.3,
            "learning_ease": 0.3
        }
        
        skill_score = compatibility_score["overall_compatibility"]
        experience_score = experience_match["relevance_score"]
        
        # Learning ease score (inverse of difficulty)
        learning_ease_map = {"easy": 1.0, "moderate": 0.7, "challenging": 0.4}
        learning_score = learning_ease_map.get(learning_curve["difficulty_level"], 0.4)
        
        overall_score = (
            skill_score * weights["skill_compatibility"] +
            experience_score * weights["experience_relevance"] +
            learning_score * weights["learning_ease"]
        )
        
        # Determine rating category
        if overall_score >= 0.8:
            rating = "excellent"
        elif overall_score >= 0.65:
            rating = "good"
        elif overall_score >= 0.5:
            rating = "fair"
        else:
            rating = "poor"
        
        return {
            "overall_score": round(overall_score, 3),
            "rating_category": rating,
            "confidence_level": "high" if skill_score > 0.6 else "medium" if skill_score > 0.3 else "low"
        }
    
    def _skill_proficiency_score(self, skill: str, employee_profile: dict) -> float:
        """Calculate proficiency score for a specific skill"""
        employee_skills = [s.lower().strip() for s in employee_profile.get('skills', [])]
        skill_lower = skill.lower().strip()
        
        if skill_lower in employee_skills:
            return 1.0  # Full proficiency
        elif any(self._check_skill_similarity(skill_lower, emp_skill) for emp_skill in employee_skills):
            return 0.6  # Partial proficiency
        else:
            return 0.0  # No proficiency
    
    def _rank_candidates(self, evaluation_results: dict) -> list:
        """Rank candidates based on overall evaluation"""
        ranked = []
        
        for employee, results in evaluation_results.items():
            ranked.append({
                "employee_name": employee,
                "overall_score": results["overall_rating"]["overall_score"],
                "rating": results["overall_rating"]["rating_category"],
                "confidence": results["overall_rating"]["confidence_level"],
                "key_strengths": results["skill_analysis"]["core_strengths"],
                "ramp_up_time": results["learning_curve"]["ramp_up_time"]
            })
        
        # Sort by overall score (descending)
        ranked.sort(key=lambda x: x["overall_score"], reverse=True)
        
        # Add ranking position
        for i, candidate in enumerate(ranked):
            candidate["rank"] = i + 1
        
        return ranked
    
    def _generate_strategic_insights(self, evaluation_results: dict, required_skills: list, 
                                   task_context: dict = None) -> dict:
        """Generate strategic insights and recommendations"""
        
        if not evaluation_results:
            return {"error": "No evaluation data available"}
        
        # Find best candidate
        best_candidate = max(evaluation_results.items(), 
                           key=lambda x: x[1]["overall_rating"]["overall_score"])
        
        # Skill coverage analysis
        skill_coverage = {}
        for skill in required_skills:
            coverage_count = sum(1 for emp_data in evaluation_results.values()
                               if skill in emp_data["skill_analysis"]["core_strengths"])
            skill_coverage[skill] = {
                "employees_with_skill": coverage_count,
                "coverage_percentage": round(coverage_count / len(evaluation_results) * 100, 1)
            }
        
        return {
            "primary_recommendation": {
                "employee": best_candidate[0],
                "score": best_candidate[1]["overall_rating"]["overall_score"],
                "rationale": f"Highest compatibility score with {best_candidate[1]['learning_curve']['ramp_up_time']} ramp-up time"
            },
            "skill_coverage_summary": skill_coverage,
            "team_composition_advice": self._suggest_team_composition(evaluation_results),
            "risk_mitigation": self._suggest_risk_mitigation(evaluation_results, required_skills),
            "development_opportunities": self._identify_development_opportunities(evaluation_results)
        }
    
    def _suggest_team_composition(self, evaluation_results: dict) -> dict:
        """Suggest optimal team composition strategies"""
        scores = [data["overall_rating"]["overall_score"] for data in evaluation_results.values()]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        if max(scores) >= 0.8:
            return {
                "recommendation": "single_lead",
                "details": "Strong individual candidate identified - single assignment recommended"
            }
        elif avg_score >= 0.6:
            return {
                "recommendation": "paired_assignment",
                "details": "Consider pairing top candidates for knowledge sharing and risk mitigation"
            }
        else:
            return {
                "recommendation": "team_with_training",
                "details": "Multiple team members with dedicated training/mentoring support needed"
            }
    
    def _suggest_risk_mitigation(self, evaluation_results: dict, required_skills: list) -> list:
        """Suggest risk mitigation strategies"""
        suggestions = []
        
        # Check for critical skill gaps
        critical_gaps = {}
        for emp_name, data in evaluation_results.items():
            gaps = data["skill_analysis"]["skill_gaps"]
            for gap in gaps:
                critical_gaps[gap] = critical_gaps.get(gap, 0) + 1
        
        # Identify skills missing across all candidates
        universal_gaps = [skill for skill, count in critical_gaps.items() 
                         if count == len(evaluation_results)]
        
        if universal_gaps:
            suggestions.append(f"Critical training needed for: {', '.join(universal_gaps)}")
        
        # Check for low overall scores
        low_scores = [name for name, data in evaluation_results.items()
                     if data["overall_rating"]["overall_score"] < 0.5]
        
        if len(low_scores) == len(evaluation_results):
            suggestions.append("Consider external consultation or additional training before assignment")
        
        return suggestions
    
    def _identify_development_opportunities(self, evaluation_results: dict) -> list:
        """Identify development opportunities for employees"""
        opportunities = []
        
        for emp_name, data in evaluation_results.items():
            transferable = data["skill_analysis"]["transferable_skills"]
            if transferable:
                opportunities.append({
                    "employee": emp_name,
                    "opportunity": f"Leverage {', '.join(transferable)} for cross-skilling",
                    "development_path": "skill_enhancement"
                })
        
        return opportunities
    
    def _perform_risk_analysis(self, evaluation_results: dict, required_skills: list) -> dict:
        """Perform comprehensive risk analysis"""
        
        scores = [data["overall_rating"]["overall_score"] for data in evaluation_results.values()]
        
        return {
            "overall_risk_level": "low" if max(scores) > 0.7 else "medium" if max(scores) > 0.5 else "high",
            "skill_coverage_risks": self._assess_skill_coverage_risks(evaluation_results, required_skills),
            "timeline_risks": self._assess_timeline_risks(evaluation_results),
            "mitigation_strategies": self._generate_mitigation_strategies(evaluation_results)
        }
    
    def _assess_skill_coverage_risks(self, evaluation_results: dict, required_skills: list) -> list:
        """Assess risks related to skill coverage"""
        risks = []
        
        for skill in required_skills:
            coverage = sum(1 for data in evaluation_results.values()
                          if skill in data["skill_analysis"]["core_strengths"])
            
            if coverage == 0:
                risks.append(f"No employee has proficiency in {skill}")
            elif coverage == 1:
                risks.append(f"Single point of failure for {skill}")
        
        return risks
    
    def _assess_timeline_risks(self, evaluation_results: dict) -> list:
        """Assess timeline-related risks"""
        risks = []
        
        long_rampup = [name for name, data in evaluation_results.items()
                      if data["learning_curve"]["ramp_up_time"] in ["4-8 weeks", "8+ weeks"]]
        
        if len(long_rampup) == len(evaluation_results):
            risks.append("All candidates require extended ramp-up time")
        
        return risks
    
    def _generate_mitigation_strategies(self, evaluation_results: dict) -> list:
        """Generate mitigation strategies"""
        strategies = []
        
        # Check if mentoring is recommended for any candidate
        needs_mentoring = any(data["learning_curve"]["mentoring_recommended"] 
                            for data in evaluation_results.values())
        
        if needs_mentoring:
            strategies.append("Assign experienced mentor for knowledge transfer")
        
        strategies.append("Conduct skills assessment before final assignment")
        strategies.append("Plan for incremental task assignment during ramp-up period")
        
        return strategies
    
    def _create_execution_roadmap(self, ranked_candidates: list, evaluation_results: dict) -> dict:
        """Create execution roadmap based on evaluation"""
        
        if not ranked_candidates:
            return {"error": "No candidates to create roadmap"}
        
        top_candidate = ranked_candidates[0]
        top_eval = evaluation_results[top_candidate["employee_name"]]
        
        roadmap = {
            "immediate_actions": [
                f"Assign {top_candidate['employee_name']} as primary resource",
                "Conduct detailed skill assessment session"
            ],
            "week_1_activities": [],
            "ongoing_support": [],
            "success_metrics": [
                "Task completion within estimated timeframe",
                "Quality meets project standards",
                "Knowledge transfer to other team members"
            ]
        }
        
        # Add specific activities based on evaluation
        if top_eval["learning_curve"]["training_priorities"]:
            roadmap["week_1_activities"].append(
                f"Provide training on: {', '.join(top_eval['learning_curve']['training_priorities'][:3])}"
            )
        
        if top_eval["learning_curve"]["mentoring_recommended"]:
            roadmap["ongoing_support"].append("Weekly mentoring sessions")
        
        return roadmap
    
    def _estimate_learning_time(self, skill: str) -> str:
        """Estimate learning time for a specific skill"""
        skill_lower = skill.lower().strip()
        
        # Basic time estimates (this would be more sophisticated in production)
        quick_learn = ["css", "html", "scss", "sass"]
        medium_learn = ["javascript", "python", "vue", "react"]
        long_learn = ["java", "machine learning", "data science"]
        
        if any(quick in skill_lower for quick in quick_learn):
            return "1-2 weeks"
        elif any(medium in skill_lower for medium in medium_learn):
            return "3-4 weeks"
        elif any(long in skill_lower for long in long_learn):
            return "6-8 weeks"
        else:
            return "2-4 weeks"  # Default


def parse_get_employee_history_result(raw_result):
    """
    Parse the result from get_employee_history to extract normalized skills and employee data
    """
    # Initialize return structure
    parsed_result = {
        "normalized_skills": [],
        "employee_fetched_results": {}
    }
    
    # If raw_result is a list, we need to extract the information differently
    if isinstance(raw_result, list):
        # Try to parse the employee data from the list
        for item in raw_result:
            if isinstance(item, dict):
                # Look for employee data structure
                if 'employee_name' in item:
                    emp_name = item['employee_name']
                    parsed_result["employee_fetched_results"][emp_name] = {
                        "skills": item.get('skills', []),
                        "experience": item.get('experience', []),
                        "projects": item.get('projects', []),
                        "score": item.get('score', 0)
                    }
                # Look for skill information
                elif 'skills' in item:
                    parsed_result["normalized_skills"].extend(item['skills'])
    
    # If it's already a dict with the expected structure, return as is
    elif isinstance(raw_result, dict) and 'normalized_skills' in raw_result:
        return raw_result
    
    return parsed_result


# Integration example with the original SkillMatcher - FIXED VERSION
if __name__ == "__main__":
    from tools_camel.get_emp_history_tool import get_employee_history
    
    skill_evaluator = SkillEvaluator()
    
    # Test data
    employees = ["Kenneth Simpson", "Mark Jenkins"]
    test_input = ["py", "JS", "lightning web components", "css3", "Vue"]
    emp_db = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employee_with_ids.xlsx"
    
    # Method 1: Initial data gathering
    print("=== METHOD 1: Skill Matching & Data Gathering ===")
    raw_result = get_employee_history(employees, emp_db)
    
    # Debug: Print the raw result to understand its structure
    print(f"Raw result type: {type(raw_result)}")
    print(f"Raw result: {raw_result}")
    
    # Parse the result properly
    if isinstance(raw_result, list):
        # Create a mock structure based on the output we can see
        method1_result = {
            "normalized_skills": test_input,  # Use the test input skills
            "employee_fetched_results": {}
        }
        
        # Extract employee data from the raw result
        for item in raw_result:
            if isinstance(item, dict) and 'employee_name' in item:
                emp_name = item['employee_name']
                method1_result["employee_fetched_results"][emp_name] = {
                    "skills": item.get('matching_skills', []),
                    "experience": [],  # We'll need to get this from another source
                    "projects": [],    # We'll need to get this from another source
                    "score": item.get('score', 0)
                }
    else:
        # If it's already in the expected format
        method1_result = raw_result
    
    print(f"Normalized Skills: {method1_result['normalized_skills']}")
    print(f"Employees Fetched: {len(method1_result['employee_fetched_results'])}")
    
    # Only proceed if we have valid data
    if method1_result['employee_fetched_results']:
        # Method 2: Comprehensive evaluation and recommendations
        print("\n=== METHOD 2: Comprehensive Evaluation & Strategic Recommendations ===")
        method2_result = skill_evaluator.evaluate_employee_fit(
            normalized_skills=method1_result["normalized_skills"],
            employee_fetched_results=method1_result["employee_fetched_results"],
            task_context={"priority": "high", "deadline": "2025-08-15", "complexity": "medium"}
        )
        
        # Display key results
        print("\n📊 CANDIDATE RANKINGS:")
        for candidate in method2_result["candidate_rankings"]:
            print(f"  {candidate['rank']}. {candidate['employee_name']} - Score: {candidate['overall_score']} ({candidate['rating']})")
        
        print(f"\n🎯 PRIMARY RECOMMENDATION:")
        rec = method2_result["strategic_recommendations"]["primary_recommendation"]
        print(f"  Employee: {rec['employee']}")
        print(f"  Score: {rec['score']}")
        print(f"  Rationale: {rec['rationale']}")
        
        print(f"\n⚠️  RISK LEVEL: {method2_result['risk_opportunity_analysis']['overall_risk_level'].upper()}")
        
        print(f"\n📋 EXECUTION ROADMAP:")
        roadmap = method2_result["execution_roadmap"]
        print(f"  Immediate: {roadmap['immediate_actions']}")
        print(f"  Week 1: {roadmap.get('week_1_activities', [])}")
    else:
        print("❌ No employee data found to evaluate")