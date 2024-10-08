from flask import render_template, redirect, url_for, flash, request, session
from app import app, db
from app.models import User, Flight, Booking
from datetime import datetime


from flask import send_from_directory

@app.route('/static/css/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)

# User routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            # Username exists, show an error message
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('signup.html')
        
        # Create a new user and add to the database
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password,is_admin=False).first()
        if user:
            session['user_id'] = user.id
            session['is_admin'] = False
            return redirect(url_for('user_dashboard'))
        else:
            # flash("Invalid credantials! ",'error')
            flash("Invalid username or password", "error")
    return render_template('login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['admin_username']
        password = request.form['admin_password']
        admin = User.query.filter_by(username=username, password=password, is_admin=True).first()

        if admin:
            session['user_id'] = admin.id
            session['is_admin'] = True  # Set is_admin to True in the session
            return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard
        else:
            flash('Invalid admin credentials. Please try again.', 'danger')
    return render_template('admin_login.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/user_dashboard')
def user_dashboard():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    return render_template('user_dashboard.html')

@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']
        
        # Convert the date and time into a datetime object for comparison
        search_datetime = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
        
        # Query to find all flights after the given date and time
        flights = Flight.query.filter(
            db.and_(
                Flight.date > search_datetime.date(),
                Flight.time >= search_datetime.time()
            )
        ).all()

        return render_template('search_flights.html', flights=flights)
    
    return render_template('search_flights.html')

@app.route('/book_flight/<int:flight_id>')
def book_flight(flight_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    flight = Flight.query.get(flight_id)
    if flight.available_seats > 0:
        flight.available_seats -= 1
        booking = Booking(user_id=session['user_id'], flight_id=flight.id)
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('user_dashboard'))
    else:
        return "No seats available"

@app.route('/my_bookings')
def my_bookings():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    bookings = Booking.query.filter_by(user_id=session['user_id']).all()
    return render_template('user_dashboard.html', bookings=bookings)

# Admin routes
@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('user_id') or not session.get('is_admin'):
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html')

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if not session.get('user_id') or not session.get('is_admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        date = request.form['date']
        time = request.form['time']
        flight = Flight(flight_number=flight_number, date=date, time=time)
        db.session.add(flight)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('add_flight.html')

@app.route('/remove_flight', methods=['GET', 'POST'])
def remove_flight():
    if request.method == 'POST':
        # Handle flight removal
        flight_id = request.form.get('flight_id')
        flight = Flight.query.get(flight_id)
        if flight:
            try:
                # First, delete all bookings associated with this flight
                Booking.query.filter_by(flight_id=flight_id).delete()

                # Then delete the flight
                db.session.delete(flight)
                db.session.commit()
                flash(f'Flight {flight.flight_number} and all associated bookings have been removed successfully.', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {str(e)}', 'error')
        else:
            flash('Flight not found.', 'error')
        return redirect(url_for('remove_flight'))

    # Handle the display of all flights or search by flight number
    search_query = request.args.get('search')
    if search_query:
        flights = Flight.query.filter(Flight.flight_number.ilike(f'%{search_query}%')).all()
    else:
        flights = Flight.query.all()
    
    return render_template('remove_flight.html', flights=flights, search_query=search_query)



# @app.route('/remove_flight1')
# def remove_flight1():
#     if not session.get('user_id') or not session.get('is_admin'):
#         return redirect(url_for('login'))
    

@app.route('/view_all_bookings', methods=['GET', 'POST'])
def view_all_bookings():
    if not session.get('user_id') or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        flight_number = request.form['flight_number']
        flight = Flight.query.filter_by(flight_number=flight_number).first()
        if flight:
            bookings = Booking.query.filter_by(flight_id=flight.id).all()
        else:
            bookings = []  # No flight found, so no bookings
        return render_template('view_bookings.html', bookings=bookings, flight_number=flight_number)
    
    # If no flight number is provided, show all bookings
    bookings = Booking.query.all()
    return render_template('view_bookings.html', bookings=bookings)

