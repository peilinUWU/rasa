import os
import random
import pandas as pd
import requests
import csv
import string

import spacy
nlp = spacy.load("en_core_web_md")

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk.forms import FormAction
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    ActionExecuted,
    UserUttered,
    FollowupAction
)

##from threading import Thread
##global api_data
##api_data = []

        

##class ActionEntityTest(Action):
##    def name(self) -> Text:
##        return "action_entity_test"
##
##    def run(self, dispatcher, tracker, domain):
##
##        ent = tracker.latest_message['entities'][0]['entity']
##        dispatcher.utter_message("Rasa got entity: " + str(ent)) 
##
##        return []



# ----------------------------------------------------
#
# Check if the user is previously greeted,
#   - If yes, call API
#   - If not, request email address to continue
#
# ----------------------------------------------------
class ActionGreet(Action):
    
    def name(self) -> Text:
        return "action_greet"


    def run(self, dispatcher, tracker, domain):
        # Check if we greeted the user
        greeted = tracker.get_slot("greeted")

        if not greeted:
            # Set the greeted slot to True
            # Go to a chit chat action form to ask 5 specific questions
            return[
                SlotSet("greeted", True),
                FollowupAction("request_email")
                ]
        else:
            return [FollowupAction("action_get_answer")]
        

    
# ----------------------------------------------------
#
# Get the user's email and store it for
# identification purpose
#
# ----------------------------------------------------
class RequestEmail(FormAction):
    
    def name(self) -> Text:
        return "request_email"


    @staticmethod
    def required_slots(tracker) -> List[Text]:   
        return ["email"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "email": [
                self.from_entity(entity="email"),
                self.from_text(intent="enter_data"),
                self.from_text(),
            ]
        }


    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        # Create the csv file if it's not there              
        if not os.path.isfile('df2.csv'):
            df = pd.DataFrame(columns = ['user', 'name', 'sport', 'animal'])  
            df.to_csv('df2.csv', index=False, header='columns')

        return[FollowupAction("action_take_path")]
            


# ----------------------------------------------------
#
# Check if the email exists in the databse,
#   - if yes, this is the first encounter
#   - if no, this is the second encounter
#
# ----------------------------------------------------
class ActionTakePath(Action):
    
    def name(self) -> Text:
        return "action_take_path"


    def run(self, dispatcher, tracker, domain):
        # Retrive the email address from the slot
        email = tracker.get_slot("email")

        # Read the csv file, the first column is the email address and has heading "user"
        user_list = pd.read_csv('df2.csv', usecols=[0])
        user_list = user_list.user.tolist()
        
        # Decide on follow up action accordingly
        if email not in user_list:
            dispatcher.utter_message("Hi! What's your name?")
            return []
        else:          
            return [FollowupAction("action_fetch_from_db")]



# ----------------------------------------------------
#
# Custom extraction for name entity
#
# ----------------------------------------------------
class ActionSetName(Action):
    
    def name(self):
        return "action_set_name"

    def run(self, dispatcher, tracker, domain):
        # Take the user's message
        input_txt = tracker.latest_message.get("text")
        input_str = str(input_txt).lower()

        # Pre process the text
        punc_test = input_str[-1]
        if punc_test not in string.punctuation:
            input_str = input_str + "."
                
        dispatcher.utter_message("Cool!")
        
        tokens = nlp(input_str)

        # If name is successfully extracted
        if len(tokens.ents) == 1:
            dispatcher.utter_message("Name entity found! (to remove)")
            extracted_ent = str(tokens.ents[0])
            return [SlotSet("PERSON", extracted_ent),
                    FollowupAction("action_process_name")] 
        else:
            dispatcher.utter_message("Failed to extract name entity! (to remove)")
            return [SlotSet("PERSON", "zero"),
                    FollowupAction("action_process_name")] 





# ----------------------------------------------------
#
# Process, and call API if user asks back
#
# ----------------------------------------------------
class ActionProcessName(Action):
    
    def name(self):
        return "action_process_name"
    

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent'].get('name')

        if intent == "chit_chat_question":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')

            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))

        return [FollowupAction("request_fav_sport")]



