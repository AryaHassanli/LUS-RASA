from api import get_cuisines, get_ingredients, get_recipes
import random

num_of_examples = 4000

templates = [
    "i want to add {ingredient}",
    "i want to include {ingredient}",
    "i want it to contain {ingredient}",
    "i want to remove {ingredient_ex}",
    "i want to delete {ingredient_ex}",
    "i want to exclude {ingredient_ex}",
    "i want it to not contain {ingredient_ex}",

    "yes please add {ingredient}",
    "yes please inlude {ingredient}",
    "yes please remove {ingredient_ex}",
    "yes please exclude {ingredient_ex}",

    "could you add {ingredient}",
    "could you remove {ingredient_ex}",
    "could you insert {ingredient}",
    "could you please exlcude {ingredient_ex}",
    
    "oh please remove {ingredient_ex}",
    "oh please forget about {ingredient_ex}",
    "umm add {ingredient}",
    "yes i want to change it. add {ingredient}",
    "yes i want to change it. remove {ingredient_ex}",
    "yes add {ingredient}",
    "yes remove {ingredient_ex}",
    "yes make it with {ingredient}",
    "give me some without {ingredient_ex}",
    'i want also to include {ingredient}',
    'i want also to exclude {ingredient_ex}',
    'i want also to contain {ingredient}',
    'i want also to delete {ingredient_ex}',
    'also add {ingredient} too',
    'also delete {ingredient_ex} too',
    'also remove {ingredient_ex}',
    'also add {ingredient} please',
    'also exclude {ingredient_ex} please',
    'also exclude {ingredient_ex}',
    "no add {ingredient} please",
    "add {ingredient}",
    "remove {ingredient_ex}",
    "forget about {ingredient_ex} please",
    "with {ingredient} please",
    "yes make it without {ingredient_ex}",
    'i dont like {ingredient_ex} today',
    'i dont want {ingredient_ex}',
    'today i do not have {ingredient_ex}',
    'please give me one without {ingredient_ex}',
    'i want something without {ingredient_ex}',
    'i want it to be without {ingredient_ex}',
    'search for some without {ingredient_ex}',
    'no i do not have {ingredient_ex}',
    'i dont have {ingredient_ex} today',
    'i want it with {ingredient}',
    'i want it with {ingredient} and without {ingredient_ex}',
    'i want to add {ingredient} and remove {ingredient_ex}',
    'add {ingredient} and delete {ingredient_ex}',
    'add {ingredient} and forget about {ingredient_ex}',
    'could you also add {ingredient} and do not include {ingredient_ex}',
    'include {ingredient} and exclude {ingredient_ex}',
    'do not include {ingredient_ex}',
    'please not include {ingredient_ex}',
    "no remove {ingredient_ex}",
    "no forget about {ingredient_ex} please",
    "no with {ingredient} please",
    "no make it without {ingredient_ex}",
    'no i dont like {ingredient_ex} today',
    'no i dont want {ingredient_ex}',
    'no today i do not have {ingredient_ex}',
    'no please give me one without {ingredient_ex}',
    'no i want something without {ingredient_ex}',
    'no i want it to be without {ingredient_ex}',
    'no search for some without {ingredient_ex}',
    'no i dont have {ingredient_ex} today',
    'no i want it with {ingredient}',
    'no i want it with {ingredient} and without {ingredient_ex}',
    'no i want to add {ingredient} and remove {ingredient_ex}',
    'no add {ingredient} and delete {ingredient_ex}',
    'no add {ingredient} and forget about {ingredient_ex}',
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

out_file = open('data/nlu-inform_ingredient.yml', 'w')
out_file.write('version: "2.0"\n\n')
out_file.write('nlu:\n')
out_file.write('- intent: inform_ingredient\n')
out_file.write('  examples: |\n')

for i in range(num_of_examples):
    template = templates[random.randint(0, len(templates)-1)]

    num_of_ingredients = random.randint(1,2)
    ingredient = []
    for i in range(num_of_ingredients + 1):
        ingredient.append(
            ingredients[random.randint(0,len(ingredients)-1)]
        )
    ingredient = generate_ingredients_text(ingredient,"add")

    ingredient_ex = []
    for i in range(num_of_ingredients + 1):
        ingredient_ex.append(
            ingredients[random.randint(0,len(ingredients)-1)]
        )
    ingredient_ex = generate_ingredients_text(ingredient_ex,"remove")
    

    data = {
        "ingredient": ingredient,
        "ingredient_ex": ingredient_ex
    }
    template = template.format(**data)

    out_file.write('    - {}\n'.format(template))

out_file.close()
