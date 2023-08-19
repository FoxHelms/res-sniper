import sqlite3

def create_table():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE restaurants (
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
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    c.execute('INSERT INTO restaurants VALUES (%s,%i)' %(restName,id))
    conn.commit()
    conn.close()


def disp_table():
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    selectPrompt = 'SELECT * FROM restaurants'
    c.execute(selectPrompt)
    data = c.fetchall()
    for d in data:
        print(d)

def get_ids():
    ids = []
    conn = sqlite3.connect('restaurant.db')
    c = conn.cursor()
    selectPrompt = 'SELECT restaurant_id FROM restaurants'
    c.execute(selectPrompt)
    data = c.fetchall()
    for d in data:
        ids.append(d[0])
    return ids

ids = get_ids()
for id in ids:
    print(id)