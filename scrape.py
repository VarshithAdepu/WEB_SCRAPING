import requests
from bs4 import BeautifulSoup

def get_recipe_data(url):
    # Fetch the webpage content
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page with status code: {response.status_code}")
        return None
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract recipe title
    title = soup.find('h1').text.strip()  # Assuming the title is in an <h1> tag
    
    # Extract ingredients (adjust class based on the website)
    ingredients = []
    for ingredient in soup.find_all(class_='ingredient'):
        ingredients.append(ingredient.text.strip())
    
    # Extract instructions (adjust class based on the website)
    instructions = []
    for step in soup.find_all(class_='instruction'):
        instructions.append(step.text.strip())
    
    # Compile the data
    recipe = {
        "title": title,
        "ingredients": ingredients,
        "instructions": instructions
    }
    
    return recipe

def save_recipe_to_file(recipe, filename):
    with open(filename, 'w') as file:
        file.write(f"Recipe Title: {recipe['title']}\n\n")
        file.write("Ingredients:\n")
        for ing in recipe['ingredients']:
            file.write(f"- {ing}\n")
        
        file.write("\nInstructions:\n")
        for step in recipe['instructions']:
            file.write(f"{step}\n")

# Example usage
recipe_url = 'https://hebbarskitchen.com/recipes/south-indian-dosa-recipes/'
recipe_data = get_recipe_data(recipe_url)

if recipe_data:
    save_recipe_to_file(recipe_data, 'recipe.txt')
    print("Recipe data saved to recipe.txt")
