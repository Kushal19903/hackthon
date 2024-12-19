from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from twilio.rest import Client

# Initialize Flask
app = Flask(__name__)

# Firebase Configuration
cred = credentials.Certificate('path/to/your-firebase-credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Twilio Configuration
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
client = Client(account_sid, auth_token)

# API: Fetch disaster updates
@app.route('/api/updates', methods=['GET'])
def fetch_disaster_updates():
    try:
        # Get disaster data from Firebase
        docs = db.collection('disaster_updates').stream()
        updates = []
        for doc in docs:
            updates.append(doc.to_dict())
        return jsonify(updates), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API: Add new disaster update
@app.route('/api/updates', methods=['POST'])
def add_disaster_update():
    try:
        # Get data from POST request
        data = request.get_json()
        type = data.get('type')
        location = data.get('location')
        details = data.get('details')
        contact = data.get('contact')

        # Add disaster update to Firebase
        db.collection('disaster_updates').add({
            'type': type,
            'location': location,
            'details': details,
            'contact': contact
        })

        # Return success response
        return jsonify({'message': 'Disaster update added successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API: Broadcast disaster alerts (SMS)
@app.route('/api/alerts', methods=['GET'])
def broadcast_alerts():
    try:
        # Fetch disaster updates
        disaster_data = db.collection('disaster_updates').stream()

        # Sample phone numbers (use actual numbers)
        user_phone_numbers = ['+1234567890', '+1987654321']

        # Broadcast alerts via SMS
        for update in disaster_data:
            message = f"Alert! {update['type']} reported at {update['location']}\n" \
                      f"Details: {update['details']}\n" \
                      f"Contact: {update['contact']}"
            for phone_number in user_phone_numbers:
                client.messages.create(
                    body=message,
                    from_='your_twilio_number',
                    to=phone_number
                )

        return jsonify({'message': 'Disaster alerts sent successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
