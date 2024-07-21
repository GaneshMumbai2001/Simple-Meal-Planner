import sqlite3

def get_recipes(dietary_preferences, allergies, ingredients):
    connection = sqlite3.connect('meal_planner.db')
    cursor = connection.cursor()
    
    # Simple query to get recipes matching dietary preferences and excluding allergies
    query = '''
    SELECT name, ingredients, dietary, recipe
    FROM recipes
    WHERE dietary LIKE ? AND ingredients NOT LIKE ?
    '''
    cursor.execute(query, ('%' + dietary_preferences + '%', '%' + allergies + '%'))
    recipes = cursor.fetchall()
    
    # Format the results
    recipe_list = []
    for recipe in recipes:
        recipe_dict = {
            "name": recipe[0],
            "ingredients": recipe[1].split(', '),
            "dietary": recipe[2].split(', '),
            "recipe": recipe[3]
        }
        recipe_list.append(recipe_dict)
    
    connection.close()
    return recipe_list
