import tkinter as tk
from tkinter import ttk, messagebox
from database import get_recipes
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MealPlannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Meal Planner")
        self.geometry("800x600")
        self.configure(bg="#f0f0f0")
        
        # Initialize frames
        self.frames = {}
        for F in (WelcomeFrame, MealPlanFrame, RecipeDetailFrame, GroceryListFrame):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("WelcomeFrame")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e0f7fa")
        self.controller = controller
        
        tk.Label(self, text="Dietary Preferences (e.g., vegetarian, vegan, gluten-free)", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.dietary_preferences = tk.Entry(self, width=40)
        self.dietary_preferences.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Allergies or Restrictions", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.allergies = tk.Entry(self, width=40)
        self.allergies.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(self, text="Available Ingredients", bg="#e0f7fa", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.ingredients = tk.Entry(self, width=40)
        self.ingredients.grid(row=2, column=1, padx=10, pady=10)
        
        tk.Button(self, text="Submit", command=self.submit_info, bg="#00796b", fg="white", font=("Helvetica", 12)).grid(row=3, column=0, columnspan=2, pady=20, sticky="n")
    
    def submit_info(self):
        dietary_preferences = self.dietary_preferences.get()
        allergies = self.allergies.get()
        ingredients = self.ingredients.get()
        
        if not dietary_preferences or not ingredients:
            messagebox.showerror("Input Error", "Please fill in all required fields")
            return
        
        self.controller.frames["MealPlanFrame"].generate_meal_plan(dietary_preferences, allergies, ingredients)
        self.controller.show_frame("MealPlanFrame")

class MealPlanFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e0f2f1")
        self.controller = controller
        
        self.meal_plan_label = tk.Label(self, text="Your Meal Plan for the Week", font=("Helvetica", 16), bg="#e0f2f1", fg="#004d40")
        self.meal_plan_label.pack(pady=20)
        
        self.meal_plan_text = tk.Text(self, wrap="word", width=50, height=10, font=("Helvetica", 12), bg="#ffffff", fg="#004d40")
        self.meal_plan_text.pack(pady=10)
        
        tk.Button(self, text="Back", command=lambda: controller.show_frame("WelcomeFrame"), bg="#00796b", fg="white", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(self, text="Grocery List", command=self.show_grocery_list, bg="#00796b", fg="white", font=("Helvetica", 12)).pack(side=tk.RIGHT, padx=10)
    
    def generate_meal_plan(self, dietary_preferences, allergies, ingredients):
        self.recipes = get_recipes(dietary_preferences, allergies, ingredients)
        self.meal_plan = self.recipes[:7]  # Simple selection of 7 meals
        
        self.meal_plan_text.delete(1.0, tk.END)
        for meal in self.meal_plan:
            self.meal_plan_text.insert(tk.END, meal["name"] + "\n")
            tk.Button(self, text=meal["name"], command=lambda m=meal: self.show_recipe(m), bg="#004d40", fg="white", font=("Helvetica", 12)).pack()
    
    def show_recipe(self, meal):
        self.controller.frames["RecipeDetailFrame"].show_recipe(meal)
        self.controller.show_frame("RecipeDetailFrame")
    
    def show_grocery_list(self):
        self.controller.frames["GroceryListFrame"].generate_grocery_list()
        self.controller.show_frame("GroceryListFrame")

class GroceryListFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e0f2f1")
        self.controller = controller
        
        self.grocery_list_label = tk.Label(self, text="Grocery List", font=("Helvetica", 16), bg="#e0f2f1", fg="#004d40")
        self.grocery_list_label.pack(pady=20)
        
        self.grocery_list_text = tk.Text(self, wrap="word", width=50, height=10, font=("Helvetica", 12), bg="#ffffff", fg="#004d40")
        self.grocery_list_text.pack(pady=10)
        
        tk.Button(self, text="Back", command=lambda: controller.show_frame("MealPlanFrame"), bg="#00796b", fg="white", font=("Helvetica", 12)).pack(pady=10)
    
    def generate_grocery_list(self):
        all_ingredients = set()
        for meal in self.controller.frames["MealPlanFrame"].meal_plan:
            all_ingredients.update(meal["ingredients"])
        
        available_ingredients = self.controller.frames["WelcomeFrame"].ingredients.get().split(', ')
        missing_ingredients = all_ingredients - set(available_ingredients)
        
        self.grocery_list_text.delete(1.0, tk.END)
        for ingredient in missing_ingredients:
            self.grocery_list_text.insert(tk.END, ingredient + "\n")

        # Display chart for next meal
        if self.controller.frames["MealPlanFrame"].meal_plan:
            self.show_meal_chart(self.controller.frames["MealPlanFrame"].meal_plan[0])
    
    def show_meal_chart(self, meal):
        # Create a chart for the meal
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(["Ingredients"], [len(meal["ingredients"])], color="#00796b")
        ax.set_title(f"Ingredients for {meal['name']}")
        ax.set_ylabel("Count")
        
        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

class RecipeDetailFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e0f2f1")
        self.controller = controller
        
        self.recipe_label = tk.Label(self, text="", font=("Helvetica", 16), bg="#e0f2f1", fg="#004d40")
        self.recipe_label.pack(pady=20)
        
        self.recipe_text = tk.Text(self, wrap="word", width=50, height=10, font=("Helvetica", 12), bg="#ffffff", fg="#004d40")
        self.recipe_text.pack(pady=10)
        
        tk.Button(self, text="Back", command=lambda: controller.show_frame("MealPlanFrame"), bg="#00796b", fg="white", font=("Helvetica", 12)).pack(pady=10)
    
    def show_recipe(self, meal):
        self.recipe_label.config(text=meal["name"])
        self.recipe_text.delete(1.0, tk.END)
        self.recipe_text.insert(tk.END, meal["recipe"])

if __name__ == "__main__":
    app = MealPlannerApp()
    app.mainloop()
