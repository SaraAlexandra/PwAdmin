import sqlite3

FIND_TABLE_QUERY = """ SELECT count(name) FROM sqlite_master WHERE type='table' AND name='PASSWORDS';"""

# creates table in database
def generateDBTable(conn):
    cursor = conn.cursor()
    cursor.execute(FIND_TABLE_QUERY)
    if cursor.fetchone()[0] == 1:
        pass
    else:
        table = """CREATE TABLE PASSWORDS (
            ID INTEGER PRIMARY KEY,
            PASSWORD               VARCHAR(50) NOT NULL,
            DESCRIPTION            VARCHAR(20) NOT NULL,
            LENGTH                 INT NOT NULL
            ); """
        
        cursor.execute(table)

# insert entry
def insertPasswordInDB(conn, pw, desc, pwLen):
    cursor = conn.cursor()
    query = """INSERT INTO PASSWORDS(PASSWORD, DESCRIPTION, LENGTH) VALUES (?,?,?);"""
    cursor.execute(query, (pw, desc, pwLen))
    conn.commit()

# read all passwords/desc
def readAll(conn):
    cursor = conn.cursor()
    cursor.execute(FIND_TABLE_QUERY)
    if cursor.fetchone()[0] == 1:
        query = "SELECT * FROM PASSWORDS;"
        result = cursor.execute(query)
        return result.fetchall()
    else:
        print("No data available in database - readAll")
        return []

# read pw for description
def readPassword(conn, desc):
    cursor = conn.cursor()
    cursor.execute(FIND_TABLE_QUERY)
    if cursor.fetchone()[0] == 1:
        query = "SELECT * FROM PASSWORDS WHERE DESCRIPTION like ?;"
        result = cursor.execute(query, ('%' + desc + '%',))
        return result.fetchall()
    else:
        print("No data available in database - readPassword")
        return []

# update password at desc
def updatePassword(conn, desc, newPw, newLength):
    cursor = conn.cursor()
    cursor.execute(FIND_TABLE_QUERY)
    if cursor.fetchone()[0] == 1:
        query = """UPDATE PASSWORDS SET PASSWORD = ?,LENGTH = ? WHERE DESCRIPTION=?;"""
        cursor.execute(query, (newPw, newLength, desc))
        conn.commit()
    else:
        print("No data available in database - udaptePassword")

    return newPw;  