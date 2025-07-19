import json
import datetime
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class EmployeeScore:
    """Data class for employee scoring"""
    employee_id: str
    employee_name: str
    assignment_id: str
    performance_score: float
    quality_score: float
    timeliness_score: float
    overall_score: float
    feedback: str
    scored_by: str
    scored_at: datetime.datetime
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['scored_at'] = self.scored_at.isoformat()
        return data

@dataclass
class LogEntry:
    """Data class for log entries"""
    timestamp: datetime.datetime
    level: str
    category: str
    message: str
    data: Optional[Dict[str, Any]] = None
    
    def to_dict(self):
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data

class AssignmentCoordinatorAgent:
    """
    Assignment Coordinator Agent responsible for scoring employees and logging data
    """
    
    def __init__(self):
        self.agent_name = "assignment_coordinator"
        self.scores_storage = []
        self.logs_storage = []
        self.score_weights = {
            'performance': 0.4,
            'quality': 0.4,
            'timeliness': 0.2
        }
    
    def score_employee(self, 
                      employee_id: str,
                      employee_name: str,
                      assignment_id: str,
                      performance_score: float,
                      quality_score: float,
                      timeliness_score: float,
                      feedback: str = "",
                      scored_by: str = "system") -> Dict[str, Any]:
        """
        Score an employee based on their assignment performance
        
        Args:
            employee_id: Unique identifier for the employee
            employee_name: Name of the employee
            assignment_id: ID of the assignment being scored
            performance_score: Performance score (0-100)
            quality_score: Quality score (0-100)
            timeliness_score: Timeliness score (0-100)
            feedback: Optional feedback text
            scored_by: Who is providing the score
            
        Returns:
            Dict containing the scoring result
        """
        try:
            # Validate scores
            scores = [performance_score, quality_score, timeliness_score]
            if not all(0 <= score <= 100 for score in scores):
                raise ValueError("All scores must be between 0 and 100")
            
            # Calculate overall score using weights
            overall_score = (
                performance_score * self.score_weights['performance'] +
                quality_score * self.score_weights['quality'] +
                timeliness_score * self.score_weights['timeliness']
            )
            
            # Create employee score record
            employee_score = EmployeeScore(
                employee_id=employee_id,
                employee_name=employee_name,
                assignment_id=assignment_id,
                performance_score=performance_score,
                quality_score=quality_score,
                timeliness_score=timeliness_score,
                overall_score=round(overall_score, 2),
                feedback=feedback,
                scored_by=scored_by,
                scored_at=datetime.datetime.now()
            )
            
            # Store the score
            self.scores_storage.append(employee_score)
            
            # Log the scoring action
            self.log_data(
                level="INFO",
                category="employee_scoring",
                message=f"Employee {employee_name} scored for assignment {assignment_id}",
                data={
                    "employee_id": employee_id,
                    "assignment_id": assignment_id,
                    "overall_score": overall_score,
                    "scored_by": scored_by
                }
            )
            
            # Determine performance level
            if overall_score >= 90:
                performance_level = "Excellent"
            elif overall_score >= 80:
                performance_level = "Good"
            elif overall_score >= 70:
                performance_level = "Satisfactory"
            elif overall_score >= 60:
                performance_level = "Needs Improvement"
            else:
                performance_level = "Poor"
            
            result = {
                "success": True,
                "employee_score": employee_score.to_dict(),
                "performance_level": performance_level,
                "message": f"Successfully scored employee {employee_name}",
                "recommendations": self._get_recommendations(overall_score, performance_score, quality_score, timeliness_score)
            }
            
            logger.info(f"Employee {employee_name} scored: {overall_score}/100")
            return result
            
        except Exception as e:
            error_msg = f"Error scoring employee: {str(e)}"
            logger.error(error_msg)
            self.log_data("ERROR", "employee_scoring", error_msg, {
                "employee_id": employee_id,
                "assignment_id": assignment_id
            })
            return {
                "success": False,
                "error": error_msg,
                "employee_id": employee_id,
                "assignment_id": assignment_id
            }
    
    def log_data(self, 
                level: str,
                category: str,
                message: str,
                data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Log data for tracking and auditing purposes
        
        Args:
            level: Log level (INFO, WARNING, ERROR, DEBUG)
            category: Category of the log entry
            message: Log message
            data: Optional additional data to log
            
        Returns:
            Dict containing the log result
        """
        try:
            # Validate log level
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            if level.upper() not in valid_levels:
                level = "INFO"
            
            # Create log entry
            log_entry = LogEntry(
                timestamp=datetime.datetime.now(),
                level=level.upper(),
                category=category,
                message=message,
                data=data
            )
            
            # Store the log entry
            self.logs_storage.append(log_entry)
            
            # Also log to Python logger
            python_logger = getattr(logger, level.lower(), logger.info)
            log_message = f"[{category}] {message}"
            if data:
                log_message += f" | Data: {json.dumps(data, default=str)}"
            python_logger(log_message)
            
            return {
                "success": True,
                "log_entry": log_entry.to_dict(),
                "message": "Data logged successfully",
                "log_id": len(self.logs_storage) - 1
            }
            
        except Exception as e:
            error_msg = f"Error logging data: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "level": level,
                "category": category
            }
    
    def _get_recommendations(self, overall_score: float, performance_score: float, 
                           quality_score: float, timeliness_score: float) -> List[str]:
        """Generate recommendations based on scores"""
        recommendations = []
        
        if overall_score < 70:
            recommendations.append("Consider additional training or support")
        
        if performance_score < 70:
            recommendations.append("Focus on improving task execution and productivity")
        
        if quality_score < 70:
            recommendations.append("Implement quality control measures and review processes")
        
        if timeliness_score < 70:
            recommendations.append("Work on time management and deadline adherence")
        
        if overall_score >= 90:
            recommendations.append("Excellent performance - consider for advanced assignments")
        
        return recommendations
    
    def get_employee_scores(self, employee_id: Optional[str] = None, 
                          assignment_id: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve employee scores with optional filtering"""
        try:
            filtered_scores = self.scores_storage.copy()
            
            if employee_id:
                filtered_scores = [s for s in filtered_scores if s.employee_id == employee_id]
            
            if assignment_id:
                filtered_scores = [s for s in filtered_scores if s.assignment_id == assignment_id]
            
            return {
                "success": True,
                "scores": [score.to_dict() for score in filtered_scores],
                "count": len(filtered_scores)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error retrieving scores: {str(e)}"
            }
    
    def get_logs(self, category: Optional[str] = None, 
                level: Optional[str] = None,
                limit: int = 100) -> Dict[str, Any]:
        """Retrieve logs with optional filtering"""
        try:
            filtered_logs = self.logs_storage.copy()
            
            if category:
                filtered_logs = [log for log in filtered_logs if log.category == category]
            
            if level:
                filtered_logs = [log for log in filtered_logs if log.level == level.upper()]
            
            # Sort by timestamp (most recent first) and limit
            filtered_logs.sort(key=lambda x: x.timestamp, reverse=True)
            filtered_logs = filtered_logs[:limit]
            
            return {
                "success": True,
                "logs": [log.to_dict() for log in filtered_logs],
                "count": len(filtered_logs)
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error retrieving logs: {str(e)}"
            }
    
    def get_employee_statistics(self, employee_id: str) -> Dict[str, Any]:
        """Get statistical summary for an employee"""
        try:
            employee_scores = [s for s in self.scores_storage if s.employee_id == employee_id]
            
            if not employee_scores:
                return {
                    "success": False,
                    "error": "No scores found for employee"
                }
            
            overall_scores = [s.overall_score for s in employee_scores]
            
            stats = {
                "employee_id": employee_id,
                "employee_name": employee_scores[0].employee_name,
                "total_assignments": len(employee_scores),
                "average_score": round(sum(overall_scores) / len(overall_scores), 2),
                "highest_score": max(overall_scores),
                "lowest_score": min(overall_scores),
                "recent_scores": overall_scores[-5:] if len(overall_scores) >= 5 else overall_scores
            }
            
            return {
                "success": True,
                "statistics": stats
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error calculating statistics: {str(e)}"
            }

# Example usage
if __name__ == "__main__":
    # Initialize the assignment coordinator agent
    coordinator = AssignmentCoordinatorAgent()
    
    print("=== Assignment Coordinator Agent Demo ===\n")
    
    # Example 1: Score an employee
    print("1. Scoring an employee:")
    score_result = coordinator.score_employee(
        employee_id="EMP001",
        employee_name="John Doe",
        assignment_id="ASG123",
        performance_score=85,
        quality_score=90,
        timeliness_score=75,
        feedback="Good work overall, but needs to improve time management",
        scored_by="manager_001"
    )
    print(json.dumps(score_result, indent=2, default=str))
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Log some data
    print("2. Logging data:")
    log_result = coordinator.log_data(
        level="INFO",
        category="system_event",
        message="Assignment coordination process started",
        data={
            "process_id": "coord_001",
            "assignments_count": 5,
            "employees_involved": ["EMP001", "EMP002", "EMP003"]
        }
    )
    print(json.dumps(log_result, indent=2, default=str))
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Score another employee
    print("3. Scoring another employee:")
    score_result2 = coordinator.score_employee(
        employee_id="EMP002",
        employee_name="Jane Smith",
        assignment_id="ASG124",
        performance_score=95,
        quality_score=88,
        timeliness_score=92,
        feedback="Excellent performance across all metrics",
        scored_by="manager_001"
    )
    print(json.dumps(score_result2, indent=2, default=str))
    
    print("\n" + "="*50 + "\n")
    
    # Example 4: Get employee statistics
    print("4. Employee statistics:")
    stats = coordinator.get_employee_statistics("EMP001")
    print(json.dumps(stats, indent=2, default=str))
    
    print("\n" + "="*50 + "\n")
    
    # Example 5: Retrieve logs
    print("5. Recent logs:")
    logs = coordinator.get_logs(limit=3)
    print(json.dumps(logs, indent=2, default=str))