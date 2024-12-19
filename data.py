from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data to simulate disaster updates
disaster_updates = [
    {"type": "Flood", "location": "New York", "details": "Severe flooding in downtown.", "contact": "123-456-7890"},
    {"type": "Earthquake", "location": "California", "details": "Strong tremors felt in the Bay Area.", "contact": "987-654-3210"}
]

@app.route('/api/updates', methods=['GET'])
def get_updates():
    return jsonify(disaster_updates)

@app.route('/api/updates', methods=['POST'])
def add_update():
    new_update = request.get_json()
    disaster_updates.append(new_update)
    return jsonify({"message": "Update added successfully!"}), 201

@app.route('/api/contact', methods=['POST'])
def send_contact():
    contact_data = request.get_json()
    # Simulate saving contact info or sending email
    return jsonify({"message": "Message sent successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
