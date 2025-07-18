import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from langchain.tools import tool

# Load environment variables
load_dotenv()

@tool
def fetch_employee_profiles(employee_names: list, excel_file_path: str = r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employees_db_1.xlsx") -> list:
    """
    Fetches employee profile information from Excel file for the given employee names.
    Calculates experience based on create_date column and extracts skills_set.
    
    Args:
        employee_names (list): List of employee names to fetch profiles for
        excel_file_path (str): Path to the Excel file containing employee data
    
    Returns:
        list: List of profile dictionaries with employee_name, skills_set, and experience_years
    """
    try:
        # Check if Excel file exists
        if not os.path.exists(excel_file_path):
            print(f"❌ Excel file not found: {excel_file_path}")
            return []
        
        # Read Excel file
        df = pd.read_excel(excel_file_path)
        
        # Check required columns
        required_columns = ['employee_name', 'skills_set', 'create_date']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return []
        
        # Filter dataframe for requested employees
        filtered_df = df[df['employee_name'].isin(employee_names)]
        
        profiles = []
        current_date = datetime.now()
        
        for _, row in filtered_df.iterrows():
            try:
                # Parse create_date
                create_date = pd.to_datetime(row['create_date'])
                
                # Calculate experience in years
                experience_years = (current_date - create_date).days / 365.25
                experience_years = round(experience_years, 1)
                
                # Extract skills (handle different formats)
                skills_set = row['skills_set']
                if pd.isna(skills_set):
                    skills_list = []
                elif isinstance(skills_set, str):
                    # Handle comma-separated skills or other formats
                    skills_list = [skill.strip() for skill in skills_set.split(',') if skill.strip()]
                else:
                    skills_list = [str(skills_set)]
                
                profile = {
                    'employee_name': row['employee_name'],
                    'skills_set': skills_list,
                    'experience_years': experience_years,
                    'create_date': create_date.strftime('%Y-%m-%d')
                }
                
                profiles.append(profile)
                
            except Exception as e:
                print(f"❌ Error processing employee {row['employee_name']}: {str(e)}")
                continue
        
        # Check for employees not found
        found_employees = [profile['employee_name'] for profile in profiles]
        not_found = [name for name in employee_names if name not in found_employees]
        
        if not_found:
            print(f"⚠️  Employees not found in Excel: {not_found}")
        
        return profiles
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        return []

def get_all_employee_profiles(excel_file_path: str = "employees.xlsx") -> dict:
    """
    Gets all employee profiles from Excel file and returns as a dictionary.
    
    Args:
        excel_file_path (str): Path to the Excel file containing employee data
    
    Returns:
        dict: Dictionary with employee names as keys and profile info as values
    """
    try:
        # Check if Excel file exists
        if not os.path.exists(excel_file_path):
            print(f"❌ Excel file not found: {excel_file_path}")
            return {}
        
        # Read Excel file
        df = pd.read_excel(excel_file_path)
        
        # Check required columns
        required_columns = ['employee_name', 'skills_set', 'create_date']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return {}
        
        employees_dict = {}
        current_date = datetime.now()
        
        for _, row in df.iterrows():
            try:
                # Parse create_date
                create_date = pd.to_datetime(row['create_date'])
                
                # Calculate experience in years
                experience_years = (current_date - create_date).days / 365.25
                experience_years = round(experience_years, 1)
                
                # Extract skills (handle different formats)
                skills_set = row['skills_set']
                if pd.isna(skills_set):
                    skills_list = []
                elif isinstance(skills_set, str):
                    # Handle comma-separated skills or other formats
                    skills_list = [skill.strip() for skill in skills_set.split(',') if skill.strip()]
                else:
                    skills_list = [str(skills_set)]
                
                employee_name = row['employee_name']
                employees_dict[employee_name] = {
                    'skills_set': skills_list,
                    'experience_years': experience_years,
                    'create_date': create_date.strftime('%Y-%m-%d')
                }
                
            except Exception as e:
                print(f"❌ Error processing employee {row['employee_name']}: {str(e)}")
                continue
        
        return employees_dict
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        return {}

if __name__ == "__main__":
    # Test with specific employees
    employees = ["Brandon Castillo", "Mark Jenkins"]
    result = fetch_employee_profiles.func(employees, r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employees_db_1.xlsx")
    print("📄 Profiles:", result)
    
    # Test getting all employees
    # print("\n" + "="*50)
    # all_employees = get_all_employee_profiles("employees.xlsx")
    # print("📄 All Employees:", all_employees)
    
    # # Example of expected Excel structure
    # print("\n" + "="*50)
    # print("📋 Expected Excel Structure:")
    # print("Columns required:")
    # print("- employee_name: Full name of the employee")
    # print("- skills_set: Comma-separated skills (e.g., 'Python, AWS, Docker')")
    # print("- create_date: Date when employee joined (YYYY-MM-DD or any date format)")
    # print("\nExample data:")
    # print("| employee_name  | skills_set              | create_date |")
    # print("|----------------|-------------------------|-------------|")
    # print("| Mark Jenkins   | Python, AWS, Docker     | 2020-01-15  |")
    # print("| Brandon Castillo | Java, Spring, MySQL   | 2019-06-20  |")