import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL for breakfast recipes (Hindi)
main_url = "https://hebbarskitchen.com/hi/recipes/"

# Function to get the HTML content of a webpage
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    return response.content

# Step 1: Extract all recipe links from the main page
html_content = get_html(main_url)
soup = BeautifulSoup(html_content, 'html.parser')

# Step 2: Find all recipe links
recipe_links = []
for link in soup.find_all('a', href=True):
    url = link['href']
    # Filter only recipe URLs
    if "https://hebbarskitchen.com/hi/" in url and "-recipes" in url and "#comments" not in url and "#respond" not in url:
        if url not in recipe_links:  # Ensure unique URLs
            recipe_links.append(url)

# Step 3: Initialize empty lists to store recipe data
recipe_names = []
recipe_urls = []
recipe_ingredients = []
recipe_instructions = []

# Step 4: Visit each recipe link to extract the name, ingredients, and instructions
for recipe_url in recipe_links:
    try:
        recipe_html = get_html(recipe_url)
        recipe_soup = BeautifulSoup(recipe_html, 'html.parser')

        # Extract the recipe name (assuming it's in the <h1> tag)
        recipe_name = recipe_soup.find('h1').get_text().strip()

        # Extract the ingredients
        ingredients_section = recipe_soup.find('div', class_='wprm-recipe-ingredients-container')
        ingredients = []
        if ingredients_section:
            ingredients_list = ingredients_section.find_all('li')
            for item in ingredients_list:
                ingredients.append(item.get_text().strip())
        ingredients_str = ", ".join(ingredients)

        # Extract the instructions
        instructions_section = recipe_soup.find('div', class_='wprm-recipe-instructions-container')
        instructions = []
        if instructions_section:
            instructions_list = instructions_section.find_all('li')
            for step in instructions_list:
                instructions.append(step.get_text().strip())
        instructions_str = " ".join(instructions)

        # Append the data to lists
        recipe_names.append(recipe_name)
        recipe_urls.append(recipe_url)
        recipe_ingredients.append(ingredients_str)
        recipe_instructions.append(instructions_str)

        # Print progress
        print(f"Scraped recipe: {recipe_name}")

        # Rate limiting to avoid overloading the server
        time.sleep(1)

    except Exception as e:
        print(f"An error occurred for {recipe_url}: {e}")
        continue

# Step 5: Create a DataFrame and save it to an Excel file
df = pd.DataFrame({
    "Recipe Name": recipe_names,
    "URL": recipe_urls,
    "Ingredients": recipe_ingredients,
    "Instructions": recipe_instructions
})

# Save DataFrame to Excel file
xlsx_file_path = "hebbars_recipes_hi.xlsx"
df.to_excel(xlsx_file_path, index=False)

print(f"Finished scraping. Recipes saved to {xlsx_file_path}.")
