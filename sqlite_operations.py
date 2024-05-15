import sqlite3 as sql


def init_database():
    
    conn = sql.connect('scrap_base.db')


    conn.execute('''CREATE TABLE IF NOT EXISTS sites_table
         (ID INTEGER PRIMARY KEY AUTOINCREMENT,
         Link           TEXT    NOT NULL,
         Title            INT     NOT NULL);''')
    conn.close()
    
def create_conn():
    conn=sql.connect("scrap_base.db")

    return conn


def add_entry(conn,link:str,title:str):
    try:
        conn.execute(f"insert into sites_table (Link, Title) values ('{link}','{title}');")
        conn.commit()
    except sql.OperationalError:
        print("SyntaxError: couldnt add an entry. Continuing scraping...")
    except Exception as e:
        print(f"Unknown error: {e}")


