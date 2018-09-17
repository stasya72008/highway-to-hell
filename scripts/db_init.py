import MySQLdb as sql
import config

conf = config.DBConfig()

db = sql.connect(host=conf.host, user=conf.user, port=int(conf.port),
                 passwd=conf.password)

cursor = db.cursor()
query = 'CREATE DATABASE IF NOT EXISTS highway'
cursor.execute(query)

query = 'ALTER DATABASE highway CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
cursor.execute(query)

query = 'USE highway'
cursor.execute(query)

query = "show tables"
cursor.execute(query)

query = 'CREATE table IF NOT EXISTS users (' \
        'ID int AUTO_INCREMENT, ' \
        'Username varchar(255) NOT NULL,' \
        'PRIMARY KEY (ID)' \
        ')'
cursor.execute(query)

query = "CREATE table IF NOT EXISTS tasks (" \
        "ID int AUTO_INCREMENT, " \
        "UserID int NOT NULL," \
        "Name varchar(255) NOT NULL," \
        "Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP()," \
        "Status enum('active', 'done', 'deleted', 'archive') NOT NULL DEFAULT 'active'," \
        "Calendar_date DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00'," \
        "PRIMARY KEY (ID)," \
        "FOREIGN KEY (UserID) REFERENCES users(ID)" \
        ")"
cursor.execute(query)

query = "ALTER TABLE tablename CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
cursor.execute(query)

db.close()
