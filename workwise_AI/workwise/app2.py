from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process-data', methods=['POST'])
def process_data():
    try:
        # Parse JSON payload
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON payload received"}), 400

        print("✅ Received JSON:")
        print(data)

        # EXAMPLE: Mock processing logic (you can call your RAG function here)
        employee_name = data.get("employee_name", "Unknown")
        decision = f"Approved for assignment: {employee_name}"
        flag = 1 if "frontend" in employee_name.lower() else 0

        # Simulated response (normally you'd call: rag_obj.rag_agent_main(data))
        rag_response = {
            "decision": decision,
            "flag": flag
        }

        return jsonify(rag_response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
