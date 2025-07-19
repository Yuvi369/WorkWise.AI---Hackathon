import pandas as pd
import os
from typing import List, Dict, Any, Callable
from datetime import datetime

def build_employee_profiles(
    employee_names: List[str],
    excel_path: str,
    leave_db_path: str,
    name_column: str = "name",
    designation_column: str = "job_title",
    default_department: str = "Development"
) -> List[Dict[str, str]]:
    """
    Build employee profile list from employee names by fetching data from Excel
    
    Args:
        employee_names: List of employee names
        excel_path: Path to Excel file containing employee data
        leave_db_path: Path to Excel file containing leave data
        name_column: Column name for employee names in Excel (default: "name")
        designation_column: Column name for job titles/designations in Excel (default: "job_title") 
        default_department: Default department to assign (default: "Development")
        
    Returns:
        List of employee profile dictionaries
    """
    try:
        print(f"🔍 Loading employee data from: {excel_path}")
        
        # Load Excel file
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
            
        df = pd.read_excel(excel_path)
        print(f"✅ Loaded Excel with {len(df)} rows")
        print(f"📋 Available columns: {list(df.columns)}")
        
        # Validate required columns
        if name_column not in df.columns:
            raise ValueError(f"Name column '{name_column}' not found. Available: {list(df.columns)}")
        if designation_column not in df.columns:
            raise ValueError(f"Designation column '{designation_column}' not found. Available: {list(df.columns)}")
        
        # Clean the name column for comparison
        df[name_column] = df[name_column].astype(str).str.strip()
        
        # Create a lookup dictionary (case-insensitive)
        name_to_designation = {}
        for idx, row in df.iterrows():
            clean_name = str(row[name_column]).strip().lower()
            designation = str(row[designation_column]).strip()
            name_to_designation[clean_name] = designation
        
        print(f"📊 Created lookup for {len(name_to_designation)} employees")
        
        # Get availability data for all employees at once
        print("🔍 Checking availability for all employees...")
        availability_results = check_availability(employee_names, leave_db_path, excel_path)
        
        # Create availability lookup
        availability_lookup = {}
        for result in availability_results:
            emp_name = result.get("employee_name", "")
            status = result.get("status", "unknown")
            message = result.get("message", "")
            
            # Convert status to simple availability
            if status == "available":
                availability_lookup[emp_name.lower()] = "Available"
            elif status == "unavailable":
                availability_lookup[emp_name.lower()] = "Unavailable"
            else:
                availability_lookup[emp_name.lower()] = "Unknown"
        
        # Build employee profiles
        employee_profiles = []
        
        print("\n🔍 Processing employees:")
        print("=" * 50)
        
        for emp_name in employee_names:
            clean_name = str(emp_name).strip()
            lookup_name = clean_name.lower()
            
            # Get designation from Excel or set default
            if lookup_name in name_to_designation:
                designation = name_to_designation[lookup_name]
                print(f"✅ Found '{clean_name}' -> Designation: '{designation}'")
            else:
                designation = "Unknown"  # Default for employees not in Excel
                print(f"❌ '{clean_name}' not found in Excel -> Using default designation")
            
            # Get availability from lookup
            availability = availability_lookup.get(lookup_name, "Unknown")
            print(f"   📅 Availability: {availability}")
            
            # Create employee profile
            profile = {
                "employee_name": clean_name,
                "designation": designation,
                "department": default_department,
                "availability": availability
            }
            
            employee_profiles.append(profile)
            print(f"   ✅ Profile created for '{clean_name}'")
        
        print("=" * 50)
        print(f"📈 Summary: Created {len(employee_profiles)} employee profiles")
        
        return employee_profiles
        
    except Exception as e:
        print(f"❌ Error building employee profiles: {e}")
        # Return basic profiles with error info
        fallback_profiles = []
        for emp_name in employee_names:
            fallback_profiles.append({
                "employee_name": str(emp_name).strip(),
                "designation": "Unknown",
                "department": default_department,
                "availability": "Unknown"
            })
        return fallback_profiles

