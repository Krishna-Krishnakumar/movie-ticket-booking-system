# Movie Ticket Booking System

A web-based Movie Ticket Booking System built with Flask that allows users to browse movies, select showtimes, and book tickets online.

## Features

- Browse available movies
- View movie details and showtimes
- Select seats and book tickets
- User-friendly interface
- Real-time seat availability
- Booking confirmation system

## Prerequisites

- Python 3.x
- MySQL
- Flask
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Krishna-Krishnakumar/movie-ticket-booking-system.git
cd movie-ticket-booking-system
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up MySQL database:
- Make sure MySQL is installed and running on your system
- The backend will automatically create the required database and tables

## Running the Application

1. Start the backend server:
```bash
python3 backend.py
```

2. In a new terminal, start the frontend application:
```bash
python3 app.py
```

3. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## Project Structure

```
movie-ticket-booking-system/
├── app.py              # Frontend Flask application
├── backend.py          # Backend API server
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── movies.html
│   ├── booking.html
│   └── confirmation.html
└── README.md
```

## Technologies Used

- Frontend: Flask, HTML, CSS
- Backend: Flask, MySQL
- Database: MySQL

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Krishna Krishnakumar

## Acknowledgments

- Flask framework
- MySQL database
- All contributors and users of the system 