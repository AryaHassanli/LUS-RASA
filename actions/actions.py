# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted, SlotSet

import http.client
import urllib.parse
import os
import json
import csv
import pickle
from api import search_api, UserData, load_user_data, save_user_data, generate_recipe_desctiption, send_recipe


class ActionCheckDate(Action):
    def name(self) -> Text:
        return "action_check_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_data = load_user_data(tracker)
        msg_cuisine = next(tracker.get_latest_entity_values("cuisine"), None)
        msg_ingredients = [
            ingredient for ingredient in tracker.get_latest_entity_values("ingredient","add")]
        msg_ingredients_ex = [
            ingredient for ingredient in tracker.get_latest_entity_values("ingredient","remove")]
            
        user_data.cuisine = msg_cuisine
        user_data.ingredients = msg_ingredients
        user_data.ingredients_ex = msg_ingredients_ex

        response = "So, you want to cook"
        if user_data.cuisine:
            response += " some {} food".format(user_data.cuisine)
        else:
            response += " some food"

        if len(user_data.ingredients):
            response += " with {}".format(user_data.ingredients[0])
            for ingredient in user_data.ingredients[1:-1]:
                response += ", {}".format(ingredient)
            if user_data.ingredients[-1] != user_data.ingredients[0]:
                response += ", and {}".format(user_data.ingredients[-1])
        
        if len(user_data.ingredients_ex):
            response += ", without {}".format(user_data.ingredients_ex[0])
            for ingredient in user_data.ingredients_ex[1:-1]:
                response += ", {}".format(ingredient)
            if user_data.ingredients_ex[-1] != user_data.ingredients_ex[0]:
                response += ", and {}".format(user_data.ingredients_ex[-1])
                 
        response += "? Am I right?"

        if user_data.cuisine is None and len(user_data.ingredients) == 0 and len(user_data.ingredients) == 0:
            response = "Ok, please let me know what cuisine do you like."
            
        dispatcher.utter_message(response)
        save_user_data(user_data, tracker)
        return []


class ActionSearch(Action):
    def name(self) -> Text:
        return "action_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_data = load_user_data(tracker)
        recipes = search_api(cuisine=user_data.cuisine,
                             ingredients=user_data.ingredients,
                             ingredients_ex=user_data.ingredients_ex)
        user_data.recipes = recipes

        response = generate_recipe_desctiption(user_data.recipes[0])
        user_data.last_read_recipe = 0

        dispatcher.utter_message(response)
        save_user_data(user_data, tracker)
        return []


class ActionNextRecipe(Action):
    def name(self) -> Text:
        return "action_next_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_data = load_user_data(tracker)

        if user_data.last_read_recipe >= len(user_data.recipes) - 1:
            dispatcher.utter_message("I have no more recipes for you")
            return []
        response = "No problem, check this out. "
        response += generate_recipe_desctiption(
            user_data.recipes[
                user_data.last_read_recipe + 1
            ]
        )
        user_data.last_read_recipe += 1

        dispatcher.utter_message(response)
        save_user_data(user_data, tracker)
        return []


class ActionAddRemoveIngredient(Action):
    def name(self) -> Text:
        return "action_add_remove_ingredient"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_data = load_user_data(tracker)

        ingredients_to_add = [
            ingredient for ingredient in tracker.get_latest_entity_values("ingredient","add")]

        ingredients_to_remove = [
            ingredient for ingredient in tracker.get_latest_entity_values("ingredient","remove")]

        print("Action Add Remove Ingredient: \n","add:\t",ingredients_to_add,"\nremove\t",ingredients_to_remove)

        for ingredient in ingredients_to_add:
            if ingredient not in user_data.ingredients:
                user_data.ingredients.append(ingredient)
            if ingredient in user_data.ingredients_ex:
                user_data.ingredients_ex.remove(ingredient)

        for ingredient in ingredients_to_remove:
            if ingredient not in user_data.ingredients_ex:
                user_data.ingredients_ex.append(ingredient)
            if ingredient in user_data.ingredients:
                user_data.ingredients.remove(ingredient)

        response = "I got it. you want"
        if user_data.cuisine:
            response += " a {} food".format(user_data.cuisine)
        else:
            response += " a food"

        if len(user_data.ingredients):
            response += " with {}".format(user_data.ingredients[0])
            for ingredient in user_data.ingredients[1:-1]:
                response += ", {}".format(ingredient)
            if user_data.ingredients[-1] != user_data.ingredients[0]:
                response += ", and {}".format(user_data.ingredients[-1])

        if len(user_data.ingredients_ex):
            response += ", without {}".format(user_data.ingredients_ex[0])
            for ingredient in user_data.ingredients_ex[1:-1]:
                response += ", {}".format(ingredient)
            if user_data.ingredients_ex[-1] != user_data.ingredients_ex[0]:
                response += ", and {}".format(user_data.ingredients_ex[-1])
                
        response += "? uhum?"

        dispatcher.utter_message(response)
        save_user_data(user_data, tracker)
        return []


class ActionSendRecipe(Action):
    def name(self) -> Text:
        return "action_send_recipe"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_data = load_user_data(tracker)
        recipe = user_data.recipes[
            user_data.last_read_recipe
        ]
        send_recipe(recipe, tracker)
        dispatcher.utter_message("Nice! I sent the detailed description to your phone.")
        return []
