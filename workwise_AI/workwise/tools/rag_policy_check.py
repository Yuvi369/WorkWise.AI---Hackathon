import pandas as pd
from langchain.tools import tool
from policy_report import generate_html_report
from rag_sys.rag.main import RAG
import os
from typing import Dict, List, Any
import json

def load_employee_excel(excel_path: str, name_column: str = "name") -> pd.DataFrame:
    """
    Load employee data from Excel file
    
    Args:
        excel_path: Path to the Excel file
        name_column: Column name containing employee names
        
    Returns:
        DataFrame with employee data
    """
    try:
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
            
        df = pd.read_excel(excel_path)
        
        if name_column not in df.columns:
            raise ValueError(f"Column '{name_column}' not found in Excel file. Available columns: {list(df.columns)}")
            
        # Clean the name column - remove extra spaces and convert to lowercase for comparison
        df[name_column] = df[name_column].astype(str).str.strip().str.lower()
        
        print(f"✅ Loaded {len(df)} employees from Excel file")
        return df
        
    except Exception as e:
        print(f"❌ Error loading Excel file: {e}")
        return pd.DataFrame()

def validate_employee_name(employee_name: str, employee_df: pd.DataFrame, name_column: str = "name") -> bool:
    """
    Check if employee name exists in the Excel file
    
    Args:
        employee_name: Name to validate
        employee_df: DataFrame containing employee data
        name_column: Column name containing employee names
        
    Returns:
        True if name exists, False otherwise
    """
    if employee_df.empty:
        return False
        
    # Clean the input name for comparison
    clean_name = str(employee_name).strip().lower()
    
    # Check if name exists in the DataFrame
    return clean_name in employee_df[name_column].values

@tool
def rag_policy_checker(
    ticket_name: str, 
    ticket_id: str, 
    ticket_description: str, 
    employee_profile: List[Dict], 
    excel_path: str = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employees_leave_1.xlsx",
    name_column: str = "name"
) -> Dict[str, Any]:
    """
    Checks if the employee can be assigned to the ticket based on HR policies using RAG.
    Now includes Excel validation and tracks checked employees.
    
    Args:
        ticket_name: Name of the ticket
        ticket_id: ID of the ticket  
        ticket_description: Description of the ticket
        employee_profile: List of employee dictionaries
        excel_path: Path to Excel file containing valid employee names
        name_column: Column name in Excel that contains employee names
        
    Returns:
        Dictionary containing:
        - checked_employees: List of employees that were validated and processed
        - skipped_employees: List of employees that were skipped (not in Excel)
        - extracted_data: RAG results and sources
        - summary: Processing summary
    """
    try:
        # Load employee data from Excel
        employee_df = load_employee_excel(excel_path, name_column)
        
        # Lists to track processing
        checked_employees = []
        skipped_employees = []
        all_extracted_data = []
        
        print("🔍 Starting employee validation and policy checking...")
        print("="*60)
        
        # Process each employee
        for employee in employee_profile:
            employee_name = employee.get("employee_name", "")
            
            # Validate employee name against Excel
            if validate_employee_name(employee_name, employee_df, name_column):
                print(f"✅ Employee '{employee_name}' found in Excel - Processing...")
                
                # Add to checked employees list
                checked_employees.append(employee)
                
                # Prepare input for RAG
                embedded_input = f"""
                    ticket_name : {ticket_name},
                    ticket_id : {ticket_id},
                    ticket_description : {ticket_description},
                    employee_profile : {employee}
                """
                
                # Run RAG for this employee
                rag_obj = RAG()
                result = rag_obj.rag_agent_main(embedded_input)
                # Extract sources and add employee info
                sources = result.get("sources", [])    

                if sources:
                    source = sources[0]  # Just take the first one (or combine if needed)
                    extracted_data = [{
                        "employee_name": employee_name,
                        "employee_designation": employee.get("designation", "N/A"),
                        "employee_department": employee.get("department", "N/A"),
                        "employee_availability": employee.get("availability", "N/A"),
                        "pdf_name": source.get("pdf_name"),
                        "pg_no": source.get("page_number"),
                        "rag_flag": result.get("flag", 0),
                        "rag_response": result.get("decision", "No decision")
                    }]
                    all_extracted_data.extend(extracted_data)




                # extracted_data = [
                #     {
                #         "employee_name": employee_name,
                #         "employee_designation": employee.get("designation", "N/A"),
                #         "employee_department": employee.get("department", "N/A"),
                #         "employee_availability": employee.get("availability", "N/A"),
                #         "pdf_name": source.get("pdf_name"),
                #         "pg_no": source.get("page_number"),
                #         #"source": source.get("page_content"),
                #         "rag_flag": result.get("flag", 0),
                #         "rag_response": result.get("decision", "No decision")
                #     }
                #     for source in sources
                # ]


                # all_extracted_data.extend(extracted_data)
                
            else:
                print(f"❌ Employee '{employee_name}' not found in Excel - Skipping...")
                skipped_employees.append(employee)
        
        print("="*60)
        print(f"📈 Processing Summary:")
        print(f"   ✅ Checked employees: {len(checked_employees)}")
        print(f"   ❌ Skipped employees: {len(skipped_employees)}")
        print(f"   📄 Total policy matches: {len(all_extracted_data)}")
        print("="*60)
        
        # Generate HTML report if we have data
        if all_extracted_data:
            print("*=*" * 60)
            print(all_extracted_data)
            print("*=*" * 60)
            generate_html_report(all_extracted_data)
            print("📊 HTML report generated successfully!")
        else:
            print("⚠️  No valid employees found - No report generated")
        
        # Return comprehensive results
        return {
            "checked_employees": checked_employees,
            "skipped_employees": skipped_employees,
            "extracted_data": all_extracted_data,
            "summary": {
                "total_employees": len(employee_profile),
                "checked_count": len(checked_employees),
                "skipped_count": len(skipped_employees),
                "policy_matches": len(all_extracted_data),
                "excel_file": excel_path
            }
        }
        
    except Exception as e:
        print(f"❌ RAG Policy Checker Failed: {e}")
        return {
            "checked_employees": [],
            "skipped_employees": employee_profile,
            "extracted_data": [],
            "summary": {
                "error": str(e),
                "total_employees": len(employee_profile),
                "checked_count": 0,
                "skipped_count": len(employee_profile),
                "policy_matches": 0
            }
        }

