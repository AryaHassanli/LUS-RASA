from api import get_cuisines, get_ingredients, get_recipes
import random

num_of_examples = 5000

templates = [
    # Nothing
    "I want to cook something today",
    "give me the recipe of some food",
    "give me the recipe of something for dinner",
    "what can i cook today",
    "suggest me a food",
    "suggest me a meal",
    "recommend a food",
    "recommend a dinner",
    "recommend a meal",
    "what food do you suggest today",
    "could you please suggest me some food",

    # Cuisine
    "i want to cook a {cuisine} food",
    "i want to cook some {cuisine} food for dinner",
    "i want to cook some {cuisine} lunch",
    "i want to cook some {cuisine} dinner",
    "what can i cook from {cuisine} cuisine for lunch",
    "what {cuisine} food should i cook today",
    "could you find me a {cuisine} food for dinner",
    "could you search for some {cuisine} food",
    "could you search me some {cuisine} meal",
    "are you able to find some {cuisine} food for me",
    "find me an {cuisine} food",
    "recommend me an {cuisine} food",
    "give me the recipe of a {cuisine} food",
    "give me the recipe of a {cuisine} cuisine",
    "suggest me a {cuisine} food",
    "suggest an {cuisine} food",
    "suggest me the recipe of a {cuisine} cuisine",

    # Cuisine and Ingredient
    "i want to cook some {cuisine} food with {ingredient} and without {ingredient_ex}",
    "i want to cook some {cuisine} cuisine with {ingredient}",
    "find me a {cuisine} food with {ingredient}",
    "find me a {cuisine} food that does not contain {ingredient_ex}",
    "what {cuisine} food with {ingredient} should i cook today",
    "find me an {cuisine} food without {ingredient_ex}",
    "give me the recipe of an {cuisine} food made by {ingredient}",
    "give me the recipe of an {cuisine} meal made by {ingredient}",
    "give me the recipe of a {cuisine} food without {ingredient_ex}",
    "what {cuisine} food  can i cook with {ingredient}",
    "how can i cook some {cuisine} food with {ingredient}",
    "could you find some {cuisine} food with {ingredient}",
    "what {cuisine} food  can i cook includes {ingredient}",
    "what {cuisine} dinner  can i cook includes {ingredient}",
    "what {cuisine} meal  can i cook includes {ingredient}",
    "what {cuisine} food  can i cook includes {ingredient} for lunch",
    "how can i cook some {cuisine} food includes {ingredient}",
    "could you find some {cuisine} food includes {ingredient}",
    "give me the recipe of an {cuisine} food that contains {ingredient} and does not have {ingredient_ex}",
    "give me the recipe of a {cuisine} food that has {ingredient}",
    "what {cuisine} food  can i cook made by {ingredient}",
    "recommend me the recipe of a {cuisine} food that has {ingredient}. i dont like {ingredient_ex}",
    "recommend me a {cuisine} food that contains {ingredient}. i prefer it without {ingredient_ex}",
    "what {cuisine} food  can i cook contains {ingredient}. please give some without {ingredient_ex}",
    "I like {cuisine} food and do not like {ingredient_ex}. what can i cook?",
    "I like {cuisine} dinner and do not like {ingredient_ex}. what can i cook for lunch?",
    "I like {cuisine} food and do not like {ingredient_ex}. can you recommend me a food?",
    "I prefer {cuisine} food and do not like {ingredient_ex}. can you suggest me a food?",    
    "I prefer {cuisine} lunch and do not like {ingredient_ex}. can you suggest me a food?",    
    "I love {cuisine} food and prefer {ingredient}. also do not like {ingredient_ex}. can you suggest me a food?",
    # Ingredient
    "today i have {ingredient}. what can i cook? I also do not like {ingredient_ex}",
    "what should i cook today with {ingredient}",
    "what can i cook with {ingredient}",
    "how to made some food with {ingredient}. i dont have {ingredient_ex}.",
    "can i cook some food with {ingredient}",
    "can i cook something for lunch with {ingredient}",
    "i have some {ingredient}. what can i cook with them",
    "can i cook something with {ingredient}",
    "do you have any food suggestion with {ingredient}",
    "suggest some food that contains {ingredient}.",
    "i dont like {ingredient_ex}. what can i cook today?",
    "can i cook somethin with {ingredient} and without {ingredient_ex}",
    "i have allergy to {ingredient_ex}. what can i cook with {ingredient}.",
]

cuisines = get_cuisines()
ingredients = get_ingredients()

def generate_ingredients_text(ingredients, role):
    if len(ingredients) == 0:
        return ""
    if len(ingredients) == 1:
        return '[{}]{{"entity":"ingredient","role":"{}"}}'.format(ingredients[0],role)
    
    s = '[{}]{{"entity":"ingredient","role":"{}"}}'.format(ingredients[0],role)
    for ingredient in ingredients[1:]:
        s += ", "
        if random.choice([True, False]):
            s += "and "
        s += '[{}]{{"entity":"ingredient","role":"{}"}}'.format(ingredient,role)
    return s

out_file = open('data/nlu-inform.yml', 'w')
out_file.write('version: "2.0"\n\n')
out_file.write('nlu:\n')
out_file.write('- intent: inform\n')
out_file.write('  examples: |\n')

for i in range(num_of_examples):
    template = templates[random.randint(0, len(templates)-1)]

    cuisine = cuisines[random.randint(0,len(cuisines)-1)]
    cuisine = "[{}](cuisine)".format(cuisine)

    num_of_ingredients = random.randint(1,4)
    ingredient = []
    for i in range(num_of_ingredients + 1):
        ingredient.append(
            ingredients[random.randint(0,len(ingredients)-1)]
        )
    ingredient = generate_ingredients_text(ingredient,"add")

    num_of_ingredients_ex = random.randint(1,2)
    ingredient_ex = []
    for i in range(num_of_ingredients_ex + 1):
        ingredient_ex.append(
            ingredients[random.randint(0,len(ingredients)-1)]
        )
    ingredient_ex = generate_ingredients_text(ingredient_ex,"remove")

    data = {
        "cuisine" : cuisine,
        "ingredient": ingredient,
        "ingredient_ex": ingredient_ex
    }
    template = template.format(**data)

    out_file.write('    - {}\n'.format(template))

out_file.close()
