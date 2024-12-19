# Firebase Configuration in Python
import firebase_admin
from firebase_admin import credentials, firestore
from twilio.rest import Client
import time

# Initialize Firebase
cred = credentials.Certificate("C:/Users/Kushal S/hackthon/parse 1/firebase-credentials.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

# Twilio SMS Configuration
account_sid = 'AC47980d35f5b3a2097aa116a8dcea2ab0'
auth_token = 'b7f8f52df5dacb7ce4cdfbd996613e15'
client = Client(account_sid, auth_token)

# Function to send SMS
def send_sms(phone_number, message):
    try:
        message = client.messages.create(
            body=message,
            from_='+12295159150',
            to='+919611581279'
        )
        print(f"Message sent to {phone_number}: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS to {phone_number}: {e}")

# Load Disaster Updates from Firebase
def load_updates():
    try:
        docs = db.collection('disaster_updates').stream()
        updates = []
        for doc in docs:
            updates.append(doc.to_dict())
        return updates
    except Exception as e:
        print(f"Error loading updates: {e}")
        return []

# Add New Disaster Update to Firebase
# Add New Disaster Update to Firebase
def add_update(type, location, details, contact, food_facilities, shelter_facility):
    try:
        db.collection('disaster_updates').add({
            'type': type,
            'location': location,
            'details': details,
            'contact': contact,
            'food_facilities': food_facilities,
            'shelter_facility': shelter_facility
        })
        print("Disaster update added successfully!")
    except Exception as e:
        print(f"Error adding update: {e}")
# Correct function call with 6 arguments
add_update(
    "Flood", 
    "City A", 
    "Severe flooding in the downtown area.", 
    "+123456789", 
    "Food facilities near your location: x, y, z", 
    "Shelter facility available at: a, b, c"
)



# Retrieve Disaster Data from Firebase
def fetch_disaster_data():
    try:
        docs = db.collection('disaster_updates').stream()
        disaster_data = []
        for doc in docs:
            disaster_data.append(doc.to_dict())
        return disaster_data
    except Exception as e:
        print(f"Error fetching disaster data: {e}")
        return []

# Broadcast Disaster Alerts via SMS
def broadcast_alerts():
    disaster_data = fetch_disaster_data()
    if not disaster_data:
        print("No disaster updates available.")
        return

    # Sample List of User Phone Numbers
    user_phone_numbers = [
        '+1234567890', # Replace with actual numbers
        '+1987654321'
    ]

    for update in disaster_data:
        message = f"Alert! {update['type']} reported at {update['location']}\n" \
                  f"Details: {update['details']}\n" \
                  f"Contact: {update['contact']}\n"\
                  f"Food Facilities: {update.get('food_facilities', 'N/A')}\n"\
                  f"Shelter Facility: {update.get('shelter_facility', 'N/A')}"
        for phone_number in user_phone_numbers:
            send_sms(phone_number, message)

# Example Firestore Schema (for Frontend Integration):
# Collection: disaster_updates
# Document Fields: type, location, details, contact

if __name__ == "__main__":
    print("Starting Disaster Alert System...")
    print("Loading updates...")
    updates = load_updates()
    for update in updates:
        print(update)

    print("Adding a new update...")
    add_update(
        "Flood", "City A", "Severe flooding in the downtown area.", 
        "+123456789", 
        "Food facilities near to your locations are x, y, z", 
        "Shelter facility is in a, b, c"
    )

    try:
        while True:
            broadcast_alerts()
            
            # Check for user input to break the loop
            user_input = input("Enter 'stop' to quit or press Enter to continue: ").strip().lower()
            if user_input == 'stop':
                print("Disaster Alert System stopped.")
                break
            
            time.sleep(60 * 5)  # Check for updates every 5 minutes

    except KeyboardInterrupt:
        print("\nDisaster Alert System stopped by user (KeyboardInterrupt).")