def create_sample_excel(excel_path: str = "employees.xlsx"):
    """
    Create a sample Excel file for testing
    """
    sample_data = {
        "name": ["divya", "vasanthakumar b", "john doe", "jane smith", "alice johnson"],
        "employee_id": ["EMP001", "EMP002", "EMP003", "EMP004", "EMP005"],
        "department": ["Development", "Development", "Testing", "HR", "Development"],
        "designation": ["Intern", "Senior Developer", "Tester", "HR Manager", "Developer"]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_excel(excel_path, index=False)
    print(f"✅ Sample Excel file created: {excel_path}")
    return excel_path

if __name__ == "__main__":
    # Create sample Excel file for testing
    #excel_file = create_sample_excel()
    
    ticket_name = "UI Production fix"
    ticket_id = "FD - 0089"
    ticket_description = "Fix UI padding and button alignment in LWC component."
    
    # Fixed the employee_profile structure (was incorrectly using set syntax)
    employee_profile = [
        {
            "employee_name": "Alexander Rush",
            "designation": "Intern",
            "department": "Development",
            "availability": "Available"
        },
        {
            "employee_name": "1234yuva",  # This should be skipped (not in Excel)
            "designation": "Intern",
            "department": "Development",
            "availability": "Unavailable" 
        },
        {
            "employee_name": "Erik Ellison",
            "designation": "Senior Developer",
            "department": "Development",
            "availability": "Available"
        }
    ]
    
    # Run the policy checker
    results = rag_policy_checker.func(
        ticket_name=ticket_name,
        ticket_id=ticket_id,
        ticket_description=ticket_description,
        employee_profile=employee_profile,
        excel_path=r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employees_leave_1.xlsx",
        name_column="name"
    )
    
    print("\\n🔍 Final Results:")
    print(f"✅ Checked employees: {len(results['checked_employees'])}")
    print(f"❌ Skipped employees: {len(results['skipped_employees'])}")
    print(f"📄 Policy matches found: {len(results['extracted_data'])}")
    
    # Print checked employees
    if results['checked_employees']:
        print("\\n✅ Processed employees:")
        for emp in results['checked_employees']:
            print(f"   - {emp['employee_name']} ({emp['designation']})")
    
    # Print skipped employees  
    if results['skipped_employees']:
        print("\\n❌ Skipped employees:")
        for emp in results['skipped_employees']:
            print(f"   - {emp['employee_name']} (not found in Excel)")