import pandas as pd
import json

def generate_meal_plan_LSM(protein_goal, carbs_goal, fat_goal, nbr_days):
        excel_file_path = 'database_agogo.xlsx'

        # Read the data from the 'recipee' table in the Excel file
        try:
            df = pd.read_excel(excel_file_path, sheet_name='recipee')
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            df = pd.DataFrame()

        # Convert the DataFrame to a list of dictionaries
        meals = df.to_dict(orient='records')
        
        # Fetch all meals
        
        breakfast_weight = 1
        lunch_weight = 1
        dinner_weight = 1
        breakfasts = [meal for meal in meals if meal["meal_type"] == 'Breakfast']
        lunches = [meal for meal in meals if meal["meal_type"] == 'Lunch']
        dinners = [meal for meal in meals if meal["meal_type"]== 'Dinner']
        
        # Use a heap to keep track of the top 7 combinations
        combinations  = []
        
        # Generate all possible combinations of meals for breakfast, lunch, and dinner
        for breakfast in breakfasts:
            for lunch in lunches:
                for dinner in dinners:
                    if (dinner["name"]!= lunch ["name"] and dinner["name"]!= breakfast ["name"] and lunch["name"]!= breakfast ["name"]):
                        for breakfast_servings in range(1, int(breakfast["servings"]) + 1):  # Assuming servings is an integer
                            for lunch_servings in range(1, int(lunch["servings"]) + 1):
                                for dinner_servings in range(1, int(dinner["servings"]) + 1):
                                    protein_meals = (breakfast["protein"] * breakfast_servings * breakfast_weight + 
                                                    lunch["protein"] * lunch_servings * lunch_weight+ 
                                                    dinner["protein"] * dinner_servings * dinner_weight)
                                    carbs_meals = (breakfast["carbs"] * breakfast_servings * breakfast_weight + 
                                                lunch["carbs"] * lunch_servings * lunch_weight+ 
                                                dinner["carbs"] * dinner_servings * dinner_weight)
                                    fat_meals = (breakfast["fat"] * breakfast_servings * breakfast_weight + 
                                                lunch["fat"] * lunch_servings * lunch_weight + 
                                                dinner["fat"] * dinner_servings * dinner_weight)
                                    
                                    # Calculate LSM score
                                    score = (4*(protein_goal - protein_meals)**2 + 
                                            (carbs_goal - carbs_meals)**2 + 
                                            (fat_goal - fat_meals)**2)
                                    
                                    combination = {
                                    "breakfast": breakfast["name"],
                                    "lunch": lunch["name"],
                                    "dinner": dinner["name"],
                                    "breakfast_servings": breakfast_servings,
                                    "lunch_servings": lunch_servings,
                                    "dinner_servings": dinner_servings,
                                    "score": score
                                    }
                                    combinations.append(combination)
   
        # Sort the combinations based on LSM score in ascending order
        combinations .sort(key=lambda x: x["score"])
        nbr_days = int(nbr_days)
        best_combinations = combinations[:nbr_days]
        return json.dumps({"best_combinations": best_combinations}, default=lambda x: float(x) if isinstance(x, Decimal) else x)




i = generate_meal_plan_LSM(protein_goal = 20, carbs_goal = 50, fat_goal = 20, nbr_days = 2)
print (i)