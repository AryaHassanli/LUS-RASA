import csv
import requests
import signal
from math import sin, cos, sqrt, atan2, radians
import os
import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted, SlotSet

import random
import http.client
import urllib.parse
import os
import json
import csv
import pickle
import spoonacular as sp
import requests
from unidecode import unidecode


class UserData():
    def __init__(self):
        self.cuisine = None
        self.ingredients = []
        self.ingredients_ex = []
        self.recipes = []
        self.last_read_recipe = 0
        self.api_token = ""
        self.api_endpoint = ""

def load_user_data(tracker: Tracker) -> UserData:
    user_id = tracker.sender_id
    user_data = UserData()

    user_db_path = os.path.join(os.curdir,'db','db.pkl') 
    if not os.path.exists(user_db_path):
        return user_data
    with open(user_db_path,"rb") as f:
        db = pickle.load(f)
        if user_id in db.keys():
            user_data = db[user_id]

    # TODO: Remove this:
    print('load:\n', ', '.join("%s: %s" % item for item in vars(user_data).items()))

    return user_data

def save_user_data(user_data: UserData, tracker: Tracker) -> bool:
    # TODO: Remove this:
    print('save:\n', ', '.join("%s: %s" % item for item in vars(user_data).items()))
    
    user_db_path = os.path.join(os.curdir,'db','db.pkl') 
    user_id = tracker.sender_id

    db = {}
    if os.path.exists(user_db_path):
        with open(user_db_path,"rb") as f:
            db = pickle.load(f)
            
    db[user_id] = user_data
    with open(user_db_path,"wb") as f:
        pickle.dump(db,f)
    return True

def search_api(cuisine=None,ingredients=None, ingredients_ex=None) -> list:
    api_key = os.getenv("RECIPE_API_KEY")
    api = sp.API(api_key)

    kwargs={
        'addRecipeInformation': True,
        'type': 'main course',
        'fillIngredients': True,
        'number': '10',
    }

    if cuisine:
        kwargs['cuisine'] = cuisine
    if ingredients:
        ingredients = ','.join(ingredients)
        kwargs['includeIngredients'] = ingredients
    if ingredients_ex:
        ingredients_ex = ','.join(ingredients_ex)
        kwargs['excludeIngredients'] = ingredients_ex

    response = api.search_recipes_complex("", **kwargs)
    data = response.json()
    results = data['results']
    templates = [
        "I got a great recipe for you; {name}. It will take {time} minutes to be ready.",
        "Such a wonderful one; {name}. It will take {time} minutes to be ready.",
        "See what I found; {name}. Takes {time} minutes to cook.",
        "You cannot guess what I found; {name}. It takes {time} minutes to cook.",
        "{name}. Nice one! Takes {time} minutes to cook.",
        "I got a great recipe for you; {name}. It will take {time} minutes to be ready.",
        "Such a wonderful one; {name}. It will take {time} minutes to be ready.",
        "See what I found; {name}. Takes {time} minutes to cook.",
        "You cannot guess what I found; {name}. It takes {time} minutes to cook.",
        "{name}. Nice one! Takes {time} minutes to cook."
    ]
    recipes = []
    for i, recipe in enumerate(results):
        name = recipe["title"]
        time = recipe["readyInMinutes"]
        s = templates[i].format(name=name,time=time)
        url = recipe["spoonacularSourceUrl"]

        recipes.append((s,url))
    random.shuffle(recipes)
    return recipes

def generate_recipe_desctiption(recipe):
    # TODO
    return str(recipe[0])

def send_recipe(recipe, api_token, api_endpoint):
    recipe_text = recipe[0]
    recipe_url = recipe[1]
    text = recipe_text + ": " + recipe_url

    phone_number = get_phone_number(api_token, api_endpoint)
    send_message(text, phone_number)
    print("Recipe Sent to Your Phone!")
    return True

def send_message(text, phone_number):
    sms_api_key = os.getenv("SMS_API_KEY")
    data = {"to": phone_number, "text": text}
    headers = {"Authorization": "basic {}".format(sms_api_key)}
    request_url = "https://gateway.sms77.io/api/sms"

    response = requests.post(request_url, headers = headers, data= data)
    if response.status_code == 200:
        return True
    return False

def get_phone_number(api_token, api_endpoint):
    headers = {'Authorization': 'Bearer {}'.format(api_token)}
    response = requests.get("{}/v2/accounts/~current/settings/Profile.mobileNumber".format(api_endpoint), headers=headers)
    response = response.json()
    phone_number = response["phoneNumber"].replace("-", "").replace(" ", "")
    if not phone_number.startswith("+") and not phone_number.startswith("00"):
        phone_number = response["countryCode"] + phone_number
    if not phone_number.startswith("+"):
        phone_number = "+" + phone_number
    return phone_number


def is_clean_ingredient(ingredient):
    if isinstance(ingredient,list):
        for item in ingredient:
            if is_clean_ingredient(item) == False:
                return False
    else:
        for char in ingredient:
            if not char.isalpha() and char != ' ':
                return False
    return True


# The bellow functions are for generating the list of ingredients and recipes to create the NLU examples
def get_recipes():
    list_of_recipes = []
    cuisine_files = [f for f in os.listdir(os.path.join(
        os.curdir, "datasets", "recipes")) if f.endswith('.json')]
    for cuisine_file in cuisine_files:
        with open(os.path.join(os.curdir, "datasets", "recipes", cuisine_file), "r", encoding="UTF-8") as f:
            recipes = json.load(f)
            for recipe in recipes:
                name = recipe['name']
                ingredients = recipe['ingredients']
                if not is_clean_ingredient(ingredients):
                    continue
                flavors = recipe['flavors'] if recipe['flavors'] is not None \
                    else {
                    "piquant": None,
                    "sour": None,
                    "salty": None,
                    "sweet": None,
                    "bitter": None,
                    "meaty": None
                }
                cuisine = cuisine_file.lower()[:-5]
                courses = recipe['course']

                for course in courses:
                    list_of_recipes.append({
                        "name": name,
                        "igredients": ingredients,
                        "flavors": flavors,
                        "cuisine": cuisine,
                        "course": course
                    })

    return list_of_recipes

def get_cuisines():
    cuisines = []
    with open(os.path.join(
        os.curdir, "datasets", "cuisines.txt")) as file:
        cuisines = file.readlines()
        cuisines = [line.rstrip() for line in cuisines]
    return cuisines

def get_ingredients():
    ingredients = set()
    cuisine_files = [f for f in os.listdir(os.path.join(
        os.curdir, "datasets", "recipes")) if f.endswith('.json')]
    for cuisine_file in cuisine_files:
        with open(os.path.join(os.curdir, "datasets", "recipes", cuisine_file), "r", encoding="UTF-8") as f:
            recipes = json.load(f)
            for recipe in recipes:
                for ingredient in recipe['ingredients']:
                    if not is_clean_ingredient(ingredient):
                        continue
                    ingredients.add(unidecode(ingredient))
    return list(ingredients)
