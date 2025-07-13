from flask import Flask, request, jsonify
import os
import json
import logging
from werkzeug.exceptions import BadRequest

# Import the business logic from main.py
from main import process_business_info, BizBuddyCrew

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment variable for the main.py to know we're running in web mode
os.environ['WEB_MODE'] = 'True'

# Create the app
app = Flask(__name__)

# Input validation function
def validate_json_data(data):
    """Validate the incoming JSON data"""
    required_fields = ['ticket_name', 'ticket_id', 'priority', 
                      'description',
                      'Project', 'Days_to_complete', 'department']
    
    optional_fileds = ['required_skills', 'suggested_employees', ]
    
    # {
    # "ticket_name": "Fix the bug in LWC",
    # "ticket_id": "AA-204",
    # "priority": "Medium",
    # "description": "We are facing issue in the button position and description box position. Please fix this ASAP.",
    # "required_skills": ["LWC", "JS"],
    # "suggested_employees": ["Vasanth", "Akash", "Yuvaraj"],
    # "Project": "Salesforce",
    # "Days_to_complete": "Should be done within 2 days",
    # "department": "Development"
    # }

    
    # Check if data is a dictionary
    if not isinstance(data, dict):
        raise BadRequest("Invalid JSON format. Expected a JSON object.")
    
    # Check for required fields
    missing_fields = []
    for field in required_fields:
        if field not in data or not data.get(field):
            missing_fields.append(field)
    
    if missing_fields:
        print(f'Some mandatory fields are missing. Need this  {missing_fields}')
        raise BadRequest(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Validate budget
    try:
        complete_days = data['Days_to_complete']
        if complete_days <= 0:
            raise ValueError("Days to complete must be positive")
    except (ValueError, TypeError):
        raise BadRequest("Invalid Days to complete format. Must be a positive number")
    
    # # Validate other fields are strings
    # string_fields = ['business_type', 'selected_state', 'selected_district', 
    #                 'experience', 'availability', 'location_type', 'team_size']
    
    for field in required_fields:
        if not isinstance(data[field], str) or not data[field].strip():
            raise BadRequest(f"Field '{field}' must be a non-empty string")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "BizBuddy Crew API",
        "version": "1.0.0"
    })

@app.route('/api/info', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        "service": "BizBuddy Crew Business Consultation API",
        "version": "1.0.0",
        "description": "Submit business consultation requests and get AI-powered recommendations",
        "endpoints": {
            "POST /api/consultation": "Submit business consultation request",
            "GET /health": "Health check",
            "GET /api/info": "API information"
        },
        "required_fields": [
            "budget (number)",
            "business_type (string)",
            "selected_state (string)",
            "selected_district (string)",
            "experience (string)",
            "availability (string)",
            "location_type (string)",
            "team_size (string)"
        ]
    })

@app.route('/api/consultation', methods=['POST'])
def submit_consultation():
    """Main API endpoint for business consultation submissions"""
    try:
        # Check if request contains JSON
        if not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Content-Type must be application/json",
                "error_code": "INVALID_CONTENT_TYPE"
            }), 400
        
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({
                "status": "error",
                "message": "No JSON data provided or invalid JSON format",
                "error_code": "NO_JSON_DATA"
            }), 400
        
        # Validate the JSON data
        validate_json_data(data)

        # {
    # "ticket_name": "Fix the bug in LWC",
    # "ticket_id": "AA-204",
    # "priority": "Medium",
    # "description": "We are facing issue in the button position and description box position. Please fix this ASAP.",
    # "required_skills": ["LWC", "JS"],
    # "suggested_employees": ["Vasanth", "Akash", "Yuvaraj"],
    # "Project": "Salesforce",
    # "Days_to_complete": "Should be done within 2 days",
    # "department": "Development"
    # }
        
        # Call the business logic function
        result = process_business_info(
            data.get('ticket_name'),
            data.get('ticket_id'),
            data.get('priority'),
            data.get('description'),
            data.get('required_skills'),
            data.get('suggested_employees'),
            data.get('Project'),
            data.get('Days_to_complete'),
            data.get('department')
        )
        
        # Save the result to a file for reference (optional)
        try:
            with open('business_consultations.json', 'a', encoding='utf-8') as f:
                consultation_record = {
                    "timestamp": data.get('timestamp', None),
                    "input_data": data,
                    "result": result
                }
                f.write(json.dumps(consultation_record) + '\n')
        except Exception as e:
            logger.error(f"Error saving consultation record: {str(e)}")
            # Don't fail the request if logging fails
        
        # Return successful JSON response
        return jsonify({
            "status": "success",
            "message": "Business consultation processed successfully",
            "data": {
                "consultation_id": f"consultation_{hash(str(data))}",
                "input_summary": {
                    "budget": data.get('budget'),
                    "business_type": data.get('business_type'),
                    "location": f"{data.get('selected_district')}, {data.get('selected_state')}",
                    "team_size": data.get('team_size'),
                    "availability": data.get('availability')
                },
                "recommendations": result.get('recommendations', 'No specific recommendations available'),
                "analysis": result
            }
        }), 200
    
    except BadRequest as e:
        logger.warning(f"Bad request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "error_code": "VALIDATION_ERROR"
        }), 400
    except Exception as e:
        logger.error(f"Error processing consultation submission: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error occurred while processing your request",
            "error_code": "INTERNAL_SERVER_ERROR"
        }), 500

@app.route('/api/consultation', methods=['GET'])
def consultation_help():
    """Help endpoint for consultation API"""
    return jsonify({
        "message": "Use POST method to submit consultation data",
        "method": "POST",
        "content_type": "application/json",
        "sample_request": {
            "ticket_name": "Fix the bug in LWC",
            "ticket_id": "AA-204",
            "priority": "Medium",
            "description": "We are facing issue in the button position and description box position. Please fix this ASAP.",
            "required_skills": ["LWC", "JS"],
            "suggested_employees": ["Vasanth", "Akash", "Yuvaraj"],
            "Project": "Salesforce",
            "Days_to_complete": 2,
            "department": "Development"
        }
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "error_code": "NOT_FOUND",
        "available_endpoints": [
            "POST /api/consultation",
            "GET /api/consultation",
            "GET /api/info",
            "GET /health"
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "status": "error",
        "message": "Method not allowed for this endpoint",
        "error_code": "METHOD_NOT_ALLOWED"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "error_code": "INTERNAL_SERVER_ERROR"
    }), 500

if __name__ == '__main__':
    print("Starting BizBuddy Crew JSON API Server...")
    print("Available endpoints:")
    print("  POST /api/consultation - Submit business consultation")
    print("  GET  /api/consultation - Get help for consultation endpoint")
    print("  GET  /api/info - Get API information")
    print("  GET  /health - Health check")
    print("\nServer running on http://0.0.0.0:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)