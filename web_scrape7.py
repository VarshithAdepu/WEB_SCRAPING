import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Function to get the HTML content of a webpage, handle 404 errors gracefully
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.content
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} for URL: {url}")
        return None  # Return None for invalid pages

# Function to extract recipe links from a page
def extract_recipe_links(page_url):
    html_content = get_html(page_url)
    
    if not html_content:
        # If the page returned a 404 error or other issue, return an empty set
        return set()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    print(f"Extracting from page: {page_url}")
    
    recipe_links = set()  # Use a set to avoid duplicates
    for link in soup.find_all('a', href=True):
        url = link['href']
        if "https://hebbarskitchen.com/hi/" in url and "-recipe" in url and "-recipes" not in url and "#comments" not in url and "#respond" not in url:
            recipe_links.add(url)
    
    return recipe_links

# Function to get recipe data from a URL
def get_recipe_data(recipe_url):
    try:
        recipe_html = get_html(recipe_url)
        
        if not recipe_html:
            return None, None, None, None  # Skip invalid pages
        
        recipe_soup = BeautifulSoup(recipe_html, 'html.parser')

        recipe_name = recipe_soup.find('h1').get_text().strip()

        ingredients_section = recipe_soup.find('div', class_='wprm-recipe-ingredients-container')
        ingredients = []
        if ingredients_section:
            ingredients_list = ingredients_section.find_all('li')
            for item in ingredients_list:
                ingredients.append(item.get_text().strip())
        ingredients_str = ", ".join(ingredients)

        instructions_section = recipe_soup.find('div', class_='wprm-recipe-instructions-container')
        instructions = []
        if instructions_section:
            instructions_list = instructions_section.find_all('li')
            for step in instructions_list:
                instructions.append(step.get_text().strip())
        instructions_str = " ".join(instructions)

        return recipe_name, recipe_url, ingredients_str, instructions_str

    except Exception as e:
        print(f"An error occurred for {recipe_url}: {e}")
        return None, None, None, None

# Read URLs from the Excel file
recipes_file_path = "hebbars_recipes_hi1.xlsx"
df_recipes = pd.read_excel(recipes_file_path)
urls = df_recipes['URL'].tolist()

# Create a folder to save individual Excel files
output_folder = "scraped_recipes"
os.makedirs(output_folder, exist_ok=True)

# Process each base URL (from the Excel file)
for base_url in urls:
    print(f"Processing base URL: {base_url}")
    
    # Initialize empty lists to store recipe data for this base URL
    recipe_names = []
    recipe_urls = []
    recipe_ingredients = []
    recipe_instructions = []
    
    # Scrape pages for the current base URL
    page_number = 1
    while True:
        page_url = f"{base_url}page/{page_number}/"
        recipe_links = extract_recipe_links(page_url)
        
        if not recipe_links:
            print(f"No more recipes found or invalid page at page {page_number}. Stopping.")
            break  # Stop if no more valid pages
        
        for recipe_url in recipe_links:
            if recipe_url not in recipe_urls:  # Ensure unique URLs
                recipe_name, url, ingredients, instructions = get_recipe_data(recipe_url)
                if recipe_name:
                    recipe_names.append(recipe_name)
                    recipe_urls.append(url)
                    recipe_ingredients.append(ingredients)
                    recipe_instructions.append(instructions)
        
        print(f"Finished scraping page {page_number}.")
        page_number += 1
        time.sleep(1)  # Rate limiting to avoid overloading the server
    
    # Create a DataFrame and save it to an Excel file immediately after scraping the base URL
    df = pd.DataFrame({
        "Recipe Name": recipe_names,
        "URL": recipe_urls,
        "Ingredients": recipe_ingredients,
        "Instructions": recipe_instructions
    })

    # Create a safe filename based on the base URL
    safe_base_url = base_url.replace('https://', '').replace('/', '_')
    xlsx_file_path = os.path.join(output_folder, f"{safe_base_url}.xlsx")
    
    # Save DataFrame to Excel file
    df.to_excel(xlsx_file_path, index=False)
    print(f"Recipes from {base_url} saved to {xlsx_file_path}.")
    
    # Rate limiting to avoid overloading the server
    time.sleep(1)

print("Finished processing all base URLs.")