# ----------------------------------------------------
#
# Ask user for favorite sport
#   
# ----------------------------------------------------
class RequestFavSport(FormAction):
    
    def name(self) -> Text:
        return "request_fav_sport"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["type_of_sport"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "type_of_sport": [
                self.from_entity(entity="sport"),
                self.from_text(),
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        userID = tracker.get_slot("email")
            
        # If entity extraction failed, set it manually to a placeholder
        result = tracker.get_slot("type_of_sport")
        data = tracker.latest_message.get('text')

        if result == data:            
            response = call_api_self_disclosure(userID, data, "sport")
            dispatcher.utter_message(str(response))
            return [SlotSet("type_of_sport", "fail"),
                    FollowupAction("request_fav_sport_reason")]
        
        # If the user doesn't have a favorite sport
        # continue to topic about animal
        intent = tracker.latest_message['intent'].get('name')
        
        if intent == "deny" or intent == "user.reject":
            return [SlotSet("type_of_sport", "zero"),
                    FollowupAction("request_fav_animal")]
        else:
            topic = tracker.latest_message['entities'][0]['entity']
            response = call_api_self_disclosure(userID, data, topic)
            dispatcher.utter_message(str(response))
                
            return []



# ----------------------------------------------------
#
# Choose actions depending on if user acknowledge
# or/and asked a question
#   - if only acknowledge, continue to next action
#   - if contains question, calls API before continuing 
#   
# ----------------------------------------------------
class ActionAddOn1(Action):
    
    def name(self) -> Text:
        return "action_add_on_1"


    def run(self, dispatcher, tracker, domain): # -> List[EventType]:
        # Get the latest message's intent
        intent = tracker.latest_message['intent'].get('name')

        # If the message has more than acknowledge
        if intent == "chit_chat_question":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')

            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))

        return [FollowupAction("request_fav_sport_reason")]



# ----------------------------------------------------
#
# Ask user what they like about the subject
#   
# ----------------------------------------------------
class RequestFavSportReason(FormAction):
    
    def name(self) -> Text:
        return "request_fav_sport_reason"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["reason_of_like_sport"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "reason_of_like_sport": [
                self.from_text()
                ],
            }              


    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:   
        intent = tracker.latest_message['intent'].get('name')
        
        if intent == "chit_chat_question":            
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')

            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))
        else:
            dispatcher.utter_message("Okay.")

        return [FollowupAction("request_fav_animal")]



# ----------------------------------------------------
#
# Ask user for details about animal
#
# ----------------------------------------------------
class RequestFavAnimal(FormAction):
    
    def name(self) -> Text:
        return "request_fav_animal"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["type_of_animal"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {                
                "type_of_animal": [
                    self.from_entity(entity="animal"),
                    self.from_text(),
                    ],
                }


    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:       
        userID = tracker.get_slot("email")

        # If entity extraction failed, set it manually to a placeholder
        result = tracker.get_slot("type_of_animal")
        data = tracker.latest_message.get('text')
        
        if result == data:            
            response = call_api_self_disclosure(userID, data, "animal")
            dispatcher.utter_message(str(response))
            return [SlotSet("type_of_animal", "fail"),
                    FollowupAction("action_store_detail")]

        # If the user doesn't have a favorite sport
        # end the survey
        intent = tracker.latest_message['intent'].get('name')
        
        if intent == "deny" or intent == "user.reject":
            return [SlotSet("type_of_animal", "zero"),
                    FollowupAction("action_store_detail")]
        else:
            topic = tracker.latest_message['entities'][0]['entity']
            response = call_api_self_disclosure(userID, data, topic)
            dispatcher.utter_message(str(response))

            return []



# ----------------------------------------------------
#
# Choose actions depending on if user acknowledge
# or/and asked a question
#   - if only acknowledge, continue to next action
#   - if contains question, calls API before continuing 
#   
# ----------------------------------------------------
class ActionAddOn2(Action):
    
    def name(self) -> Text:
        return "action_add_on_2"


    def run(self, dispatcher, tracker, domain): # -> List[EventType]:
        intent = tracker.latest_message['intent'].get('name')

        if intent == "chit_chat_question":            
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')

            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))        

        return [FollowupAction("action_store_detail")]


    
