import os
import random
import pandas as pd
import requests
import csv
import datetime

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
    FollowupAction,
    ReminderScheduled
)

        

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
            return [FollowupAction("ask_name")]
        else:          
            return [FollowupAction("action_fetch_from_db")]



# ----------------------------------------------------
#
# Actions for first encounter, starting with
# asking for user's name
#
# ----------------------------------------------------
class AskName(FormAction):
    
    def name(self) -> Text:
        return "ask_name"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["name"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {          
            "name": [
                self.from_entity(entity="PERSON"),
                self.from_text(),
                ],     
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:

        # Calls API and reply a name to user
        userID = tracker.get_slot("email")
        data = tracker.latest_message.get('text')
        r = requests.post('https://546c412d1867.ngrok.io/get_answer',
                          json={"userID": str(userID), "data": str(data)} )

        if r.json()["error"] == None:            
            response = r.json()["answer"]
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
                self.from_entity(entity="sport")
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        # Calls API and reveal something about the subject
        userID = tracker.get_slot("email")
        data = tracker.latest_message.get('text')
        topic = tracker.latest_message['entities'][0]['entity']
        r = requests.post("https://546c412d1867.ngrok.io/get_disclosure",
                          json={"userID": str(userID), "data": str(data), "topic": str(topic)} )

        # Test thread number
        #print(threading.current_thread().name)

        if r.json()["error"] == None:
            response = r.json()["answer"]
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
        if intent != "affirm":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')
            r = requests.post('https://546c412d1867.ngrok.io/get_answer',
                              json={"userID": str(userID), "data": str(data)} )

            if r.json()["error"] == None:
                response = r.json()["answer"]
                dispatcher.utter_message(str(response))

        return [FollowupAction("request_sport_detail_2")]





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
        # If user reply with a question, calls API before continuing
        intent = tracker.latest_message['intent'].get('name')
        
        if intent == "chit_chat_question" or "chit_chat":            
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')
            r = requests.post('https://546c412d1867.ngrok.io/get_answer',
                              json={"userID": str(userID), "data": str(data)} )

            if r.json()["error"] == None:
                response = r.json()["answer"]
                dispatcher.utter_message(str(response))

        return [FollowupAction("request_fav_animal")]





# ----------------------------------------------------
# Ask user for details about animal
#
# ----------------------------------------------------
class RequestFavAnimal(FormAction):
    
    def name(self) -> Text:
        return "request_fav_animal"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["type_of_animal"]
##        return ["type_of_animal", "own_animal"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {                
                "type_of_animal": [
                    self.from_entity(entity="animal"),
                    ],
##                "own_animal": [
##                    self.from_intent(intent="affirm", value=True),
##                    self.from_intent(intent="deny", value=False),
##                    ],
                }


    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:       
        # Calls API and reveal something about the subject
        userID = tracker.get_slot("email")
        data = tracker.latest_message.get('text')
        topic = tracker.latest_message['entities'][0]['entity']
        r = requests.post("https://546c412d1867.ngrok.io/get_disclosure",
                          json={"userID": str(userID), "data": str(data), "topic": str(topic)} )

        # Test thread number
        #print(threading.current_thread().name)

        if r.json()["error"] == None:
            response = r.json()["answer"]
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
        # Get the latest message's intent
        intent = tracker.latest_message['intent'].get('name')

        # If the message has more than acknowledge
        if intent != "affirm":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')
            r = requests.post('https://546c412d1867.ngrok.io/get_answer',
                              json={"userID": str(userID), "data": str(data)} )

            if r.json()["error"] == None:
                response = r.json()["answer"]
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
        name   = tracker.get_slot("name")
        sport  = tracker.get_slot("type_of_sport")
        animal = tracker.get_slot("type_of_animal")
        
        Data = { 'user'  : [user],
                 'name'  : [name],
                 'sport' : [sport],
                 'animal': [animal],
               }
        
        # Store relevant data to a csv file
        df = pd.DataFrame(Data, columns = ['user', 'name', 'sport', 'animal'])  
        df.to_csv('df2.csv', index=False, mode='a', header=False)

        # Clear the following slots
        return [SlotSet("type_of_sport", None),
                SlotSet("reason_of_like_sport", None),
                SlotSet("recent_active_sport", None),
                SlotSet("type_of_animal", None),
                SlotSet("own_animal", None),
                SlotSet("animal_breed", None),
                SlotSet("plan_to_own_animal", None),                
                FollowupAction("action_end_session_1"),
                ]



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
        df = pd.read_csv("df2.csv", usecols=col_list)

        # Extract the 'user' column and turn it into a list
        user_list = df["user"]
        user_list = user_list.tolist()

        # Get the user's index
        user = tracker.get_slot("email")
        index = user_list.index(user)

        # Get the user's topic and recent activity bool          
        user_name   = df["name"][index]  
        user_sport  = df["sport"][index]
        user_animal = df["animal"][index]         

        
        return [SlotSet("name", user_name),
                SlotSet("type_of_sport", user_sport),
                SlotSet("type_of_animal", user_animal),
                FollowupAction("ask_how_are"),
                ]


    
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
        return ["how_are"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {            
            "how_are": [                
                self.from_text(),                
                ],        
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:

        # Calls API and reply a name to user
        userID = tracker.get_slot("email")
        data = tracker.latest_message.get('text')
        r = requests.post('https://546c412d1867.ngrok.io/get_answer',
                          json={"userID": str(userID), "data": str(data)} )

        if r.json()["error"] == None:            
            response = r.json()["answer"]
            dispatcher.utter_message(str(response))

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
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        # Get the latest message's intent
        intent = tracker.latest_message['intent'].get('name')

        # If the message has more than acknowledge
        if intent == "chit_chat_question":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')
            r = requests.post('https://546c412d1867.ngrok.io/get_answer',
                              json={"userID": str(userID), "data": str(data)} )

            if r.json()["error"] == None:
                response = r.json()["answer"]
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
        # Get the latest message's intent
        intent = tracker.latest_message['intent'].get('name')

        # If the message has more than acknowledge
        if intent == "chit_chat_question":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')
            r = requests.post('https://546c412d1867.ngrok.io/get_answer',
                              json={"userID": str(userID), "data": str(data)} )

            if r.json()["error"] == None:
                response = r.json()["answer"]
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
                ],
            }
    

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        # Get the latest message's intent
        intent = tracker.latest_message['intent'].get('name')

        # If the message has more than acknowledge
        if intent == "chit_chat_question":
            userID = tracker.get_slot("email")
            data = tracker.latest_message.get('text')
            r = requests.post('https://546c412d1867.ngrok.io/get_answer',
                              json={"userID": str(userID), "data": str(data)} )

            if r.json()["error"] == None:
                response = r.json()["answer"]
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
            r = requests.post('https://546c412d1867.ngrok.io/get_answer',
                              json={"userID": str(userID), "data": str(data)} )

            if r.json()["error"] == None:
                response = r.json()["answer"]
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
        dispatcher.utter_message("Thank you! You have now finished the first session, please proceed to the form for a small survey then come back to restart the session.")
        return []


class ActionEndSession2(Action):
    
    def name(self) -> Text:
        return "action_end_session_2"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Great, it was nice talking to you!")
        dispatcher.utter_message("Thank you! Please proceed to the form to answer a few questions to complete the test.")
        return []



# ----------------------------------------------------
# A self disclosure component that is used after
# asking the opening question
# ----------------------------------------------------
class ActionSelfDisclosure(Action):
    def name(self) -> Text:
        return "action_self_disclosure"

    def run(self, dispatcher, tracker, domain): # -> List[EventType]:

        # Get the user
        userID = tracker.get_slot("email")

        # Get the user's input
        data = tracker.latest_message.get('text')

        # Get the entity
        topic = tracker.latest_message['entities'][0]['entity']

        # API call
        r = requests.post("https://546c412d1867.ngrok.io/get_disclosure",
                          json={"userID": str(userID), "data": str(data), "topic": str(topic)} )

        # Test thread number
        #print(threading.current_thread().name)

        if r.json()["error"] == None:
            response = r.json()["answer"]
            dispatcher.utter_message(str(response))
        #else:
            #Ask new question instead because unexpected error occurred

        return []

    

# ----------------------------------------------------
# A self disclosure component that is used after
# asking the opening question
# ----------------------------------------------------
class ActionGetAnswer(Action):
    def name(self) -> Text:
        return "action_get_answer"

    def run(self, dispatcher, tracker, domain): # -> List[EventType]:         

        # Get the user
        userID = tracker.get_slot("email")

        # Get the user's input
        data = tracker.latest_message.get('text')

        # API call
        r = requests.post('https://546c412d1867.ngrok.io/get_answer',
                          json={"userID": str(userID), "data": str(data)} )


        if r.json()["error"] == None:
            response = r.json()["answer"]
            dispatcher.utter_message(str(response))
        else:
            dispatcher.utter_message("Something went wrong")
            #Ask new question instead because unexpected error occurred

        return []
