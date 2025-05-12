from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# DB init
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_number TEXT NOT NULL,
            is_booked INTEGER DEFAULT 0
        )
    ''')
    conn.commit()

    # Insert slots if empty
    c.execute("SELECT COUNT(*) FROM slots")
    if c.fetchone()[0] == 0:
        for i in range(1, 11):  # 10 slots
            c.execute("INSERT INTO slots (slot_number, is_booked) VALUES (?, ?)", (f"SLOT-{i}", 0))
        conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM slots")
    slots = c.fetchall()
    conn.close()
    return render_template('home.html', slots=slots)

@app.route('/book/<int:slot_id>', methods=['GET', 'POST'])
def book(slot_id):
    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("UPDATE slots SET is_booked = 1 WHERE id = ?", (slot_id,))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('book.html', slot_id=slot_id)

@app.route('/release/<int:slot_id>', methods=['POST'])
def release(slot_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE slots SET is_booked = 0 WHERE id = ?", (slot_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
