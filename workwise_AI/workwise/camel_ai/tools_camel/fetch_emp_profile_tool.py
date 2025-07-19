import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from langchain.tools import tool

# Load environment variables
load_dotenv()

def fetch_employee_profiles(employee_names: list, excel_file_path: str) -> list:
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
        if not os.path.exists(excel_file_path):
            print(f"❌ Excel file not found: {excel_file_path}")
            return []

        df = pd.read_excel(excel_file_path)

        required_columns = ['name', 'skill_name', 'create_date']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return []

        filtered_df = df[df['name'].isin(employee_names)]

        profiles = []
        current_date = datetime.now()

        for _, row in filtered_df.iterrows():
            try:
                create_date = pd.to_datetime(row['create_date'])
                experience_years = round((current_date - create_date).days / 365.25, 1)

                skills_raw = row['skill_name']
                if pd.isna(skills_raw):
                    skills_list = []
                elif isinstance(skills_raw, str):
                    skills_list = [skill.strip() for skill in skills_raw.split(',') if skill.strip()]
                else:
                    skills_list = [str(skills_raw)]

                profile = {
                    'employee_name': row['name'],
                    'skills_set': skills_list,
                    'experience_years': experience_years,
                    'create_date': create_date.strftime('%Y-%m-%d')
                }

                profiles.append(profile)

            except Exception as e:
                print(f"❌ Error processing employee {row.get('name', 'UNKNOWN')}: {str(e)}")
                continue

        found_employees = [profile['employee_name'] for profile in profiles]
        not_found = [name for name in employee_names if name not in found_employees]

        if not_found:
            print(f"⚠️  Employees not found in Excel: {not_found}")

        return profiles

    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        return []


def get_all_employee_profiles(excel_file_path: str = "employees.xlsx") -> dict:
    try:
        if not os.path.exists(excel_file_path):
            print(f"❌ Excel file not found: {excel_file_path}")
            return {}

        df = pd.read_excel(excel_file_path)

        required_columns = ['name', 'skills_name', 'create_date']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            print(f"Available columns: {list(df.columns)}")
            return {}

        employees_dict = {}
        current_date = datetime.now()

        for _, row in df.iterrows():
            try:
                create_date = pd.to_datetime(row['create_date'])
                experience_years = round((current_date - create_date).days / 365.25, 1)

                skills_raw = row['skills_name']
                if pd.isna(skills_raw):
                    skills_list = []
                elif isinstance(skills_raw, str):
                    skills_list = [skill.strip() for skill in skills_raw.split(',') if skill.strip()]
                else:
                    skills_list = [str(skills_raw)]

                employee_name = row['name']
                employees_dict[employee_name] = {
                    'skills_set': skills_list,
                    'experience_years': experience_years,
                    'create_date': create_date.strftime('%Y-%m-%d')
                }

            except Exception as e:
                print(f"❌ Error processing employee {row.get('name', 'UNKNOWN')}: {str(e)}")
                continue

        return employees_dict

    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        return {}


if __name__ == "__main__":
    # Test with specific employees
    employees = ["Brandon Castillo", "Mark Jenkins"]
    result = fetch_employee_profiles.func(employees, r"D:\ww_github\WorkWise.AI---Hackathon\workwise_AI\workwise\tools\datasets\employees_db_1.xlsx")
    print(f"**** {result}")
    #print("📄 Profiles:", result)
    