# ----------------------------------------------------
#
# Storing details to csv
#
# ----------------------------------------------------
class ActionStoreDetail(Action):
    
    def name(self) -> Text:
        return "action_store_detail"

    def run(self, dispatcher, tracker, domain): # -> List[EventType]:                
        user   = tracker.get_slot("email")
        name   = tracker.get_slot("PERSON")
        sport  = tracker.get_slot("type_of_sport")
        animal = tracker.get_slot("type_of_animal")

        dispatcher.utter_message("storing details (remove)")
        dispatcher.utter_message("user: " + str(user))
        dispatcher.utter_message("name: " + str(name))
        dispatcher.utter_message("sport: " + str(sport))
        dispatcher.utter_message("animal: " + str(animal))

        if sport == "zero" and animal == "zero":
            dispatcher.utter_message("So it seems that you dislike topics related sport and animal, that's okay.")
            
        
        Data = { 'user'  : [str(user)],
                 'name'  : [str(name)],
                 'sport' : [str(sport)],
                 'animal': [str(animal)],
               }
        
        # Store relevant data to a csv file
        df = pd.DataFrame(Data, columns = ['user', 'name', 'sport', 'animal'])  
        df.to_csv('df2.csv', index=False, mode='a', header=False)

        # Clear the following slots
        return [SlotSet("type_of_sport", None),
                SlotSet("reason_of_like_sport", None),
                SlotSet("type_of_animal", None),              
                FollowupAction("action_end_session_1")]



# ----------------------------------------------------
#
# Fetch stored data from csv
#
# ----------------------------------------------------
class ActionFetchFromDB(Action):
    
    def name(self) -> Text:
        return "action_fetch_from_db"

    def run(self, dispatcher, tracker, domain): # -> List[EventType]:        
        # Define column headers     
        col_list = ['user', 'name', 'sport', 'animal']
            
        # Read the csv file
        dispatcher.utter_message("Reading csv")
        df = pd.read_csv("df2.csv", usecols=col_list)
        dispatcher.utter_message("Done reading csv")

        # Extract the 'user' column and turn it into a list
        
        dispatcher.utter_message("Getting user index")
        user_list = df["user"]
        user_list = user_list.tolist()


        # Get the user's index
        user = tracker.get_slot("email")
        index = user_list.index(user)
        dispatcher.utter_message("Done getting user index: " + str(index))

        # Get the user's topic and recent activity bool          
        user_name   = df["name"][index]  
        user_sport  = df["sport"][index]
        user_animal = df["animal"][index]

        dispatcher.utter_message("name: " + str(user_name) )
        dispatcher.utter_message("sport: " + str(user_sport))
        dispatcher.utter_message("animal: " + str(user_animal))

        
        return [SlotSet("PERSON", str(user_name)),
                SlotSet("type_of_sport", str(user_sport)),
                SlotSet("type_of_animal", str(user_animal)),
                FollowupAction("ask_how_are")]


    
# ----------------------------------------------------
#
# Actions for second encounter, starting with
# asking for how user are
#
# ----------------------------------------------------
class AskHowAre(FormAction):
    
    def name(self) -> Text:
        return "ask_how_are"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        user_name = tracker.get_slot("PERSON")
        if user_name == "zero":
            return ["how_are_no_name"]
        else:
            return ["how_are"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {            
            "how_are": [                
                self.from_text(),                
                ],        
            "how_are_no_name": [                
                self.from_text(),                
                ],        
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        intent = tracker.latest_message['intent'].get('name')

        if intent == "chit_chat_question" or intent == "chit_chat":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')
            
            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))

        sport  = tracker.get_slot("type_of_sport")
        animal = tracker.get_slot("type_of_animal")
        
        if sport == "fail":
            return [FollowupAction("request_fav_sport_again")]
        elif sport == "zero" and animal == "zero":
            dispatcher.utter_message("Well, it seems that we didn't have a chance to talk about anything.")
            return [FollowupAction("action_end_session_2")]
        elif sport == "zero":
            return [FollowupAction("request_own_pet")]
        else:
            return [FollowupAction("request_recent_sport")]




