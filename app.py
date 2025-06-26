from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

app = Flask(__name__)
app.secret_key = 'secret-key'

DATA_FILE = 'data/bookings.json'
USER_FILE = 'data/users.json'
VENUES = [
    {"name": "Venue A", "image": "venue_a.jpg"},
    {"name": "Venue B", "image": "venue_b.jpg"},
    {"name": "Venue C", "image": "venue_c.jpg"}
]

# Ensure data folders exist
os.makedirs('data', exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)

def load_bookings():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_bookings(bookings):
    with open(DATA_FILE, 'w') as f:
        json.dump(bookings, f, indent=2)

def load_users():
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=2)

@app.route('/')
def home():
    bookings = load_bookings()
    return render_template('index.html', bookings=bookings, venues=VENUES, user=session.get('user'))

@app.route('/book', methods=['POST'])
def book():
    if 'user' not in session:
        flash('Please log in to book.')
        return redirect(url_for('login'))

    form = request.form
    bookings = load_bookings()
    new_booking = {
        'user': session['user'],
        'activity': form.get('activity'),
        'venue': form.get('venue'),
        'accessories': form.get('accessories'),
        'date': form.get('date'),
        'time': form.get('time')
    }
    for b in bookings:
        if b['date'] == new_booking['date'] and b['venue'] == new_booking['venue'] and b['activity'] == new_booking['activity']:
            flash('Booking already exists for this date, venue, and activity.')
            return redirect(url_for('home'))

    bookings.append(new_booking)
    save_bookings(bookings)
    flash('Booking successful!')
    return redirect(url_for('home'))

@app.route('/calendar')
def calendar_view():
    bookings = load_bookings()
    return render_template('calendar.html', bookings=bookings, user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            flash('Logged in successfully')
            return redirect(url_for('home'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if username in users:
            flash('User already exists')
            return redirect(url_for('register'))
        users[username] = password
        save_users(users)
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/admin')
def admin():
    if session.get('user') != 'admin':
        return "Access Denied"
    users = load_users()
    bookings = load_bookings()
    return render_template('admin.html', users=users, bookings=bookings)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully')
    return redirect(url_for('home'))

# Render compatibility: use port from environment
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
