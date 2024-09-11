import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL for breakfast recipes (Hindi)
base_url = "https://hebbarskitchen.com/hi/recipes/breakfast-recipes-hi/"

# Function to get the HTML content of a webpage
def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.content

# Function to extract the maximum number of pages
def get_max_pages(url):
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Print the HTML content of the pagination section for debugging
    pagination_section = soup.find('div', class_='pagination')
    if pagination_section:
        print("Pagination section found.")
        print(pagination_section.prettify())
    
    # Extract maximum page number from pagination links
    pagination_links = soup.find_all('a', href=True)
    max_page = 1
    for link in pagination_links:
        href = link['href']
        if 'page' in href:
            try:
                page_number = int(href.split('page/')[1].split('/')[0])
                if page_number > max_page:
                    max_page = page_number
            except ValueError:
                continue
    
    return max_page

# Function to extract recipe links from a page
def extract_recipe_links(page_url):
    html_content = get_html(page_url)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Print the HTML content of the page for debugging
    print(f"Extracting from page: {page_url}")
    print(soup.prettify())
    
    recipe_links = set()  # Use a set to avoid duplicates
    for link in soup.find_all('a', href=True):
        url = link['href']
        # Filter only recipe URLs
        if "https://hebbarskitchen.com/" in url and "-recipe" in url and "-recipes" not in url and "#comments" not in url and "#respond" not in url:
            recipe_links.add(url)
    
    return recipe_links

# Function to get recipe data from a URL
def get_recipe_data(recipe_url):
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

        return recipe_name, recipe_url, ingredients_str, instructions_str

    except Exception as e:
        print(f"An error occurred for {recipe_url}: {e}")
        return None, None, None, None

# Get the maximum number of pages
try:
    max_pages = get_max_pages(base_url)
    print(f"Maximum number of pages: {max_pages}")

    # Initialize empty lists to store recipe data
    recipe_names = []
    recipe_urls = []
    recipe_ingredients = []
    recipe_instructions = []

    # Scrape pages up to the maximum number of pages
    for page_number in range(1, max_pages + 1):
        print(f"Scraping page {page_number}...")
        page_url = f"{base_url}page/{page_number}/"
        recipe_links = extract_recipe_links(page_url)
        
        if not recipe_links:
            print("No more recipes found on this page. Ending scraping.")
            break  # Exit the loop if no recipes found on the page
        
        for recipe_url in recipe_links:
            if recipe_url not in recipe_urls:  # Ensure unique URLs
                recipe_name, url, ingredients, instructions = get_recipe_data(recipe_url)
                if recipe_name:
                    recipe_names.append(recipe_name)
                    recipe_urls.append(url)
                    recipe_ingredients.append(ingredients)
                    recipe_instructions.append(instructions)

        # Rate limiting to avoid overloading the server
        time.sleep(1)

    # Create a DataFrame and save it to an Excel file
    df = pd.DataFrame({
        "Recipe Name": recipe_names,
        "URL": recipe_urls,
        "Ingredients": recipe_ingredients,
        "Instructions": recipe_instructions
    })

    # Save DataFrame to Excel file
    xlsx_file_path = "hebbars_breakfast_recipes_hi_with_instructions.xlsx"
    df.to_excel(xlsx_file_path, index=False)

    print(f"Finished scraping. Recipes saved to {xlsx_file_path}.")

except Exception as e:
    print(f"An error occurred: {e}")
