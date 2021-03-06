import MySQLdb as sql
import config

conf = config.DBConfig()

db = sql.connect(host=conf.host, user=conf.user, port=int(conf.port),
                 passwd=conf.password)

cursor = db.cursor()

try:
    cursor.execute("USE highway")
    cursor.execute("SHOW TABLES")

    if not any([t for t in cursor.fetchall() if t[0] == 'roles']):
        query = "CREATE table roles(" \
                "ID int AUTO_INCREMENT," \
                "Role varchar(50) NOT NULL," \
                "PRIMARY KEY (ID)" \
                ")"
        cursor.execute(query)
        query = "INSERT INTO roles (ID, Role) VALUES (1, 'Admin')"
        db.cursor().execute(query)
        query = "INSERT INTO roles (ID, Role) VALUES (2, 'Regular')"
        db.cursor().execute(query)
        query = "ALTER TABLE users ADD Role int NOT NULL"
        db.cursor().execute(query)
        query = "ALTER TABLE users ADD FOREIGN KEY (Role) REFERENCES roles(ID)"
        db.cursor().execute(query)
        query = "ALTER TABLE users ADD Password varchar(25) NOT NULL"
        db.cursor().execute(query)
        query = "ALTER TABLE users MODIFY Username varchar(255) NOT NULL UNIQUE"
        db.cursor().execute(query)
        query = "ALTER TABLE tasks ADD Position int NOT NULL"
        db.cursor().execute(query)

finally:
    db.close()
