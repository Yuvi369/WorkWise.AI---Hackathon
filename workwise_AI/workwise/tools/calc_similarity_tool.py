from langchain.tools import tool
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
import re
from dataclasses import dataclass

from similarity_report import generate_html_report

@dataclass
class TicketRecord:
    """Data class for storing ticket information"""
    ticket_name: str
    description: str
    comments: str
    skills_used: List[str]
    employee_name: str
    resolution_time: Optional[float] = None
    complexity: Optional[str] = None

class EmployeeTicketManager:
    """Manages employee data and ticket history"""
    
    def __init__(self, base_file_path: str, history_file_path: str):
        self.base_file_path = base_file_path
        self.history_file_path = history_file_path
        self.employees_df = None
        self.ticket_history_df = None
        self.employee_ticket_records = {}
        self.load_data()
    
    def load_data(self):
        """Load employee base data and ticket history"""
        try:
            # Load employee base data (default sheet)
            self.employees_df = pd.read_excel(self.base_file_path)
            print(f"✅ Loaded {len(self.employees_df)} employees from base file")
            
            # Load ticket history from Sheet 2
            self.ticket_history_df = pd.read_excel(self.history_file_path, sheet_name=1)  # Sheet 2 (0-indexed)
            print(f"✅ Loaded {len(self.ticket_history_df)} ticket records from Sheet 2")
            
            # Process and organize data
            self._process_employee_data()
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def _process_employee_data(self):
        """Process and organize employee ticket data"""
        try:
            # Debug: Print column names
            print(f"📋 Base file columns: {list(self.employees_df.columns)}")
            print(f"📋 History file columns: {list(self.ticket_history_df.columns)}")
            
            # Use specific column names
            base_name_col = 'employee_name'
            history_name_col = 'assigned_to'
            
            # Verify columns exist
            if base_name_col not in self.employees_df.columns:
                raise ValueError(f"Column '{base_name_col}' not found in base file")
            if history_name_col not in self.ticket_history_df.columns:
                raise ValueError(f"Column '{history_name_col}' not found in history file")
            
            print(f"🔍 Using columns - Base: '{base_name_col}', History: '{history_name_col}'")
            
            # Get employee names from base file (normalize for comparison)
            base_employees = set(
                self.employees_df[base_name_col]
                .dropna()
                .astype(str)
                .str.strip()
                .str.lower()
            )
            
            # Get employee names from history file
            history_employees_raw = self.ticket_history_df[history_name_col].dropna()
            print(f"🔍 Raw assignee values: {history_employees_raw.head(10).tolist()}")
            print(f"🔍 Assignee column data type: {history_employees_raw.dtype}")
            print(f"🔍 Non-null assignee count: {len(history_employees_raw)}")
            
            history_employees = set(
                history_employees_raw
                .astype(str)
                .str.strip()
                .str.lower()
            )
            
            # Remove 'nan' values that might come from string conversion
            history_employees = {emp for emp in history_employees if emp != 'nan' and emp != ''}
            
            print(f"👥 Base file employees: {len(base_employees)}")
            print(f"🎫 History file employees: {len(history_employees)}")
            print(f"🤝 Matching employees: {len(base_employees.intersection(history_employees))}")
            
            # Show sample names for debugging
            print(f"📝 Sample base names: {list(base_employees)[:5]}")
            print(f"📝 Sample history names: {list(history_employees)[:5]}")
            
            # Create mapping for original case names
            employee_name_mapping = {}
            for _, row in self.employees_df.iterrows():
                original_name = str(row[base_name_col]).strip()
                normalized_name = original_name.lower()
                employee_name_mapping[normalized_name] = original_name
            
            # Group tickets by employee (only for employees in base file)
            processed_count = 0
            for _, row in self.ticket_history_df.iterrows():
                assigned_employee = str(row.get(history_name_col, '')).strip()
                
                if not assigned_employee or assigned_employee.lower() == 'nan':
                    continue
                
                # Check if employee exists in base file (case-insensitive)
                normalized_assigned = assigned_employee.lower()
                if normalized_assigned in base_employees:
                    
                    # Use original case name from base file
                    original_employee_name = employee_name_mapping[normalized_assigned]
                    
                    # Extract skills from various sources
                    skills_used = self._extract_skills(row)
                    
                    # Create ticket record with flexible column mapping
                    ticket_record = TicketRecord(
                        ticket_name=str(row.get('ticket_name', row.get('Ticket Name', row.get('title', '')))),
                        description=str(row.get('description', row.get('Description', row.get('summary', '')))),
                        comments=str(row.get('comments', row.get('Comments', row.get('Resolution', row.get('notes', ''))))),
                        skills_used=skills_used,
                        employee_name=original_employee_name,
                        resolution_time=row.get('resolution_time', row.get('Resolution Time')),
                        complexity=row.get('complexity', row.get('Complexity'))
                    )
                    
                    # Store in employee records
                    if original_employee_name not in self.employee_ticket_records:
                        self.employee_ticket_records[original_employee_name] = []
                    
                    self.employee_ticket_records[original_employee_name].append(ticket_record)
                    processed_count += 1
            
            print(f"✅ Processed {processed_count} tickets for {len(self.employee_ticket_records)} employees")
            
            # Show some sample processed data
            if self.employee_ticket_records:
                sample_employee = list(self.employee_ticket_records.keys())[0]
                sample_tickets = len(self.employee_ticket_records[sample_employee])
                print(f"📊 Sample: {sample_employee} has {sample_tickets} tickets")
                
                # Show sample ticket details
                if sample_tickets > 0:
                    sample_ticket = self.employee_ticket_records[sample_employee][0]
                    print(f"📋 Sample ticket: {sample_ticket.ticket_name}")
                    print(f"🔧 Skills used: {sample_ticket.skills_used[:5]}")  # Show first 5 skills
            
        except Exception as e:
            print(f"❌ Error processing employee data: {e}")
            raise
    
    def _detect_name_column(self, df: pd.DataFrame) -> str:
        """Auto-detect the employee name column"""
        possible_names = [
            'employee_name', 'Employee Name', 'name', 'Name', 
            'full_name', 'Full Name', 'employee', 'Employee',
            'assigned_to', 'Assigned To', 'assignee', 'Assignee'
        ]
        
        for col in possible_names:
            if col in df.columns:
                return col
        
        # If no exact match, look for columns containing 'name' or 'employee'
        for col in df.columns:
            if 'name' in col.lower() or 'employee' in col.lower():
                return col
        
        # Default to first column if nothing found
        return df.columns[0]
    
    def _extract_skills(self, row: pd.Series) -> List[str]:
        """Extract skills from ticket data"""
        skills = []
        
        # Common skill-related column names to check
        skill_columns = [
            'skills_used', 'Skills Used', 'skills', 'Skills',
            'primary_skills', 'Primary Skills', 'primary_skill', 'Primary Skill',
            'secondary_skills', 'Secondary Skills', 'secondary_skill', 'Secondary Skill',
            'technology_stack', 'Technology Stack', 'technologies', 'Technologies',
            'tools_used', 'Tools Used', 'tools', 'Tools',
            'programming_language', 'Programming Language', 'languages', 'Languages',
            'framework', 'Framework', 'frameworks', 'Frameworks',
            'database', 'Database', 'databases', 'Databases',
            'platform', 'Platform', 'platforms', 'Platforms'
        ]
        
        # Extract from skill columns
        for col in skill_columns:
            if col in row and pd.notna(row[col]):
                skill_text = str(row[col])
                # Split by common separators
                for separator in [',', ';', '|', '\n', '/']:
                    if separator in skill_text:
                        skills.extend(skill_text.split(separator))
                        break
                else:
                    skills.append(skill_text)
        
        # Extract skills from ticket description and comments
        text_fields = ['description', 'Description', 'comments', 'Comments', 'notes', 'Notes']
        combined_text = ""
        for field in text_fields:
            if field in row and pd.notna(row[field]):
                combined_text += " " + str(row[field])
        
        # Extract common technology keywords from text
        tech_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'git', 'github', 'gitlab', 'jira', 'confluence',
            'linux', 'windows', 'ubuntu', 'centos',
            'api', 'rest', 'graphql', 'microservices', 'devops',
            'tensorflow', 'pytorch', 'machine learning', 'ai', 'ml',
            'html', 'css', 'bootstrap', 'tailwind', 'sass',
            'sql', 'nosql', 'database', 'backend', 'frontend',
            's3', 'ec2', 'lambda', 'cloudformation', 'terraform'
        ]
        
        combined_text_lower = combined_text.lower()
        for keyword in tech_keywords:
            if keyword in combined_text_lower:
                skills.append(keyword)
        
        # Clean and normalize skills
        cleaned_skills = []
        for skill in skills:
            if skill and str(skill).strip():
                clean_skill = str(skill).strip().lower()
                # Remove common prefixes/suffixes
                clean_skill = clean_skill.replace('skill:', '').replace('tech:', '').strip()
                if clean_skill and len(clean_skill) > 1:
                    cleaned_skills.append(clean_skill)
        
        return list(set(cleaned_skills))  # Remove duplicates
    
    def get_employee_names(self) -> List[str]:
        """Get list of available employee names"""
        return list(self.employee_ticket_records.keys())
    
    def get_employee_history(self, employee_name: str) -> List[TicketRecord]:
        """Get ticket history for a specific employee"""
        return self.employee_ticket_records.get(employee_name, [])

