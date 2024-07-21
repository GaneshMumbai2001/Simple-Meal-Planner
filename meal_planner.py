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
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12))
        
        # Initialize frames
        self.frames = {}
        for F in (InitialPage, WelcomeFrame, MealPlanFrame, RecipeDetailFrame, GroceryListFrame):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("InitialPage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class InitialPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e0f2f1")
        self.controller = controller
        
        ttk.Label(self, text="Meal Planner", font=("Helvetica", 24, "bold"), background="#e0f2f1", foreground="#004d40").pack(pady=20)
        
        self.meal_names_text = tk.Text(self, wrap="word", width=50, height=10, font=("Helvetica", 12), bg="#ffffff", fg="#004d40")
        self.meal_names_text.pack(pady=10)
        
        self.healthy_tips_text = tk.Text(self, wrap="word", width=50, height=5, font=("Helvetica", 12), bg="#ffffff", fg="#004d40")
        self.healthy_tips_text.pack(pady=10)
        
        ttk.Button(self, text="Continue", command=self.go_to_welcome, style="TButton").pack(pady=20)
        
        self.display_initial_info()
    
    def display_initial_info(self):
        # Fetch initial meal names and healthy tips
        initial_meals = get_recipes("", "", "")[:5]  # Simple selection of 5 meals
        healthy_tips = [
            "Stay hydrated! Drink plenty of water.",
            "Include a variety of fruits and vegetables in your diet.",
            "Choose whole grains over refined grains.",
            "Opt for lean proteins like fish, chicken, and beans.",
            "Limit added sugars and salt."
        ]
        
        self.meal_names_text.delete(1.0, tk.END)
        for meal in initial_meals:
            self.meal_names_text.insert(tk.END, meal.get("name", "No Name") + "\n")
        
        self.healthy_tips_text.delete(1.0, tk.END)
        for tip in healthy_tips:
            self.healthy_tips_text.insert(tk.END, "• " + tip + "\n")
    
    def go_to_welcome(self):
        self.controller.show_frame("WelcomeFrame")

class WelcomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e0f7fa")
        self.controller = controller
        
        ttk.Label(self, text="Dietary Preferences (e.g., vegetarian, vegan, gluten-free)", background="#e0f7fa").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.dietary_preferences = ttk.Entry(self, width=40)
        self.dietary_preferences.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(self, text="Allergies or Restrictions", background="#e0f7fa").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.allergies = ttk.Entry(self, width=40)
        self.allergies.grid(row=1, column=1, padx=10, pady=10)
        
        ttk.Label(self, text="Available Ingredients", background="#e0f7fa").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.ingredients = ttk.Entry(self, width=40)
        self.ingredients.grid(row=2, column=1, padx=10, pady=10)
        
        ttk.Button(self, text="Submit", command=self.submit_info, style="TButton").grid(row=3, column=0, columnspan=2, pady=20, sticky="n")
    
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
        
        ttk.Label(self, text="Your Meal Plan for the Week", font=("Helvetica", 16), background="#e0f2f1", foreground="#004d40").pack(pady=20)
        
        self.meal_plan_text = tk.Text(self, wrap="word", width=50, height=10, font=("Helvetica", 12), bg="#ffffff", fg="#004d40")
        self.meal_plan_text.pack(pady=10)
        
        ttk.Button(self, text="Back", command=lambda: controller.show_frame("WelcomeFrame"), style="TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(self, text="Grocery List", command=self.show_grocery_list, style="TButton").pack(side=tk.RIGHT, padx=10)
    
    def generate_meal_plan(self, dietary_preferences, allergies, ingredients):
        self.recipes = get_recipes(dietary_preferences, allergies, ingredients)
        self.meal_plan = self.recipes[:7]  # Simple selection of 7 meals
        
        self.meal_plan_text.delete(1.0, tk.END)
        for meal in self.meal_plan:
            self.meal_plan_text.insert(tk.END, meal.get("name", "No Name") + "\n")
            ttk.Button(self, text=meal.get("name", "No Name"), command=lambda m=meal: self.show_recipe(m), style="TButton").pack()
    
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
        
        ttk.Label(self, text="Grocery List", font=("Helvetica", 16), background="#e0f2f1", foreground="#004d40").pack(pady=20)
        
        self.grocery_list_text = tk.Text(self, wrap="word", width=50, height=10, font=("Helvetica", 12), bg="#ffffff", fg="#004d40")
        self.grocery_list_text.pack(pady=10)
        
        ttk.Button(self, text="Back", command=lambda: controller.show_frame("MealPlanFrame"), style="TButton").pack(pady=10)
    
    def generate_grocery_list(self):
        all_ingredients = set()
        for meal in self.controller.frames["MealPlanFrame"].meal_plan:
            all_ingredients.update(meal.get("ingredients", []))
        
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
        ax.bar(["Ingredients"], [len(meal.get("ingredients", []))], color="#00796b")
        ax.set_title(f"Ingredients for {meal.get('name', 'Meal')}")
        ax.set_ylabel("Count")
        
        # Embed the chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

class RecipeDetailFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e0f2f1")
        self.controller = controller
        
        self.recipe_name_label = ttk.Label(self, text="", font=("Helvetica", 16), background="#e0f2f1", foreground="#004d40")
        self.recipe_name_label.pack(pady=10)
        
        self.recipe_ingredients_text = tk.Text(self, wrap="word", width=50, height=10, font=("Helvetica", 12), bg="#ffffff", fg="#004d40")
        self.recipe_ingredients_text.pack(pady=10)
        
        self.recipe_instructions_text = tk.Text(self, wrap="word", width=50, height=10, font=("Helvetica", 12), bg="#ffffff", fg="#004d40")
        self.recipe_instructions_text.pack(pady=10)
        
        ttk.Button(self, text="Back to Meal Plan", command=lambda: controller.show_frame("MealPlanFrame"), style="TButton").pack(pady=10)
    
    def show_recipe(self, meal):
        self.recipe_name_label.config(text=meal.get("name", "No Name"))
        self.recipe_ingredients_text.delete(1.0, tk.END)
        self.recipe_ingredients_text.insert(tk.END, "\n".join(meal.get("ingredients", [])))
        self.recipe_instructions_text.delete(1.0, tk.END)
        self.recipe_instructions_text.insert(tk.END, meal.get("instructions", "No Instructions"))

if __name__ == "__main__":
    app = MealPlannerApp()
    app.mainloop()
