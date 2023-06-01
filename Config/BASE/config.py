HOSTNAME = '127.0.0.1'
PORT = 3306
USERNAME = 'root'
PASSWORD = 'your_password'
DATABASE = 'chat_time_system'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI


SECRET_KEY = "cv;/pobjs41.]l.,dkv' dsvafmaeofcasv"
SESSION_TYPE = 'filesystem'
SESSION_USE_SIGNER = True
SESSION_FILE_THRESHOLD = 1000
SESSION_REFRESH_EACH_REQUEST = True
SESSION_PERMANENT = True