@tool
def calculate_similarity(
    ticket_name: str, 
    description: str, 
    skill_sets: List[str], 
    employee_name: Optional[str] = None,
    base_file_path: str = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employees_db.xlsx",
    history_file_path: str = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\tkt_history_FS.xlsx"
) -> Dict[str, Any]:
    """
    Calculates similarity score between a new ticket and employee's past tickets.
    
    Args:
        ticket_name: Name of the current ticket
        description: Description of the current ticket
        skill_sets: List of skills required for the current ticket
        employee_name: Specific employee to check (optional)
        base_file_path: Path to employee base Excel file
        history_file_path: Path to ticket history Excel file
    
    Returns:
        Dictionary with similarity scores and recommendations
    """
    
    try:
        # Initialize manager
        manager = EmployeeTicketManager(base_file_path, history_file_path)
        
        # Prepare current ticket text
        current_ticket_text = f"{ticket_name} {description} {' '.join(skill_sets)}".lower()
        
        results = {}
        
        # If specific employee is provided
        if employee_name:
            if employee_name in manager.get_employee_names():
                score = _calculate_employee_similarity(
                    current_ticket_text, 
                    manager.get_employee_history(employee_name)
                )
                results[employee_name] = {
                    'similarity_score': score,
                    'ticket_count': len(manager.get_employee_history(employee_name)),
                    'past_tickets': [
                        {
                            'name': record.ticket_name,
                            'description': record.description[:100] + "..." if len(record.description) > 100 else record.description,
                            'skills': record.skills_used
                        }
                        for record in manager.get_employee_history(employee_name)[:5]  # Top 5 most recent
                    ]
                }
            else:
                results[employee_name] = {
                    'similarity_score': 0.0,
                    'error': 'Employee not found in database'
                }
        
        # Calculate for all employees
        else:
            employee_scores = []
            
            for emp_name in manager.get_employee_names():
                score = _calculate_employee_similarity(
                    current_ticket_text,
                    manager.get_employee_history(emp_name)
                )
                
                employee_scores.append({
                    'employee_name': emp_name,
                    'similarity_score': score,
                    'ticket_count': len(manager.get_employee_history(emp_name))
                })
            
            # Sort by similarity score
            employee_scores.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            # Get top 5 matches
            top_matches = employee_scores[:5]
            
            results = {
                'current_ticket': {
                    'name': ticket_name,
                    'description': description,
                    'skills_required': skill_sets
                },
                'top_matches': top_matches,
                'all_employees_count': len(employee_scores),
                'recommendations': _generate_recommendations(top_matches)
            }
        print(f"=============================================== {results}")
        generate_html_report(results)
        return results
        
    except Exception as e:
        return {
            'error': f"Similarity calculation failed: {str(e)}",
            'similarity_score': 0.0
        }

