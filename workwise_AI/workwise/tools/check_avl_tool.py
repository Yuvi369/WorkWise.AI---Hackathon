import pandas as pd
from datetime import datetime
from langchain.tools import tool

from tools.availability_report import generate_html_report

@tool
def check_availability(employee_names: list, leave_db, emp_db) -> list:
    """
    Checks if each employee is currently available based on HRMS data.
    Returns a list of status dicts for each employee.
    """
    try:
        # Load Excel files
        employee_df = pd.read_excel(emp_db)
        leave_df = pd.read_excel(leave_db)
        
        # Get current date
        current_date = datetime.now().date()
        
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
    generate_html_report(results)
    return results


if __name__ == "__main__":
    employees = ["Mark Jenkins", "Kenneth Simpson", "Anthony Wright"]
    leave_db = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\Final_Employees_Leave_Table.xlsx"
    emp_db = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employee_with_ids.xlsx"
    res = check_availability.func(employees, leave_db, emp_db)
    for r in res:
        print(r)