import os
import random
import pandas as pd
import requests
import csv

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
# Check if the user is previously greeted,
# if not, we will ask 5 questions
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
# Get the user's email for identification purpose
# ----------------------------------------------------
class RequestEmail(FormAction):
    """Asks for the user's email, and store it into a slot. Note at this point the email is not yet recorded to the database"""

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
        if not os.path.isfile('df.csv'):
            df = pd.DataFrame(columns = ['user', 'sport', 'recent_active', 'animal', 'own'])  
            df.to_csv('df.csv', index=False, header='columns')


        # Proceed to next step: check if user exists        
##        dispatcher.utter_message("(Email received, proceeding to the next step...)")
        dispatcher.utter_message("Welcome!")
        return[FollowupAction("action_take_path")]
            
         

# ----------------------------------------------------
# Check if the email exists in the databse, and
# choose different actions accordingly
# ----------------------------------------------------
class ActionTakePath(Action):
    def name(self) -> Text:
        return "action_take_path"


    def run(self, dispatcher, tracker, domain):
        # Retrive the email address from the slot
        email = tracker.get_slot("email")

        # Read the csv file, the first column is the email address and has heading "user"
        user_list = pd.read_csv('df.csv', usecols=[0])
        user_list = user_list.user.tolist()

        # Decide on follow up action accordingly
        if email not in user_list:
           
##            dispatcher.utter_message("(User is not found in the databse, requesting more details...)")
            return [FollowupAction("chit_chat_1")]
        else:          
##            dispatcher.utter_message("(User found in database...)")
            return [FollowupAction("chit_chat_second")]

        
        
# ----------------------------------------------------
# Chit chat questions for first session
#
# ----------------------------------------------------
class ChitChat1(FormAction):   
    def name(self) -> Text:
        return "chit_chat_1"


