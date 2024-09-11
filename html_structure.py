# from urllib.request import urlopen

# url = "https://hebbarskitchen.com/recipes/south-indian-dosa-recipes"
# page = urlopen(url)
# html_bytes = page.read()
# html = html_bytes.decode("utf-8")
# print(html)
from urllib.request import urlopen, Request

url = "https://hebbarskitchen.com/sponge-dosa-recipe-curd-dosa-set-dosa/"
headers = {'User-Agent': 'Mozilla/5.0'}

# Create a request with the custom user-agent
request = Request(url, headers=headers)
page = urlopen(request)

html_bytes = page.read()
html = html_bytes.decode("utf-8")
print(html)
