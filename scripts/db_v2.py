import MySQLdb as sql
import config

conf = config.DBConfig()

db = sql.connect(host=conf.host, user=conf.user, port=int(conf.port),
                 passwd=conf.password)

cursor = db.cursor()
query = "USE highway"
cursor.execute(query)

query = "SELECT column_name FROM information_schema.columns WHERE table_name = 'users'"
cursor.execute(query)
if cursor.rowcount == 2:
    query = "CREATE table roles(" \
            "ID int AUTO_INCREMENT," \
            "Role varchar(50) NOT NULL," \
            "PRIMARY KEY (ID)" \
            ")"
    cursor.execute(query)
    query = "INSERT INTO roles (ID, Role) VALUES (1, Admin), (2, Regular)"

    query = "ALTER TABLE users ADD Role int DEFAULT 2"
    cursor.execute(query)
    query = "ALTER TABLE tasks ADD Position int DEFAULT 999999"
    cursor.execute(query)

db.close()