##    def run(self, dispatcher, tracker, domain):
##        dispatcher.utter_message(template=f"utter_ask_how_are")
##        return[]

    @staticmethod
    def required_slots(tracker) -> List[Text]:   
        return ["name"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {            
            "name": [
                self.from_entity(entity="PERSON"),
                self.from_text(),
                ],            
##            "how_are": [                
##                self.from_text(),                
##                ],            
##            "where_from": [
##                self.from_text(),
##                ],
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:

        # Get the latest message's intent
        intent = intent = tracker.latest_message['intent'].get('name')

        # If the message is not a question,
        # then proceed to the next step
        if intent == "chit_chat_question":
            # Get the user
            userID = tracker.get_slot("email")

            # Get the user's input
            data = tracker.latest_message.get('text')

            # API call
            r = requests.post('https://aebfc2ed232f.ngrok.io/get_answer',
                              json={"userID": str(userID), "data": str(data)} )

            if r.json()["error"] == None:
                response = r.json()["answer"]
                dispatcher.utter_message(str(response))
            #else:
                #Ask new question instead because unexpected error occurred

        return [FollowupAction("request_sport_detail")]



# ----------------------------------------------------
# Ask user for details related to sport
#   
# ----------------------------------------------------
class RequestSportDetail(FormAction):
    def name(self) -> Text:
        return "request_sport_detail"


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

        # Run self disclosure module (maybe make a class for easier call)
        
        # Get the user
        userID = tracker.get_slot("email")

        # Get the user's input
        data = tracker.latest_message.get('text')

        # Get the entity
        topic = tracker.latest_message['entities'][0]['entity']

        # API call
        r = requests.post("https://aebfc2ed232f.ngrok.io/get_disclosure",
                          json={"userID": str(userID), "data": str(data), "topic": str(topic)} )

        # Test thread number
        #print(threading.current_thread().name)

        if r.json()["error"] == None:
            response = r.json()["answer"]
            dispatcher.utter_message(str(response))

            
        return [FollowupAction("action_optional_get_answer")]
        #return [FollowupAction("action_self_disclosure")]



# ----------------------------------------------------
# A self disclosure component that is used after
# asking the opening question
# ----------------------------------------------------
class ActionOptionalGetAnswer(Action):
    def name(self) -> Text:
        return "action_optional_get_answer"

    def run(self, dispatcher, tracker, domain): # -> List[EventType]:

        # Get the latest message's intent
        intent = intent = tracker.latest_message['intent'].get('name')

        # If the message is not a question,
        # then proceed to the next step
        if intent == "affirm":
            return [FollowupAction("request_more_sport_detail")]
        # If the message is a question,
        # then call the API before proceeding to the next step
        else:
            # Get the user
            userID = tracker.get_slot("email")

            # Get the user's input
            data = tracker.latest_message.get('text')

            # API call
            r = requests.post('https://aebfc2ed232f.ngrok.io/get_answer',
                              json={"userID": str(userID), "data": str(data)} )


            if r.json()["error"] == None:
                response = r.json()["answer"]
                dispatcher.utter_message(str(response))
            #else:
                #Ask new question instead because unexpected error occurred

            return [FollowupAction("request_more_sport_detail")]



# ----------------------------------------------------
# Ask user for more details related to sport
#   
# ----------------------------------------------------
class RequestMoreSportDetail(FormAction):
    def name(self) -> Text:
        return "request_more_sport_detail"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["reason_of_like_sport", "recent_active_sport"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "reason_of_like_sport": [
                self.from_text()
                ],
            "recent_active_sport": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
                ],
            }              


    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:   
        return [FollowupAction("request_animal_detail")]



# ----------------------------------------------------
# Ask user for details about animal
#
# ----------------------------------------------------
class RequestAnimalDetail(FormAction):
    def name(self) -> Text:
        return "request_animal_detail"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        # If user's topic is general      - ask for specific
        # If user's topic is about sport  - ask why it's interesting
        # If user's topic is about animal - ask if user owns one
        # Else the bot can't say much about the topic  and will take it as a request
        # slot "topic_general" is auto filled and can be used    
        return ["type_of_animal", "own_animal"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {                
                "type_of_animal": [
                    self.from_entity(entity="animal"),
                    ],
                "own_animal": [
                    self.from_intent(intent="affirm", value=True),
                    self.from_intent(intent="deny", value=False),
                    ],
                }


    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:       
        
        return [FollowupAction("request_more_animal_detail")]



# ----------------------------------------------------
# Ask user for more details about animal
#
# ----------------------------------------------------
class RequestMoreAnimalDetail(FormAction):
    def name(self) -> Text:
        return "request_more_animal_detail"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        # Check if user owns animal
        own_animal = tracker.get_slot("own_animal")

        # If user owns animal, then ask about breed
        # If user doesn't own, then ask if user will own one in future
        if own_animal:
            return ["animal_breed"]
        else:
            return ["plan_to_own_animal"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {                
                "animal_breed": [
                    self.from_text(),                    
                    ],
                "plan_to_own_animal": [
                    self.from_text(),     
                    ],
                }


    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:       
        # Stop message
        #dispatcher.utter_message("Okay, the bot has gathered enough information for now. It will now start storing them!")

        return [FollowupAction("action_store_detail")]
    

    
# ----------------------------------------------------
# Used for storing details
#
# ----------------------------------------------------
class ActionStoreDetail(Action):
    def name(self) -> Text:
        return "action_store_detail"

    def run(self, dispatcher, tracker, domain): # -> List[EventType]:         
        
        user          = tracker.get_slot("email")
        sport         = tracker.get_slot("type_of_sport")
        recent_active = tracker.get_slot("recent_active_sport")
        animal        = tracker.get_slot("type_of_animal")
        own_animal    = tracker.get_slot("own_animal")

        if recent_active:
            bool_recent_active = "yes"
        else:
            bool_recent_active = "no"

        if own_animal:
            bool_own_animal = "yes"
        else:
            bool_own_animal = "no"
        
        Data = { 'user': [user],
                 'sport': [sport],
                 'recent_active': [bool_recent_active],
                 'animal': [animal],
                 'own': [bool_own_animal]
               }
        
        # Store relevant data to a csv file
        df = pd.DataFrame(Data, columns = ['user', 'sport', 'recent_active', 'animal', 'own'])  
        df.to_csv('df.csv', index=False, mode='a', header=False)

        # Clear the following slots
        return [SlotSet("type_of_sport", None),
                SlotSet("reason_of_like_sport", None),
                SlotSet("recent_active_sport", None),
                SlotSet("type_of_animal", None),
                SlotSet("own_animal", None),
                SlotSet("animal_breed", None),
                SlotSet("plan_to_own_animal", None),                
                FollowupAction("action_end_conversation"),
                ]

        

# ----------------------------------------------------
# Chit chat questions for second session
#
# ----------------------------------------------------
class ChitChatSecond(FormAction):   
    def name(self) -> Text:
        return "chit_chat_second"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["how_been", "free_time", "where_live", "how_is_place", "weather"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {            
            "how_been": [                
                self.from_text(),                
                ],            
            "free_time": [
                self.from_text(),
                ],            
            "where_live": [
                self.from_text(),
                ],            
            "how_is_place": [
                self.from_text(),
                ],                 
            "weather": [
                self.from_text(),
                ],       
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        return [FollowupAction("action_fetch_from_db")]

    
# ----------------------------------------------------
# Custom action used for second time interaction
#
# ----------------------------------------------------
class ActionFetchFromDB(Action):
    def name(self) -> Text:
        return "action_fetch_from_db"

    def run(self, dispatcher, tracker, domain): # -> List[EventType]:
        
        # Define column headers
        # col_list = ["user", "topic", "recent_active"]        
        col_list = ['user', 'sport', 'recent_active', 'animal', 'own']
            
        # Read the csv file
        df = pd.read_csv("df.csv", usecols=col_list)

        # Extract the 'user' column and turn it into a list
        user_list = df["user"]
        user_list = user_list.tolist()

        # Get the user's index
        user = tracker.get_slot("email")
        index = user_list.index(user)

        # Get the user's topic and recent activity bool
        user_sport         = df["sport"][index]          # Returns a sport type
        user_recent_active = df["recent_active"][index]  # Returns if user recently active
        user_animal        = df["animal"][index]         # Returns a animal type
        user_own_animal    = df["own"][index]            # Returns if user owns animal

        # Conver to bool
        if user_recent_active == "yes":
            bool_user_recent_active = True
        else:
            bool_user_recent_active = False

        if user_own_animal == "yes":
            bool_user_own_animal = True
        else:
            bool_user_own_animal = False

##        dispatcher.utter_message("(Debug message), user_recent_active: " + str(bool_user_recent_active) + "\nuser_own_animal: " + str(bool_user_own_animal))

        
        return [SlotSet("type_of_sport", user_sport),
                SlotSet("recent_active_sport", bool_user_recent_active),
                SlotSet("type_of_animal", user_animal),
                SlotSet("own_animal", bool_user_own_animal),
                FollowupAction("long_term_question"),
                ]



# ----------------------------------------------------
# Ask user for more details about animal
#
# ----------------------------------------------------
class LongTermQuestion(FormAction):
    def name(self) -> Text:
        return "long_term_question"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        
        sport         = tracker.get_slot("type_of_sport")
        recent_active = tracker.get_slot("recent_active_sport")
        animal        = tracker.get_slot("type_of_animal")
        own_animal    = tracker.get_slot("own_animal")


        # - If user did the activity: ask how did it go
        # - If not, ask if user will do in the future
        if recent_active == True and own_animal == True:
            return ["how_go_sport", "watch_sport", "how_old_is_animal", "animal_color"]
        elif recent_active == True and own_animal == False:
            return ["how_go_sport", "watch_sport", "why_like_animal", "animal_size"]
        elif recent_active == False and own_animal == True:
            return ["play_in_future", "watch_sport", "how_old_is_animal", "animal_color"]
        elif recent_active == False and own_animal == False:
            return ["play_in_future", "watch_sport", "why_like_animal", "animal_size"]
        
        


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "how_go_sport": [
                self.from_text(),
                ],
            "watch_sport": [
                self.from_text(),
                ],
            "play_in_future": [
                self.from_text(),
                ],
            "how_old_is_animal": [
                self.from_text(),
                ],
            "animal_color": [
                self.from_text(),
                ],
            "why_like_animal": [
                self.from_text(),
                ],
            "animal_size": [
                self.from_text(),
                ],
            }


    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:       
        # Stop message
        #dispatcher.utter_message("Okay, the bot has gathered enough information for now. It will now start storing them!")

        return [FollowupAction("action_end_conversation_final")]




# ----------------------------------------------------
# Custom action for ending first session
#
# ----------------------------------------------------
class ActionEndConversation(Action):
    def name(self) -> Text:
        return "action_end_conversation"

    def run(self, dispatcher, tracker, domain):
           
        dispatcher.utter_message("Thank you! You have now finished the first session, please proceed to the form for a small survey then come back to restart the session.")
        return []


class ActionEndConversationFinal(Action):
    def name(self) -> Text:
        return "action_end_conversation_final"

    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message("Great, it was nice talking to you!")
        dispatcher.utter_message("Thank you! You are almost done! Please proceed to the form to answer a few final questions.")
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
        r = requests.post("https://aebfc2ed232f.ngrok.io/get_disclosure",
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
        r = requests.post('https://aebfc2ed232f.ngrok.io/get_answer',
                          json={"userID": str(userID), "data": str(data)} )


        if r.json()["error"] == None:
            response = r.json()["answer"]
            dispatcher.utter_message(str(response))
        else:
            dispatcher.utter_message("Something went wrong")
            #Ask new question instead because unexpected error occurred

        return []
