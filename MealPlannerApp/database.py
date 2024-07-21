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
        name = recipe[0]
        ingredients_str = recipe[1] if recipe[1] else ''  # Handle NULL values
        dietary_str = recipe[2] if recipe[2] else ''  # Handle NULL values
        recipe_text = recipe[3] if recipe[3] else ''  # Handle NULL values
        
        recipe_dict = {
            "name": name,
            "ingredients": ingredients_str.split(', ') if ingredients_str else [],  # Handle empty strings
            "dietary": dietary_str.split(', ') if dietary_str else [],  # Handle empty strings
            "recipe": recipe_text
        }
        recipe_list.append(recipe_dict)
    
    connection.close()
    return recipe_list
