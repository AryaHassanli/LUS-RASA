# Language Understanding Systems - RASA Powered Recipe Recommender: Be My Chef

## Requirements

1. Install [RASA](https://rasa.com/docs/rasa/installation/)
2. Install python library [spoonacular api](https://pypi.org/project/spoonacular/)
3. Download and Install [ngrok](https://ngrok.com/download)
4. Set the following environmental variables:
    1. Spoonacular api key: Spoonacular used for searching the recipes. Create an account and generate the key from [here](https://spoonacular.com/food-api). Then set the RECIPE_API_KEY to the generated api key.
    2. SMS77 api key: SMS77 api is used for sending the final sms to the user. Create an account and generate the api key from [here](https://www.sms77.io). Then set the SMS_API_KEY to your api key.

## Usage
1. Open a terminal and run `rasa`: 
    ```bash
    $ rasa run
    ```
    This will load the last model available in `models`.

2. Open a new terminal and run action server to handle the custom actions:
    ```bash
    $ rasa run actions
    ```

3. Create the Alexa skill using the instruction given in [LUS repo.](https://github.com/esrel/LUS/blob/master/notebooks/rasa_alexa.ipynb)

4. Run ngrok, so that Alexa can connect to your localhost:
    ```bash
    $ ngrok http 5005
    ```

5. The output of ngrok after running would be something like this:
    ```bash
    ngrok by @inconshreveable
    (Ctrl+C to quit)
    Session Status                online
    Account                       Arya (Plan: Free)
    Version                       2.3.40
    Region                        United States (us)
    Web Interface                 http://127.0.0.1:4040
    Forwarding                    http://***********.ngrok.io -> http://localhost:5005
    Forwarding                    https://***********.ngrok.io -> http://localhost:5005              
    ```

    Copy the given https address following by `/webhooks/alexa_assistant/webhook` in Alexa Console -> Endpoint

6. Now you can test your skill

## Samples

### Say Hi
- Hello my chef
- Good morning

### Ask for an Introduction
- What can you do?
- What's your skill?

### Challenge it!
- Are you a robot?
- Are you a real chef?

### Ask them to suggest you some food
- I want to cook some Italian food for lunch.
- Give me recipe with tomatoes and potatoes.
- What can I cook for dinner with tomatoes and mushrooms? Also I don't like peppers.

## Resources

* [RASA docs](https://rasa.com/docs/)
* [esrel/LUS](https://github.com/esrel/LUS)
* [giTorto/rasa-restaurantbot](https://github.com/giTorto/rasa-restaurantbot)
* [Manikandan-Raj/ticketbooking](https://github.com/Manikandan-Raj/ticketbooking)
* [sousablde/MoviCHTR-with-Rasa](https://github.com/sousablde/MoviCHTR-with-Rasa)