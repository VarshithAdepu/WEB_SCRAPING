import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# Path to the Excel file with recipe URLs
xlsx_file_path = "hebbars_breakfast_recipes_hi.xlsx"


# Step 1: Read the existing Excel sheet
df = pd.read_excel(xlsx_file_path)

# Step 2: Initialize empty lists to store extracted data
recipe_names = []
recipe_ingredients = []

# Step 3: Define a function to extract data from a recipe URL
def extract_recipe_data(recipe_url):
    try:
        # Get the HTML content of the recipe page
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(recipe_url, headers=headers)
        recipe_soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the recipe name (assuming it's in the <h1> tag)
        recipe_name = recipe_soup.find('h1').get_text().strip()

        # Extract the ingredients (assuming they are within <li> elements)
        ingredients = []
        ingredients_list = recipe_soup.find_all('li')
        for item in ingredients_list:
            ingredients.append(item.get_text().strip())

        # Convert the ingredients list to a single string separated by commas
        ingredients_str = ", ".join(ingredients)

        return recipe_name, ingredients_str

    except Exception as e:
        print(f"Error extracting data from {recipe_url}: {e}")
        return None, None

# Step 4: Iterate through each URL in the DataFrame and extract data
for index, row in df.iterrows():
    recipe_url = row['URL']

    # Extract the recipe data from the URL
    recipe_name, ingredients_str = extract_recipe_data(recipe_url)

    # Append the extracted data to the lists
    recipe_names.append(recipe_name)
    recipe_ingredients.append(ingredients_str)

    # Print progress
    print(f"Extracted data from: {recipe_url}")

    # Optional: Delay to avoid overloading the server
    time.sleep(1)

# Step 5: Add the extracted data to the DataFrame
df['Recipe Name'] = recipe_names
df['Ingredients'] = recipe_ingredients

# Step 6: Save the updated DataFrame back to the Excel sheet
df.to_excel(xlsx_file_path, index=False)

print(f"Data extraction completed. The Excel sheet has been updated.")
