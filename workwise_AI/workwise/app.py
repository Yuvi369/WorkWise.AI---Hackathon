from flask import Flask, render_template, request, jsonify
from textwrap import dedent
import os
import json
import logging
from werkzeug.exceptions import BadRequest

# Import the business logic from main.py
from main import process_business_info, BizBuddyCrew

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)

# Set environment variable for the main.py to know we're running in web mode
os.environ['WEB_MODE'] = 'True'

# Create the app
app = Flask(__name__)

# Input validation function
def validate_form_data(data):
    required_fields = ['budget', 'business_type', 'selected_state', 
                      'selected_district', 'experience', 'availability',
                      'location_type', 'team_size']
    
    for field in required_fields:
        if not data.get(field):
            raise BadRequest(f"Missing required field: {field}")
    
    try:
        budget = float(data['budget'])
        if budget <= 0:
            raise ValueError("Budget must be positive")
    except (ValueError, TypeError):
        raise BadRequest("Invalid budget format. Must be a positive number")

@app.route('/')
def home():
    """Serve the HTML form."""
    try:
        return render_template('business_form.html')
    except Exception as e:
        logger.error(f"Error rendering home page: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/submit', methods=['POST'])
def submit():
    """Process form submission and pass data to the main business logic."""
    try:
        # Validate form data
        form_data = {
            'budget': request.form.get('budget'),
            'business_type': request.form.get('business_type') or request.form.get('other_business_type'),
            'selected_state': request.form.get('selected_state') or request.form.get('other_state'),
            'selected_district': request.form.get('selected_district') or request.form.get('other_district'),
            'experience': request.form.get('experience'),
            'availability': request.form.get('availability') or request.form.get('other_availability'),
            'location_type': request.form.get('location_type') or request.form.get('other_location_type'),
            'team_size': request.form.get('team_size')
        }
        
        validate_form_data(form_data)
        
        # Call the business logic function from main.py
        result = process_business_info(
            form_data['budget'],
            form_data['business_type'],
            form_data['selected_state'],
            form_data['selected_district'],
            form_data['experience'],
            form_data['availability'],
            form_data['location_type'],
            form_data['team_size']
        )
        
        # Save the result to a file for reference
        try:
            with open('business_info.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving business info: {str(e)}")
        
        # Return a JSON response for API usage or render a results template
        return render_template('results.html', result=result)
    
    except BadRequest as e:
        logger.warning(f"Bad request: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Error processing form submission: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/api/submit', methods=['POST'])
def api_submit():
    """API endpoint for programmatic access."""
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            raise BadRequest("No JSON data provided")
        
        validate_form_data(data)
        
        # Call the business logic function
        result = process_business_info(
            data.get('budget'),
            data.get('business_type'),
            data.get('selected_state'),
            data.get('selected_district'),
            data.get('experience'),
            data.get('availability'),
            data.get('location_type'),
            data.get('team_size')
        )
        
        # Return JSON response
        return jsonify({"status": "success", "data": result})
    
    except BadRequest as e:
        logger.warning(f"Bad request: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 400
    except Exception as e:
        logger.error(f"Error processing API submission: {str(e)}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    # Save the HTML form to the templates directory
    with open('templates/business_form.html', 'w', encoding='utf-8') as f:
        f.write(dedent("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BizBuddy Crew - Business Consultation</title>
    <style>
        :root {
            --primary: #4361ee;
            --primary-dark: #3a56d4;
            --secondary: #7209b7;
            --accent: #f72585;
            --light: #f8f9fa;
            --dark: #212529;
            --success: #38b000;
            --warning: #ffaa00;
            --error: #d00000;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: #f0f2f5;
            color: var(--dark);
            line-height: 1.6;
        }
        
        .container {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
        }
        
        .header h1 {
            color: var(--primary);
            font-size: 36px;
            margin-bottom: 10px;
            position: relative;
            display: inline-block;
        }
        
        .header h1::after {
            content: '';
            position: absolute;
            width: 50%;
            height: 4px;
            background: linear-gradient(to right, var(--primary), var(--accent));
            bottom: -10px;
            left: 25%;
            border-radius: 2px;
        }
        
        .header p {
            color: var(--dark);
            font-size: 18px;
            max-width: 600px;
            margin: 20px auto;
        }
        
        .form-card {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .form-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: var(--dark);
            font-size: 16px;
        }
        
        .form-control {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .form-control:focus {
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
        }
        
        .form-control:hover {
            border-color: #c0c0c0;
        }
        
        .radio-group, .checkbox-group {
            margin-top: 10px;
        }
        
        .radio-item, .checkbox-item {
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }
        
        .radio-item input, .checkbox-item input {
            margin-right: 10px;
            accent-color: var(--primary);
        }
        
        .btn {
            display: inline-block;
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .btn:hover {
            background-color: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(67, 97, 238, 0.4);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-submit {
            background: linear-gradient(to right, var(--primary), var(--secondary));
            width: 100%;
        }
        
        .submit-container {
            text-align: center;
        }
        
        .progress-indicator {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
        }
        
        .progress-step {
            flex: 1;
            text-align: center;
            position: relative;
        }
        
        .progress-step::before {
            content: '';
            height: 3px;
            width: 100%;
            background-color: #e0e0e0;
            position: absolute;
            top: 15px;
            left: 50%;
            z-index: 1;
        }
        
        .progress-step:last-child::before {
            display: none;
        }
        
        .step-number {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background-color: #e0e0e0;
            color: var(--dark);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 5px;
            position: relative;
            z-index: 2;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .step-number.active {
            background-color: var(--primary);
            color: white;
        }
        
        .step-title {
            font-size: 14px;
            color: #777;
            transition: all 0.3s ease;
        }
        
        .step-title.active {
            color: var(--primary);
            font-weight: 600;
        }
        
        .form-subtitle {
            color: var(--primary);
            margin-bottom: 20px;
            font-size: 20px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }
        
        .form-note {
            font-size: 14px;
            color: #777;
            margin-top: 5px;
        }
        
        .form-footer {
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            color: #777;
        }
        
        .custom-select {
            position: relative;
            display: block;
            width: 100%;
        }
        
        .custom-select select {
            display: block;
            width: 100%;
            padding: 12px 15px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            appearance: none;
            background-color: white;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .custom-select select:focus {
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
        }
        
        .custom-select select:hover {
            border-color: #c0c0c0;
        }
        
        .custom-select::after {
            content: '▼';
            font-size: 14px;
            color: #777;
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            pointer-events: none;
            transition: all 0.3s ease;
        }
        
        .custom-select:hover::after {
            color: var(--primary);
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
                margin: 20px auto;
            }
            
            .header h1 {
                font-size: 28px;
            }
            
            .form-card {
                padding: 20px;
            }
            
            .step-title {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>BizBuddy Crew</h1>
            <p>Need clarification for your Business? Great! This is the right place to get clarified. 
            Just provide the needed information to BizBuddy and we'll help you get started.</p>
        </div>
        
        <div class="progress-indicator">
            <div class="progress-step">
                <div class="step-number active">1</div>
                <div class="step-title active">Basic Info</div>
            </div>
            <div class="progress-step">
                <div class="step-number">2</div>
                <div class="step-title">Location</div>
            </div>
            <div class="progress-step">
                <div class="step-number">3</div>
                <div class="step-title">Experience</div>
            </div>
            <div class="progress-step">
                <div class="step-number">4</div>
                <div class="step-title">Operations</div>
            </div>
        </div>
        
        <form id="business-consultation" action="/submit" method="post">
            <div class="form-card">
                <h3 class="form-subtitle">Business Basics</h3>
                
                <div class="form-group">
                    <label for="budget">What is your planned budget (in INR) for starting the business?</label>
                    <input type="number" id="budget" name="budget" class="form-control" placeholder="Enter your budget in INR" required>
                    <div class="form-note">Please enter a numerical value without commas or symbols</div>
                </div>
                
                <div class="form-group">
                    <label for="business-type">What type of business are you planning to start?</label>
                    <div class="custom-select">
                        <select id="business-type" name="business_type" class="form-control" required>
                            <option value="" disabled selected>Choose a business type</option>
                            <option value="Retail">Retail</option>
                            <option value="Manufacturing">Manufacturing</option>
                            <option value="Service">Service</option>
                            <option value="E-commerce">E-commerce</option>
                            <option value="Other">Other (please specify)</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group" id="other-business-type-container" style="display: none;">
                    <label for="other-business-type">Please specify your business type:</label>
                    <input type="text" id="other-business-type" name="other_business_type" class="form-control" placeholder="Describe your business type">
                </div>
            </div>
            
            <div class="form-card">
                <h3 class="form-subtitle">Location Details</h3>
                
                <div class="form-group">
                    <label for="state">In which state do you plan to start your business?</label>
                    <div class="custom-select">
                        <select id="state" name="selected_state" class="form-control" required>
                            <option value="" disabled selected>Select a state</option>
                            <option value="Tamil Nadu">Tamil Nadu</option>
                            <option value="Andhra Pradesh">Andhra Pradesh</option>
                            <option value="Karnataka">Karnataka</option>
                            <option value="Kerala">Kerala</option>
                            <option value="Other">Other (please specify)</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group" id="other-state-container" style="display: none;">
                    <label for="other-state">Please specify the state:</label>
                    <input type="text" id="other-state" name="other_state" class="form-control" placeholder="Enter your state">
                </div>
                
                <div class="form-group">
                    <label for="district">In which district of the selected state will the business be located?</label>
                    <div class="custom-select">
                        <select id="district" name="selected_district" class="form-control" required>
                            <option value="" disabled selected>Select a district</option>
                            <!-- Districts will be populated based on state selection -->
                        </select>
                    </div>
                </div>
                
                <div class="form-group" id="other-district-container" style="display: none;">
                    <label for="other-district">Please specify the district:</label>
                    <input type="text" id="other-district" name="other_district" class="form-control" placeholder="Enter your district">
                </div>
            </div>
            
            <div class="form-card">
                <h3 class="form-subtitle">Experience & Skills</h3>
                
                <div class="form-group">
                    <label for="experience">Do you have any prior experience or skills relevant to the business?</label>
                    <textarea id="experience" name="experience" class="form-control" rows="4" placeholder="e.g., cooking, digital marketing, repair work, sales, etc." required></textarea>
                </div>
                
                <div class="form-group">
                    <label>How much time can you dedicate to running this business?</label>
                    <div class="radio-group">
                        <div class="radio-item">
                            <input type="radio" id="full-time" name="availability" value="Full-time" required>
                            <label for="full-time">Full-time</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" id="part-time" name="availability" value="Part-time">
                            <label for="part-time">Part-time</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" id="weekends" name="availability" value="Weekends only">
                            <label for="weekends">Weekends only</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" id="other-time" name="availability" value="Other">
                            <label for="other-time">Other</label>
                        </div>
                    </div>
                </div>
                
                <div class="form-group" id="other-availability-container" style="display: none;">
                    <label for="other-availability">Please specify your availability:</label>
                    <input type="text" id="other-availability" name="other_availability" class="form-control" placeholder="Describe your availability">
                </div>
            </div>
            
            <div class="form-card">
                <h3 class="form-subtitle">Business Operations</h3>
                
                <div class="form-group">
                    <label>Where do you plan to operate your business from?</label>
                    <div class="radio-group">
                        <div class="radio-item">
                            <input type="radio" id="home" name="location_type" value="Home" required>
                            <label for="home">Home</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" id="rented-shop" name="location_type" value="Rented Shop">
                            <label for="rented-shop">Rented Shop</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" id="online-only" name="location_type" value="Online only">
                            <label for="online-only">Online only</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" id="shared-workspace" name="location_type" value="Shared Workspace">
                            <label for="shared-workspace">Shared Workspace</label>
                        </div>
                        <div class="radio-item">
                            <input type="radio" id="other-location" name="location_type" value="Other">
                            <label for="other-location">Other</label>
                        </div>
                    </div>
                </div>
                
                <div class="form-group" id="other-location-container" style="display: none;">
                    <label for="other-location-type">Please specify your business location type:</label>
                    <input type="text" id="other-location-type" name="other_location_type" class="form-control" placeholder="Describe your business location">
                </div>
                
                <div class="form-group">
                    <label for="team-size">Are you planning to start this business alone or with a partner/team?</label>
                    <div class="custom-select">
                        <select id="team-size" name="team_size" class="form-control" required>
                            <option value="" disabled selected>Choose an option</option>
                            <option value="Alone">Alone (Solo Entrepreneur)</option>
                            <option value="With a partner">With a partner (2 people)</option>
                            <option value="Small team">Small team (3-5 people)</option>
                            <option value="Large team">Large team (more than 5 people)</option>
                        </select>
                    </div>
                </div>
            </div>
            
            <div class="submit-container">
                <button type="submit" class="btn btn-submit">Submit Consultation Request</button>
            </div>
            
            <div class="form-footer">
                <p>Your information is secure with us. We'll use it only to provide you with relevant business insights.</p>
            </div>
        </form>
    </div>
    
    <script>
        // Districts data for each state
        const districtsByState = {
            "Tamil Nadu": ["Madurai", "Chennai", "Theni", "Coimbatore", "Tirunelveli", "Salem", "Other"],
            "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Tirupati", "Guntur", "Kurnool", "Other"],
            "Karnataka": ["Bangalore", "Mysore", "Mangalore", "Hubli", "Belgaum", "Other"],
            "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Other"],
            "Other": ["Other"]
        };
        
        // Populate districts dropdown based on selected state
        document.getElementById('state').addEventListener('change', function() {
            const stateValue = this.value;
            const districtDropdown = document.getElementById('district');
            const otherStateContainer = document.getElementById('other-state-container');
            
            // Clear previous options
            districtDropdown.innerHTML = '<option value="" disabled selected>Select a district</option>';
            
            // Show/hide "Other" state input field
            if (stateValue === 'Other') {
                otherStateContainer.style.display = 'block';
            } else {
                otherStateContainer.style.display = 'none';
            }
            
            // Add new options based on selected state
            const districts = districtsByState[stateValue] || districtsByState['Other'];
            districts.forEach(district => {
                const option = document.createElement('option');
                option.value = district;
                option.textContent = district;
                districtDropdown.appendChild(option);
            });
        });
        
        // Handle "Other" district selection
        document.getElementById('district').addEventListener('change', function() {
            const districtValue = this.value;
            const otherDistrictContainer = document.getElementById('other-district-container');
            
            if (districtValue === 'Other') {
                otherDistrictContainer.style.display = 'block';
            } else {
                otherDistrictContainer.style.display = 'none';
            }
        });
        
        // Handle "Other" business type selection
        document.getElementById('business-type').addEventListener('change', function() {
            const businessTypeValue = this.value;
            const otherBusinessTypeContainer = document.getElementById('other-business-type-container');
            
            if (businessTypeValue === 'Other') {
                otherBusinessTypeContainer.style.display = 'block';
            } else {
                otherBusinessTypeContainer.style.display = 'none';
            }
        });
        
        // Handle "Other" availability selection
        const availabilityRadios = document.querySelectorAll('input[name="availability"]');
        availabilityRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                const otherAvailabilityContainer = document.getElementById('other-availability-container');
                
                if (this.value === 'Other') {
                    otherAvailabilityContainer.style.display = 'block';
                } else {
                    otherAvailabilityContainer.style.display = 'none';
                }
            });
        });
        
        // Handle "Other" location type selection
        const locationTypeRadios = document.querySelectorAll('input[name="location_type"]');
        locationTypeRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                const otherLocationContainer = document.getElementById('other-location-container');
                
                if (this.value === 'Other') {
                    otherLocationContainer.style.display = 'block';
                } else {
                    otherLocationContainer.style.display = 'none';
                }
            });
        });
    </script>
</body>
</html>"""))
    
    # Create a complete results template
    with open('templates/results.html', 'w', encoding='utf-8') as f:
        f.write(dedent("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BizBuddy Crew - Results</title>
    <style>
        :root {
            --primary: #4361ee;
            --primary-dark: #3a56d4;
            --secondary: #7209b7;
            --accent: #f72585;
            --light: #f8f9fa;
            --dark: #212529;
            --success: #38b000;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background-color: #f0f2f5;
            color: var(--dark);
            line-height: 1.6;
        }
        
        .container {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            position: relative;
        }
        
        .header h1 {
            color: var(--primary);
            font-size: 36px;
            margin-bottom: 10px;
            position: relative;
            display: inline-block;
        }
        
        .header h1::after {
            content: '';
            position: absolute;
            width: 50%;
            height: 4px;
            background: linear-gradient(to right, var(--primary), var(--accent));
            bottom: -10px;
            left: 25%;
            border-radius: 2px;
        }
        
        .header p {
            color: var(--dark);
            font-size: 18px;
            max-width: 600px;
            margin: 20px auto;
        }
        
        .result-card {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .result-subtitle {
            color: var(--primary);
            margin-bottom: 20px;
            font-size: 24px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }
        
        .result-item {
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .result-item:last-child {
            border-bottom: none;
        }
        
        .result-label {
            font-weight: 600;
            color: var(--secondary);
            margin-bottom: 5px;
        }
        
        .result-value {
            font-size: 16px;
            white-space: pre-line;
        }
        
        .btn {
            display: inline-block;
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-decoration: none;
        }
        
        .btn:hover {
            background-color: var(--primary-dark);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(67, 97, 238, 0.4);
        }
        
        .success-message {
            background-color: var(--success);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 30px;
            text-align: center;
            font-weight: 600;
        }
        
        .recommendations-section {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #f0f0f0;
        }
        
        .recommendations-header {
            font-size: 26px;
            color: var(--primary);
            margin-bottom: 20px;
            text-align: center;
        }
        
        .recommendation-content {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid var(--secondary);
            margin-bottom: 20px;
            white-space: pre-line;
        }
        
        .btn-container {
            text-align: center;
            margin-top: 30px;
        }
        
        .checklist {
            list-style-type: none;
            margin: 20px 0;
            padding: 0;
        }
        
        .checklist li {
            padding: 10px 0;
            position: relative;
            padding-left: 30px;
            border-bottom: 1px dashed #e0e0e0;
        }
        
        .checklist li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--success);
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
                margin: 20px auto;
            }
            
            .header h1 {
                font-size: 28px;
            }
            
            .result-card {
                padding: 20px;
            }
            
            .result-subtitle {
                font-size: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Your Business Consultation Results</h1>
            <p>Thank you for using BizBuddy Crew! Below are the insights and recommendations based on your input.</p>
        </div>
        
        <div class="success-message">
            Successfully processed your business consultation request!
        </div>
        
        <div class="result-card">
            <h2 class="result-subtitle">Submitted Information</h2>
            
            <div class="result-item">
                <div class="result-label">Budget</div>
                <div class="result-value">{{ result.budget }} INR</div>
            </div>
            
            <div class="result-item">
                <div class="result-label">Business Type</div>
                <div class="result-value">{{ result.business_type }}</div>
            </div>
            
            <div class="result-item">
                <div class="result-label">Location</div>
                <div class="result-value">{{ result.selected_district }}, {{ result.selected_state }}</div>
            </div>
            
            <div class="result-item">
                <div class="result-label">Experience</div>
                <div class="result-value">{{ result.experience }}</div>
            </div>
            
            <div class="result-item">
                <div class="result-label">Availability</div>
                <div class="result-value">{{ result.availability }}</div>
            </div>
            
            <div class="result-item">
                <div class="result-label">Location Type</div>
                <div class="result-value">{{ result.location_type }}</div>
            </div>
            
            <div class="result-item">
                <div class="result-label">Team Size</div>
                <div class="result-value">{{ result.team_size }}</div>
            </div>
        </div>
        
        <div class="recommendations-section">
            <h2 class="recommendations-header">Our Recommendations</h2>
            
            <div class="recommendation-content">
                {% if result.recommendations %}
                    {{ result.recommendations | safe }}
                {% else %}
                    Based on your input, our team recommends starting with a lean business model and focusing on validating your business idea through market research. Consider the following steps:
                    
                    <ul class="checklist">
                        <li>Conduct market research to validate demand</li>
                        <li>Develop a minimum viable product (MVP)</li>
                        <li>Create a detailed business plan</li>
                        <li>Explore local business support programs</li>
                        <li>Network with local entrepreneurs</li>
                    </ul>
                {% endif %}
            </div>
        </div>
        
        <div class="btn-container">
            <a href="/" class="btn">Start New Consultation</a>
        </div>
    </div>
</body>
</html>"""))
    
    app.run(debug=True, host='0.0.0.0', port=5000)