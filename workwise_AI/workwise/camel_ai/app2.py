from flask import Flask, request, jsonify
from dummy_main import main_alternative

app = Flask(__name__)

@app.route('/process-data', methods=['POST'])
def process_data():
    try:
        # Parse JSON payload
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload received"}), 400
        
        print("✅ Received JSON:")
        final_recommendation = main_alternative(data)
        print(data)
        
        # Return the recommendation from the agents
        return jsonify({
            "status": "success", 
            "message": "Data processed successfully",
            "recommendation": final_recommendation
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)