def check_availability(employee_names: list, leave_db: str, emp_db: str) -> list:
    """
    Checks if each employee is currently available based on HRMS data.
    Returns a list of status dicts for each employee.
    """
    try:
        print(f"📋 Loading employee database: {emp_db}")
        print(f"📋 Loading leave database: {leave_db}")
        
        # Load Excel files
        employee_df = pd.read_excel(emp_db)
        leave_df = pd.read_excel(leave_db)
        
        # Get current date
        current_date = datetime.now().date()
        print(f"📅 Current date: {current_date}")
        
        results = []
        
        for employee_name in employee_names:
            result = {"employee_name": employee_name}
            
            # Step 1: Check if employee exists in employee excel
            employee_row = employee_df[employee_df['name'].str.strip().str.lower() == employee_name.strip().lower()]
            
            if employee_row.empty:
                result["status"] = "error"
                result["message"] = f"Employee '{employee_name}' not found in employee database"
                results.append(result)
                continue
            
            # Step 2: Get employee ID (column name is 'id' in employee file)
            employee_id = employee_row.iloc[0]['id']
            print(f"   👤 {employee_name} -> ID: {employee_id}")
            
            # Step 3: Check leave status using employee ID (column name is 'employee_id' in leave file)
            leave_row = leave_df[leave_df['employee_id'] == employee_id]
            
            if leave_row.empty:
                result["status"] = "available"
                result["message"] = "Employee available for assigning tickets"
                results.append(result)
                continue
            
            # Step 4: Check state column for confirmed leaves
            confirmed_leaves = leave_row[leave_row['state'].str.strip().str.lower() == 'confirm']
            
            if confirmed_leaves.empty:
                result["status"] = "available"
                result["message"] = "Employee available for assigning tickets"
                results.append(result)
                continue
            
            # Step 5: Check if any confirmed leave covers current date
            employee_on_leave = False
            return_date = None
            
            for _, leave in confirmed_leaves.iterrows():
                # Convert date_to to datetime if it's not already
                if pd.notna(leave['date_to']):
                    if isinstance(leave['date_to'], str):
                        date_to = datetime.strptime(leave['date_to'], '%Y-%m-%d').date()
                    else:
                        date_to = leave['date_to'].date() if hasattr(leave['date_to'], 'date') else leave['date_to']
                    
                    # Check if current date is within leave period
                    if current_date <= date_to:
                        employee_on_leave = True
                        # Find the latest return date
                        if return_date is None or date_to > return_date:
                            return_date = date_to
            
            if employee_on_leave:
                # Calculate days until return (return date + 1 day)
                next_available_date = return_date + pd.Timedelta(days=1)
                result["status"] = "unavailable"
                result["message"] = f"Selected employee is not available till {next_available_date.strftime('%d-%m-%Y')}"
            else:
                result["status"] = "available"
                result["message"] = "Employee available for assigning tickets"
            
            results.append(result)
            
    except FileNotFoundError as e:
        return [{"status": "error", "message": f"Excel file not found: {e}"}]
    except Exception as e:
        return [{"status": "error", "message": f"Error processing data: {str(e)}"}]
    
    return results

# Usage example
if __name__ == "__main__":
    # Your employee list
    employees = ["Kenneth Simpson", "1234yuva", "Mark Jenkins"]
    
    # Path to your Excel files
    leave_db = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\Final_Employees_Leave_Table.xlsx"
    emp_db = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employee_with_ids.xlsx"
    
    # Build employee profiles
    employee_profiles = build_employee_profiles(
        employee_names=employees,
        excel_path=emp_db,
        leave_db_path=leave_db,
        name_column="name",
        designation_column="job_title",
        default_department="Development"
    )
    
    # Print results
    print("\n🎯 Final Employee Profiles:")
    print("=" * 60)
    for i, profile in enumerate(employee_profiles, 1):
        print(f"{i}. {profile}")
    
    print(f"\n📊 Total profiles created: {len(employee_profiles)}")