import re
import time
import os
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Base URL for scraping
baseurl = "https://www.allrecipes.com/recipe/"

# Lists to store scraped data
recipes = []  # List of all recipe names
links = []  # List of all recipe URLs
ingredients = []  # List of all recipe ingredients

# Directory to store the .txt files
output_dir = "recipes"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through a range of recipe IDs
for i in range(23000, 23132):  # Adjust the range as needed
    try:
        url = baseurl + str(i)
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        # Create request with user-agent
        request = Request(url, headers=headers)
        
        # Fetch page content
        with urlopen(request) as page:
            html_bytes = page.read()
            html = html_bytes.decode("utf-8")
        
        # Extract the title of the recipe (name)
        title_pattern = "<title.*?>.*?</title.*?>"
        title_match = re.search(title_pattern, html, re.IGNORECASE)
        
        if title_match:
            title = re.sub("<.*?>", "", title_match.group()).strip()
            title = re.sub("\| Allrecipes", "", title).strip()
            title = re.sub("Recipe", "", title).strip()
            recipes.append(title)
        
        # Extract the URL of the recipe
        url_pattern = r'"url": ".*?"'
        url_match = re.search(url_pattern, html, re.IGNORECASE)
        
        if url_match:
            recipe_url = re.sub('"url":', "", url_match.group()).strip().replace('"', "")
            links.append(recipe_url)
        
        # Extract ingredients of the recipe
        ingredients_pattern = r'(?<="recipeIngredient": \[)[\S\s]*?(?=\])'
        ingredients_match = re.search(ingredients_pattern, html, re.IGNORECASE)
        
        if ingredients_match:
            ingridients = ingredients_match.group()
            ingridients = re.sub('"', "", ingridients).strip()
            ingredients_list = ingridients.split(',')
            ingredients.append(ingredients_list)
        
        # Save recipe data to a .txt file
        file_name = f"{output_dir}/{title}.txt"
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(f"Recipe Name: {title}\n")
            f.write(f"URL: {recipe_url}\n")
            f.write("Ingredients:\n")
            for ingredient in ingredients_list:
                f.write(f"- {ingredient.strip()}\n")
        
        # Print progress
        print(f"Saved recipe: {title}")
        
        # Rate limiting to avoid overloading the server
        time.sleep(1)
    
    except (HTTPError, URLError) as e:
        print(f"Error fetching URL {url}: {e}")
        continue
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        continue

print(f"Finished scraping. {len(recipes)} recipes saved.")