def _calculate_employee_similarity(current_ticket_text: str, past_tickets: List[TicketRecord]) -> float:
    """Calculate similarity between current ticket and employee's past tickets"""
    
    if not past_tickets:
        return 0.0
    
    try:
        # Combine past ticket texts
        past_ticket_texts = []
        for record in past_tickets:
            combined_text = f"{record.ticket_name} {record.description} {record.comments} {' '.join(record.skills_used)}".lower()
            past_ticket_texts.append(combined_text)
        
        # Create all documents
        all_docs = [current_ticket_text] + past_ticket_texts
        
        # Use TF-IDF vectorizer for better semantic understanding
        vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)  # Include bigrams for better context
        )
        
        # Fit and transform
        tfidf_matrix = vectorizer.fit_transform(all_docs)
        
        # Calculate cosine similarity
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        
        # Calculate weighted average (more recent tickets get higher weight)
        weights = np.linspace(1.0, 0.5, len(past_tickets))  # Recent tickets weighted higher
        weighted_score = np.average(similarities[0], weights=weights)
        
        return round(float(weighted_score), 3)
        
    except Exception as e:
        print(f"❌ Error in similarity calculation: {e}")
        return 0.0

def _generate_recommendations(top_matches: List[Dict]) -> List[str]:
    """Generate recommendations based on similarity scores"""
    recommendations = []
    
    if not top_matches:
        recommendations.append("No matching employees found in the database.")
        return recommendations
    
    best_match = top_matches[0]
    
    if best_match['similarity_score'] >= 0.7:
        recommendations.append(f"🎯 {best_match['employee_name']} is an excellent match with {best_match['similarity_score']:.1%} similarity")
    elif best_match['similarity_score'] >= 0.5:
        recommendations.append(f"✅ {best_match['employee_name']} is a good match with {best_match['similarity_score']:.1%} similarity")
    elif best_match['similarity_score'] >= 0.3:
        recommendations.append(f"⚠️ {best_match['employee_name']} has moderate relevance with {best_match['similarity_score']:.1%} similarity")
    else:
        recommendations.append("❌ No employees found with strong similarity to this ticket")
    
    # Add experience level recommendations
    high_exp_employees = [emp for emp in top_matches if emp['ticket_count'] >= 10]
    if high_exp_employees:
        recommendations.append(f"💼 Consider experienced employees: {', '.join([emp['employee_name'] for emp in high_exp_employees[:3]])}")
    
    return recommendations

# Example usage and testing
if __name__ == "__main__":
    # Test the similarity calculation
    test_ticket_name = "Database Backup Automation"
    test_description = "Set up automated daily backups for the production database to an S3 bucket."
    test_skills = ["AWS", "S3", "cloud computing", "storage services", "database management"]
    
    print("🔍 Testing Ticket Similarity Calculator")
    print("=" * 50)
    
    # Test with all employees
    results = calculate_similarity.func(
        ticket_name=test_ticket_name,
        description=test_description,
        skill_sets=test_skills
    )
    
    print("📊 Results:")
    if 'error' in results:
        print(f"❌ Error: {results['error']}")
    elif 'top_matches' in results:
        print(f"📋 Current Ticket: {results['current_ticket']['name']}")
        print(f"🎯 Top Matches:")
        for match in results['top_matches']:
            print(f"  • {match['employee_name']}: {match['similarity_score']:.1%} similarity ({match['ticket_count']} past tickets)")
        
        print(f"\n💡 Recommendations:")
        for rec in results['recommendations']:
            print(f"  {rec}")
    
    print("\n" + "=" * 50)
    print("✅ Similarity calculation completed!")