import mysql.connector

def init_database():
    # First connect without database
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sukritham@4",
        auth_plugin="caching_sha2_password"
    )
    cur = con.cursor()
    
    # Drop and recreate database
    cur.execute("DROP DATABASE IF EXISTS movie_booking")
    cur.execute("CREATE DATABASE movie_booking")
    cur.execute("USE movie_booking")
    
    print("Database initialized!")
    return con, cur

def connect():
    print("Attempting to connect to MySQL...")
    
    # Initialize database
    con, cur = init_database()

    print("Connected successfully!")
    cur = con.cursor()

    # 🔹 First, create independent tables (NO FOREIGN KEYS)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            Movie_ID INT PRIMARY KEY AUTO_INCREMENT,
            Movie_Name VARCHAR(255),
            Release_Date DATE,
            Director VARCHAR(255),
            Cast TEXT,
            Budget DECIMAL(10,2),
            Duration TIME,
            Rating DECIMAL(2,1)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS theatres (
            Theatre_ID INT PRIMARY KEY AUTO_INCREMENT,
            Theatre_Name VARCHAR(255),
            Location VARCHAR(255)
        )
    """)

    # 🔹 Then, create dependent tables (WITH FOREIGN KEYS)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS shows (
            Show_ID INT PRIMARY KEY AUTO_INCREMENT,
            Movie_ID INT NOT NULL,
            Theatre_ID INT NOT NULL,
            Show_Time TIME,
            Available_Seats INT,
            FOREIGN KEY (Movie_ID) REFERENCES movies(Movie_ID) ON DELETE CASCADE,
            FOREIGN KEY (Theatre_ID) REFERENCES theatres(Theatre_ID) ON DELETE CASCADE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            Booking_ID INT PRIMARY KEY AUTO_INCREMENT,
            User_Name VARCHAR(255),
            Show_ID INT NOT NULL,
            Tickets_Booked INT,
            FOREIGN KEY (Show_ID) REFERENCES shows(Show_ID) ON DELETE CASCADE
        )
    """)

    con.commit()
    con.close()
    print("✅ Tables created successfully!")

# Add a movie
def add_movie(Movie_Name, Release_Date, Director, Cast, Budget, Duration, Rating):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sukritham@4",
        database="movie_booking",
        auth_plugin="caching_sha2_password"
    )
    cur = con.cursor()
    cur.execute("INSERT INTO movies (Movie_Name, Release_Date, Director, Cast, Budget, Duration, Rating) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                (Movie_Name, Release_Date, Director, Cast, Budget, Duration, Rating))
    con.commit()
    con.close()

# View all movies
def view_movies():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sukritham@4",
        database="movie_booking",
        auth_plugin="caching_sha2_password"
    )
    cur = con.cursor()
    cur.execute("SELECT * FROM movies")
    rows = cur.fetchall()
    con.close()
    return rows

# Get all theatres
def view_theatres():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sukritham@4",
        database="movie_booking",
        auth_plugin="caching_sha2_password"
    )
    cur = con.cursor()
    cur.execute("SELECT * FROM theatres")
    rows = cur.fetchall()
    con.close()
    return rows

# Get shows for a specific movie and theatre
def get_shows(movie_id, theatre_id):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sukritham@4",
        database="movie_booking",
        auth_plugin="caching_sha2_password"
    )
    cur = con.cursor()
    cur.execute("SELECT * FROM shows WHERE Movie_ID = %s AND Theatre_ID = %s", (movie_id, theatre_id))
    rows = cur.fetchall()
    con.close()
    return rows

# Get movie ID by name
def get_movie_id(movie_name):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sukritham@4",
        database="movie_booking",
        auth_plugin="caching_sha2_password"
    )
    cur = con.cursor()
    cur.execute("SELECT Movie_ID FROM movies WHERE Movie_Name = %s", (movie_name,))
    result = cur.fetchone()
    con.close()
    return result[0] if result else None

# Get theatre ID by name
def get_theatre_id(theatre_name):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sukritham@4",
        database="movie_booking",
        auth_plugin="caching_sha2_password"
    )
    cur = con.cursor()
    cur.execute("SELECT Theatre_ID FROM theatres WHERE Theatre_Name = %s", (theatre_name,))
    result = cur.fetchone()
    con.close()
    return result[0] if result else None

# Add a booking
def add_booking(User_Name, Show_ID, Tickets_Booked):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sukritham@4",
        database="movie_booking",
        auth_plugin="caching_sha2_password"
    )
    cur = con.cursor()
    cur.execute("INSERT INTO bookings (User_Name, Show_ID, Tickets_Booked) VALUES (%s, %s, %s)", 
                (User_Name, Show_ID, Tickets_Booked))
    cur.execute("UPDATE shows SET Available_Seats = Available_Seats - %s WHERE Show_ID = %s", 
                (Tickets_Booked, Show_ID))
    con.commit()
    con.close()

def initialize_sample_data():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sukritham@4",
        database="movie_booking",
        auth_plugin="caching_sha2_password"
    )
    cur = con.cursor()

    # Add sample movies
    movies = [
        ('Inception', '2010-07-16', 'Christopher Nolan', 'Leonardo DiCaprio, Ellen Page', 160000000, '02:28:00', 8.8),
        ('The Dark Knight', '2008-07-18', 'Christopher Nolan', 'Christian Bale, Heath Ledger', 185000000, '02:32:00', 9.0),
        ('Pulp Fiction', '1994-10-14', 'Quentin Tarantino', 'John Travolta, Uma Thurman', 8000000, '02:34:00', 8.9),
        ('The Shawshank Redemption', '1994-09-23', 'Frank Darabont', 'Tim Robbins, Morgan Freeman', 25000000, '02:22:00', 9.3),
        ('Interstellar', '2014-11-07', 'Christopher Nolan', 'Matthew McConaughey, Anne Hathaway', 165000000, '02:49:00', 8.6)
    ]
    
    for movie in movies:
        cur.execute("INSERT IGNORE INTO movies (Movie_Name, Release_Date, Director, Cast, Budget, Duration, Rating) VALUES (%s, %s, %s, %s, %s, %s, %s)", movie)
    
    # Add sample theatres
    theatres = [
        ('PVR Cinema', 'Downtown'),
        ('INOX Movies', 'City Center'),
        ('Cinepolis', 'Mall of Entertainment'),
        ('Carnival Cinemas', 'West End')
    ]
    
    for theatre in theatres:
        cur.execute("INSERT IGNORE INTO theatres (Theatre_Name, Location) VALUES (%s, %s)", theatre)
    
    # Add sample shows for each movie in each theatre
    show_times = ['10:00:00', '13:00:00', '16:00:00', '19:00:00', '22:00:00']
    
    # Get all movies and theatres
    cur.execute("SELECT Movie_ID FROM movies")
    movie_ids = cur.fetchall()
    cur.execute("SELECT Theatre_ID FROM theatres")
    theatre_ids = cur.fetchall()
    
    # Add shows
    for movie_id in movie_ids:
        for theatre_id in theatre_ids:
            for show_time in show_times:
                cur.execute("INSERT IGNORE INTO shows (Movie_ID, Theatre_ID, Show_Time, Available_Seats) VALUES (%s, %s, %s, %s)", 
                          (movie_id[0], theatre_id[0], show_time, 100))
    
    con.commit()
    con.close()
    print("✅ Sample data initialized!")

if __name__ == "__main__":
    connect()
    initialize_sample_data()
