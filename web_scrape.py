recipies =[] 
#list of all the recipe names

link =[] 
#list of all the recipe url

ingri = [] 
#list of all the recipe ingredients

for i in range(23000, 23132):
        try:
            
            url = baseurl + str(i) 
            #adding the page to the base url
            
            page = urlopen(url)
            html_bytes = page.read() 
            html = html_bytes.decode("utf-8") 
            
            pattern = "<title.*?>.*?</title.*?>" 
            #regex to extract the title of the page - this contains the name
            match_results = re.search(pattern, html, re.IGNORECASE)
            title = match_results.group()
            title = re.sub("<.*?>", "", title) 
            #removing the <title> tag from the found pattern
            title = re.sub("\| Allrecipes", "", title) 
	    #removing the unwanted data from the found pattern
            title = re.sub("Recipe", "", title) 
	    #removing the Recipe at the end of the name (completely optional)
            
            recipies.append(title) 
	    #adding the data to the list
            
            #print(title)
            
            pattern2 = r'"url": ".*?"' 
	    #regex to extract the complete url of the page
            match_results2 = re.search(pattern2, html, re.IGNORECASE)
            url2 = match_results2.group() 
            url2 = re.sub('"url":', "", url2) 
	    #removing the unwanted '"url": ' tag from the found pattern
            url2 = re.sub('"', "", url2) 
	    #removing unwanted " marks
            
            link.append(url2) 
	    #adding the data to the list 
            
            #print(url2)
            
            pattern3 = '(?<="recipeIngredient": \[)[\S\s]*(?="recipeInstructions")' 
	    #regex to extract the ingredients
            match_results3 = re.search(pattern3, html, re.IGNORECASE)
            ingridients = match_results3.group()
            ingridients = re.sub('\],', "", ingridients) 
	    #removing unwanted symbols from the pattern found
            ingridients = re.sub('"', "", ingridients) 
	    #removing unwanted symbols from the pattern found
            ingridients = re.sub('\n', "", ingridients) 
	    #removing new lines from the pattern
            ingridients = re.sub('\\s+', ' ', ingridients) 
	    #removing multiple white spaces and replacing it with single white space
            ingridients = ingridients.split(',') 
	    #converting the string to a list so that it could be converted into multiple rows later
            
            ingri.append(ingridients) #adding the data to the list 
            
            #print(ingridients)
            
        except:
            continue
