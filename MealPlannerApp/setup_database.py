import sqlite3

def create_database():
    connection = sqlite3.connect('meal_planner.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        dietary TEXT NOT NULL,
        recipe TEXT NOT NULL
    )
    ''')

    # Insert some sample recipes
    cursor.executemany('''
    INSERT INTO recipes (name, ingredients, dietary, recipe) VALUES (?, ?, ?, ?)
    ''', [
        ('Spaghetti with Tomato Sauce', 'spaghetti, tomato sauce', 'vegetarian', 'Cook spaghetti. Add tomato sauce.'),
        ('Veggie Stir-fry', 'vegetables, soy sauce', 'vegan', 'Stir-fry vegetables. Add soy sauce.')
    ])

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_database()
    print("Database and table created successfully, with sample recipes added.")
