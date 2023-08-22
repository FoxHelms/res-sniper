import sqlite3

def create_table():
    conn = sqlite3.connect('permanent_restaurant.db')
    c = conn.cursor()
    if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='all_restaurants'"):
        c.execute('''CREATE TABLE all_restaurants (
                restaurant_name text,
                restaurant_id integer
                )''')
        conn.commit()
    conn.close()


def entry_in_db(entry):
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('SELECT rowid FROM restaurants WHERE restaurant_name=%s' %entry)
    data = c.fetchone()
    if data:
        return True
    else:
        return False
    
def write_to_db(restName,id):
    #if entry_in_db(restName):
    #    return
    #else:
    conn = sqlite3.connect('permanent_restaurant.db')
    c = conn.cursor()
    # START HERE This is throwing invalid input. 
    c.execute(f'INSERT INTO all_restaurants VALUES {restName},{id}')
    conn.commit()
    conn.close()


def disp_table():
    conn = sqlite3.connect('permanent_restaurant.db')
    c = conn.cursor()
    selectPrompt = 'SELECT * FROM all_restaurants'
    c.execute(selectPrompt)
    data = c.fetchall()
    for d in data:
        print(d)

def get_ids():
    ids = []
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    selectPrompt = 'SELECT restaurant_id FROM all_restaurants'
    c.execute(selectPrompt)
    data = c.fetchall()
    for d in data:
        ids.append(d[0])
    return ids