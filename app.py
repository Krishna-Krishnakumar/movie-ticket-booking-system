from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import backend
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/movies')
def movies():
    movies = backend.view_movies()
    return render_template('movies.html', movies=movies)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        # Get form data
        user_name = request.form.get('user_name')
        movie_id = request.form.get('movie')
        theatre_id = request.form.get('theatre')
        show_id = request.form.get('show')
        tickets = request.form.get('tickets')

        if not all([user_name, movie_id, theatre_id, show_id, tickets]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('booking'))

        # Add booking to database
        try:
            backend.add_booking(user_name, int(show_id), int(tickets))
            flash('Booking successful!', 'success')
            return redirect(url_for('confirmation'))
        except Exception as e:
            flash('Error making booking. Please try again.', 'error')
            return redirect(url_for('booking'))

    # GET request - show booking form
    movies = backend.view_movies()
    theatres = backend.view_theatres()
    return render_template('booking.html', movies=movies, theatres=theatres)

@app.route('/get_shows', methods=['POST'])
def get_shows():
    try:
        movie_id = request.form.get('movie_id')
        theatre_id = request.form.get('theatre_id')
        
        if not movie_id or not theatre_id:
            return jsonify({'error': 'Missing movie_id or theatre_id'}), 400
            
        shows = backend.get_shows(int(movie_id), int(theatre_id))
        show_list = []
        for show in shows:
            show_time = show[3]
            if isinstance(show_time, timedelta):
                # Convert timedelta to string in HH:MM:SS format
                total_seconds = int(show_time.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                time_str = str(show_time)
                
            show_list.append({
                'id': show[0],
                'time': time_str,
                'available_seats': show[4]
            })
        return jsonify(show_list)
    except Exception as e:
        app.logger.error(f"Error getting shows: {str(e)}")
        return jsonify({'error': 'Failed to get show times'}), 500

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True) 