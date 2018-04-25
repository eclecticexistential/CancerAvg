import sqlite3


db1999_conn = sqlite3.connect('states1999.db')


def initialize1999():
    db1999_conn.execute("DROP TABLE IF EXISTS States1999")
    db1999_conn.commit()
    try:
        db1999_conn.execute(
            "CREATE TABLE States1999(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Year INTEGER NOT NULL, "
            "State TEXT NOT NULL, Pop INTEGER NOT NULL, Cancer INTEGER NOT NULL);")
        db1999_conn.commit()

        # print("Table Created")

    except sqlite3.OperationalError:
        print("Table couldn't be Created")


initialize1999()


def insert_into_db(year, state, pop, cancer):
        db1999_conn.execute("INSERT INTO States1999 (Year, State, Pop, Cancer) VALUES ('" + year + "', '" +
                            state + "', '" + pop + "', '" + cancer + "')")


def get_1999_stats():
    cursor = db1999_conn.cursor()
    try:
        result = cursor.execute("SELECT Year, State, Pop, Cancer FROM States1999")
        return result

    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")

    except:
        print("Couldn't Retrieve Data From Database")

