from flask import Flask, jsonify, render_template, request
import json
import uuid  # For generating unique application numbers

app = Flask(__name__)

# Load applications from a JSON file (or create an empty dictionary if file doesn't exist)
try:
    with open("applications.json", "r") as f:
        applications = json.load(f)
except FileNotFoundError:
    applications = {}

# Save applications to file
def save_applications():
    with open("applications.json", "w") as f:
        json.dump(applications, f, indent=4)

# Route to submit a loan application
@app.route('/api/apply', methods=['POST'])
def apply():
    data = request.get_json()
    name = data.get('name')
    zipcode = data.get('zipcode')

    if not name or not zipcode:
        return jsonify({'error': 'Name and Zipcode are required'}), 400

    app_id = str(uuid.uuid4())[:8]  # Generate short unique ID
    applications[app_id] = {"name": name, "zipcode": zipcode, "status": "received"}

    save_applications()

    return jsonify({'message': 'Application submitted successfully', 'application_id': app_id})

# Route to check application status
@app.route('/api/status/<app_id>', methods=['GET'])
def check_status(app_id):
    if app_id in applications:
        return jsonify({'application_id': app_id, 'status': applications[app_id]['status']})
    return jsonify({'error': 'Application not found'}), 404

# Route to update application status
@app.route('/api/update/<app_id>', methods=['PUT'])
def update_status(app_id):
    data = request.get_json()
    new_status = data.get('status')

    if app_id not in applications:
        return jsonify({'error': 'Application not found'}), 404

    if new_status not in ["received", "processing", "accepted", "rejected"]:
        return jsonify({'error': 'Invalid status'}), 400

    applications[app_id]['status'] = new_status
    save_applications()

    return jsonify({'message': 'Application status updated successfully'})

# Route to render the frontend
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
