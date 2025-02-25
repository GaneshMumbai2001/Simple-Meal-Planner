# Meal Planner App

## Description

The Meal Planner app is a Python-based desktop application designed to help users plan their weekly meals based on dietary preferences, allergies, and available ingredients. It generates a meal plan for the week, provides detailed recipes, and creates a grocery list with missing ingredients.

## Features

- **Meal Planning:** Generates a weekly meal plan based on user input.
- **Recipe Details:** Displays detailed information for each recipe.
- **Grocery List:** Provides a list of missing ingredients and visualizes ingredient counts.
- **Chart Visualization:** Shows a bar chart of ingredient counts for the selected meal.

## Prerequisites

- Python 3.7 or higher
- Required Python libraries: `tkinter`, `matplotlib`, `sqlite3`

## Installation

1. **Clone the Repository:**

    ```powershell
    git clone https://github.com/GaneshMumbai2001/Simple-Meal-Planner.git
    ```

2. **Navigate to the Project Directory:**

    ```powershell
    cd meal-planner-app
    ```

3. **Install Required Libraries:**

    Install the required Python libraries using pip:

    ```powershell
    pip install matplotlib
    ```

4. **Set Up the Database:**

    Run the `setup_database.py` script to create the database and populate it with sample recipes:

    ```powershell
    python setup_database.py
    ```

## Usage

1. **Start the Application:**

    Run the main application script:

    ```powershell
    python meal_planner.py
    ```

2. **Using the Application:**

    - **Welcome Frame:** Enter dietary preferences, allergies, and available ingredients. Click "Submit" to generate a meal plan.
    - **Meal Plan Frame:** View the meal plan for the week. Click on meal names to see detailed recipes or use the "Grocery List" button to view missing ingredients.
    - **Grocery List Frame:** Check the list of missing ingredients and view a bar chart of ingredient counts for the selected meal.
    - **Recipe Detail Frame:** View detailed information about a selected recipe.

## Screenshots

1. **Entering Information:**

   ![Screenshot 2024-07-21 121006](https://github.com/user-attachments/assets/4534f8d2-b557-401f-b7fa-bc32ac989f8e)


2. **Viewing Meal Plan:**

   ![Screenshot 2024-07-21 121054](https://github.com/user-attachments/assets/957ccebb-b196-4d45-87a8-d8539b3aeec2)


3. **Checking Grocery List:**

   ![Screenshot 2024-07-21 121154](https://github.com/user-attachments/assets/7073c03a-0d30-4383-a046-ec965d07d1cd)


## Troubleshooting

- **Database Issues:** Ensure that `setup_database.py` has been run successfully and that the database file `meal_planner.db` exists in the project directory.
- **Missing Libraries:** If you encounter missing library errors, verify that all required libraries are installed.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Contributions are welcome!

## Contact

For any questions or feedback, please contact ganeshmumbai2001@gmail.com
