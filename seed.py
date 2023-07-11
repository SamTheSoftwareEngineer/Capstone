import json
import psycopg2

drop_database = "dropdb funseeker"

create_database = "createdb funseeker"

def insert_data():
    # Read the JSON data
    with open('activities.json') as file:
        data = json.load(file)

    # Establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
        host='localhost',
        database='funseeker',
        user='postgres',
        password='postgres'
    )

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    
    # Drop the activity, favorites, and users tables if they exists
    drop_table_query = "DROP TABLE IF EXISTS activities, favorites, users CASCADE;"
    cursor.execute(drop_table_query)
    conn.commit()
    
    
    create_table_query = """
        CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    );
    
    CREATE TABLE activities (
        key TEXT PRIMARY KEY,
        accessibility TEXT,
        activity TEXT,
        type TEXT,
        participants INTEGER,
        price FLOAT
    );
    
    CREATE TABLE favorites (
        id SERIAL PRIMARY KEY,
        activity VARCHAR(255),
        user_id INTEGER REFERENCES users(id)
        
    );
    """
    


    cursor.execute(create_table_query)
    conn.commit()

    # Insert data into the PostgreSQL database
    for activity in data:
        query = "INSERT INTO activities (key, accessibility, activity, type, participants, price) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (
            activity['key'],
            activity['accessibility'],
            activity['activity'],
            activity['type'],
            activity['participants'],
            activity['price']
        )
        cursor.execute(query, values)

    # Commit the changes and close the cursor and connection
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Tables create successfully. Data inserted successfully.")

if __name__ == '__main__':
    insert_data()
