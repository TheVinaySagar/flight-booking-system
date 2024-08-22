class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flight_user:password123@localhost/flight_booking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
