from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data storage (just for demo)
bookings = []
venues = ["Venue A", "Venue B", "Venue C"]

@app.route('/')
def home():
    return render_template('index.html', venues=venues, bookings=bookings)

@app.route('/book', methods=['POST'])
def book():
    user = request.form.get('user')
    activity = request.form.get('activity')
    venue = request.form.get('venue')
    accessories = request.form.get('accessories')
    date = request.form.get('date')
    time = request.form.get('time')

    # Check if booking exists
    for b in bookings:
        if b['date'] == date and b['venue'] == venue and b['activity'] == activity:
            return "Booking already exists for this date, venue, and activity. Please go back and try another slot."

    booking = {
        'user': user,
        'activity': activity,
        'venue': venue,
        'accessories': accessories,
        'date': date,
        'time': time
    }
    bookings.append(booking)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
