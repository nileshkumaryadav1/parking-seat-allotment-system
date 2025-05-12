from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get MongoDB URI from environment variable
MONGODB_URI = os.getenv("MONGODB_URI")

# Initialize Flask app
app = Flask(__name__)

# MongoDB setup
client = MongoClient(MONGODB_URI)
db = client["parking_system"]
slots_collection = db["slots"]

# DB init
def init_db():
    if slots_collection.count_documents({}) == 0:
        for i in range(1, 11):  # 10 slots
            slots_collection.insert_one({"slot_number": f"SLOT-{i}", "is_booked": False})

@app.route('/')
def home():
    slots = list(slots_collection.find())
    return render_template('home.html', slots=slots)

@app.route('/book/<slot_id>', methods=['GET', 'POST'])
def book(slot_id):
    try:
        if request.method == 'POST':
            slots_collection.update_one({"_id": ObjectId(slot_id)}, {"$set": {"is_booked": True}})
            return redirect('/')
        return render_template('book.html', slot_id=slot_id)
    except Exception as e:
        return f"Error booking slot: {e}"

@app.route('/release/<slot_id>', methods=['GET', 'POST'])
def release(slot_id):
    try:
        if request.method == 'POST':
            result = slots_collection.update_one({"_id": ObjectId(slot_id)}, {"$set": {"is_booked": False}})
            if result.matched_count == 0:
                return render_template('release.html', slot_id=slot_id, error="Slot not found.")
            return redirect('/')
        return render_template('release.html', slot_id=slot_id)
    except Exception as e:
        return render_template('release.html', slot_id=slot_id, error="Something went wrong.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