# ----------------------------------------------------
#
# Ask user for favorite sport again
#   
# ----------------------------------------------------
class RequestFavSportAgain(FormAction):
    
    def name(self) -> Text:
        return "request_fav_sport_again"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["type_of_sport_2"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "type_of_sport_2": [
                self.from_text(),
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        return [FollowupAction("request_recent_sport")]
        


    
# ----------------------------------------------------
#
# Long term question, ask if user did their
# favorite sport recently
#
# ----------------------------------------------------
class RequestRecentSport(FormAction):
    
    def name(self) -> Text:
        return "request_recent_sport"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["recent_active_sport"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "recent_active_sport": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
                self.from_text(),
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        # If entity extraction failed, set it manually to a placeholder
        result = tracker.get_slot("recent_active_sport")
        data = tracker.latest_message.get('text')
        
        if result == data:            
            return [FollowupAction("add_on_3")]

        # Get the latest message's intent
        intent = tracker.latest_message['intent'].get('name')

        # If the message has more than acknowledge
        if intent == "chit_chat_question":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')

            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))

        return [FollowupAction("follow_up_recent_sport")]


    

# ----------------------------------------------------
#
# Follow up question, ask if user questions depending
# on the previous answer
#
# ----------------------------------------------------
class FollwUpRecentSport(FormAction):
    
    def name(self) -> Text:        
        return "follow_up_recent_sport"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        recent_active = tracker.get_slot("recent_active_sport")

        if recent_active == True:
            return ["how_go_sport"]
        else:
            return ["play_in_future"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "how_go_sport": [
                self.from_text(),
                ],
            "play_in_future": [
                self.from_text(),
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        intent = tracker.latest_message['intent'].get('name')

        if intent == "chit_chat_question":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')

            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))
        
        animal = tracker.get_slot("type_of_animal")
        
        if animal == "zero":
            return [FollowupAction("action_end_session_2")]
        elif animal == "fail":
            return [FollowupAction("request_fav_animal_again")]
        else:
            return [FollowupAction("add_on_3")]
        



# ----------------------------------------------------
#
# Ask user for details about animal again
#
# ----------------------------------------------------
class RequestFavAnimalAgain(FormAction):
    
    def name(self) -> Text:
        return "request_fav_animal_again"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["type_of_animal_2"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {                
                "type_of_animal_2": [
                    self.from_text(),
                    ],
                }


    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:       
        return [FollowupAction("request_own_pet")]

        


# ----------------------------------------------------
#
# Leave room for user to ask question
#
# ----------------------------------------------------
class AddOn3(FormAction):
    
    def name(self) -> Text:
        return "add_on_3"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["add_on_3"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "add_on_3": [                
                self.from_text(),
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        # Get the latest message's intent
        intent = tracker.latest_message['intent'].get('name')

        # If the message has more than acknowledge
        if intent != "affirm":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')

            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))

        return [FollowupAction("request_own_pet")]



    
# ----------------------------------------------------
#
# Long term question, ask if user own pet
#
# ----------------------------------------------------
class RequestOwnPet(FormAction):
    
    def name(self) -> Text:
        return "request_own_pet"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["own_animal"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "own_animal": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
                self.from_text(),
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        # If entity extraction failed, set it manually to a placeholder
        result = tracker.get_slot("recent_active_sport")
        data = tracker.latest_message.get('text')
        
        if result == data:            
            return [FollowupAction("add_on_4")]

        # Get the latest message's intent
        intent = tracker.latest_message['intent'].get('name')

        # If the message has more than acknowledge
        if intent == "chit_chat_question":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')

            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))

        return [FollowupAction("follow_up_own_pet")]



# ----------------------------------------------------
#
# Follow up question, ask if user questions depending
# on the previous answer
#
# ----------------------------------------------------
class FollwUpOwnPet(FormAction):
    
    def name(self) -> Text:        
        return "follow_up_own_pet"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        own_animal = tracker.get_slot("own_animal")

        if own_animal == True:
            return ["animal_color"]
        else:
            return ["plan_to_own_animal"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "animal_color": [
                self.from_text(),
                ],
            "plan_to_own_animal": [
                self.from_text(),
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        # Get the latest message's intent
        intent = tracker.latest_message['intent'].get('name')

        # If the message has more than acknowledge
        if intent == "chit_chat_question":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')

            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))
                
        return [FollowupAction("add_on_4")]



# ----------------------------------------------------
#
# Leave room for user to ask question
#
# ----------------------------------------------------
class AddOn3(FormAction):
    
    def name(self) -> Text:
        return "add_on_4"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["add_on_4"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "add_on_4": [                
                self.from_text(),
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        # Get the latest message's intent
        intent = tracker.latest_message['intent'].get('name')

        # If the message has more than acknowledge
        if intent != "affirm":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')

            response = call_api_question(userID, data)
            dispatcher.utter_message(str(response))

        return [FollowupAction("action_end_session_2")]







# ----------------------------------------------------
#
# Custom action for ending conversations
#
# ----------------------------------------------------
class ActionEndSession1(Action):
    
    def name(self) -> Text:
        return "action_end_session_1"


    def run(self, dispatcher, tracker, domain):
        user_name = tracker.get_slot("PERSON")
        if user_name == "zero":
            dispatcher.utter_message(template="utter_end_session_1_no_name")
        else:
            dispatcher.utter_message(template="utter_end_session_1")
            
        return [SlotSet("email", None),
                SlotSet("PERSON", None),
                FollowupAction('action_listen')]



class ActionEndSession2(Action):
    
    def name(self) -> Text:
        return "action_end_session_2"


    def run(self, dispatcher, tracker, domain):        
        dispatcher.utter_message("Great, it was nice talking to you!")
        user_name = tracker.get_slot("PERSON")
        if user_name == "zero":
            dispatcher.utter_message(template="utter_end_session_2_no_name")
        else:
            dispatcher.utter_message(template="utter_end_session_2")
            
        return [FollowupAction('action_listen')]



# ----------------------------------------------------
# A self disclosure component that is used after
# asking the opening question
# ----------------------------------------------------
class ActionSelfDisclosure(Action):
    
    def name(self) -> Text:
        return "action_self_disclosure"


    def run(self, dispatcher, tracker, domain): # -> List[EventType]:
        userID = tracker.get_slot("email")
        data = tracker.latest_message.get('text')
        topic = tracker.latest_message['entities'][0]['entity']

        response = call_api_self_disclosure(userID, data, topic)
        dispatcher.utter_message(str(response))
    
        return []

    

# ----------------------------------------------------
#
# A self disclosure component that is used after
# asking the opening question
#
# ----------------------------------------------------
class ActionGetAnswer(Action):
    
    def name(self) -> Text:
        return "action_get_answer"


    def run(self, dispatcher, tracker, domain): # -> List[EventType]:         
        userID = tracker.get_slot("email")
        data = tracker.latest_message.get('text')

        response = call_api_question(userID, data)
        dispatcher.utter_message(str(response))
        
##        Thread(target=call_api_question, args=(userID, data, dispatcher)).start()        

        return []



# ----------------------------------------------------
#
# Call API functions
#
# ----------------------------------------------------
def call_api_question(userID, data):
    
    r = requests.post('http://f8298a7a6831.ngrok.io/get_answer', json={"userID": userID, "data": data})
    if r.json()["error"] == None:
        response = r.json()["answer"]
        return response
    else:
        response = "Something went wrong when calling the API."
        return response



def call_api_self_disclosure(userID, data, topic):
        
    r = requests.post('http://f8298a7a6831.ngrok.io/get_disclosure', json={"userID": userID, "data": data, "topic": topic})
    if r.json()["error"] == None:
        response = r.json()["answer"]
        return response
    else:
        response = "Something went wrong when calling the API."
        return response
