import MySQLdb as sql
import config

conf = config.DBConfig()

db = sql.connect(host=conf.host, user=conf.user, port=int(conf.port),
                 passwd=conf.password)

cursor = db.cursor()
query = 'CREATE DATABASE IF NOT EXISTS highway'
cursor.execute(query)

query = 'USE highway'
cursor.execute(query)

query = 'CREATE table users (' \
        'ID int AUTO_INCREMENT, ' \
        'Username varchar(20) NOT NULL,' \
        'PRIMARY KEY (ID)' \
        ')'
cursor.execute(query)

query = "CREATE table tasks (" \
        "ID int AUTO_INCREMENT, " \
        "UserID int NOT NULL," \
        "Name varchar(255) NOT NULL," \
        "Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()," \
        "Status enum('active', 'done', 'deleted', 'archive') NOT NULL DEFAULT 'active'," \
        "Calendar_date varchar(15)," \
        "PRIMARY KEY (ID)," \
        "FOREIGN KEY (UserID) REFERENCES users(ID)" \
        ")"
cursor.execute(query)

db.close()
