import os
import random
import pandas as pd
import requests
import csv

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    ActionExecuted,
    UserUttered,
)



# ----------------------------------------------------
# Get the user's email for identification purpose
# ----------------------------------------------------
class RequestEmail(FormAction):
    """Asks for the user's email, call the newsletter API and sign up user"""

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

        #email = tracker.get_slot("email")
        #dispatcher.utter_message("Email " + email + " was recorded.")
        dispatcher.utter_message("Email recorded. (This message is for debug purpose and will be removed in the future!)")            
        return []



# ----------------------------------------------------
# Start the conversation based
# on if the user exists or not  
# ----------------------------------------------------
class ActionStartConversation(Action):
    """Returns the chitchat utterance dependent on the intent"""

    def name(self) -> Text:
        return "action_start_conversation"

    @staticmethod
    def start_story_events(story_intent): # type: (Text) -> List[Dict]
        return [ActionExecuted("action_listen")] + [UserUttered("/" + story_intent, {
            "intent": {"name": story_intent, "confidence": 1.0},
            "entities": {}
        })]

    def run(self, dispatcher, tracker, domain): # -> List[EventType]:

        # Use the email to check if user exists
        email = tracker.get_slot("email")
        user_list = pd.read_csv('output.csv', usecols=[0])
        user_list = user_list.user.tolist()

        # If user exists
        if email in user_list:
            dispatcher.utter_message("User exists.  (This message is for debug purpose and will be removed in the future!)")            
            return self.start_story_events("user.second_time") 
            #return another stoy where another action is taken, which will look into the csv
        else: # User does not exist
            dispatcher.utter_message("User does not exist. (This message is for debug purpose and will be removed in the future!)")
            # Trigger the story for first time conversation
            return self.start_story_events("user.first_time")


        
##        intent = tracker.latest_message["intent"].get("name")

        # retrieve the correct chitchat utterance dependent on the intent
##        if intent in [
##            "ask_builder",
##            "ask_weather",
##            "ask_howdoing",
##            "ask_whatspossible",
##            "ask_whatisrasa",
##            "ask_isbot",
##            "ask_howold",
##            "ask_languagesbot",
##            "ask_restaurant",
##            "ask_time",
##            "ask_wherefrom",
##            "ask_whoami",
##            "handleinsult",
##            "nicetomeeyou",
##            "telljoke",
##            "ask_whatismyname",
##            "ask_howbuilt",
##            "ask_whoisit",
##        ]:
##            dispatcher.utter_message(template=f"utter_{intent}")
##        return []


# ----------------------------------------------------
# Used for first time conversation,
# i.e. user does not exist in the database
#   - Ask which sport the user likes, this info is recorded
#   - Ask why user likes it, this info is not recorded
# ----------------------------------------------------

class RequestSport(FormAction):
    
    def name(self) -> Text:
        return "request_sport"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["type_of_topic", "reason_of_like", "recent_active"]
##        return ["type_of_topic"]
        

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "type_of_topic": [                
                self.from_entity(entity="sport"),
                self.from_entity(entity="animal"),
                self.from_text(intent="enter_data"),
                ],
            "reason_of_like": [                
                self.from_entity(entity="reason"),
                self.from_text(intent="enter_data"),
                ],
            "recent_active": [                
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
                ],
            }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        type_of_topic  = tracker.get_slot("type_of_topic")
        reason_of_like = tracker.get_slot("reason_of_like")
        recent_active  = tracker.get_slot("recent_active")
        user           = tracker.get_slot("email")

        Data = { 'User': [user],
                 'Topic': [type_of_topic],
                 'Recently active': [recent_active]
                 }
        # Store relevant data to a csv file
        df = pd.DataFrame(Data, columns = ['User', 'Topic', 'Recently active'])

##        if not os.path.isfile('output.csv'):
##            df.to_csv('output.csv', index=False, header='columns')
##        else:
        df.to_csv('output.csv', index=False, mode='a', header=False)


        # Something for fun before ending the session         
        # ConceptNet API
        obj_has_property = requests.get('http://api.conceptnet.io/query?start=/c/en/' + type_of_topic + '&rel=/r/HasProperty').json()
        obj_receive_action = requests.get('http://api.conceptnet.io/query?start=/c/en/' + type_of_topic + '&rel=/r/ReceivesAction').json()

        # Randomly pick a topic with 50/50 chance
        random_topic_pick = random.randint(0,1)
        if random_topic_pick == 0:
            decided_topic = obj_has_property
        else:
            decided_topic = obj_receive_action

        # Randomly pick one of the search result
        if (len(decided_topic) > 1):
            edge_index = random.randint(0, len(decided_topic)-1)
            topic_property = decided_topic['edges'][edge_index]['end']['label']
        else:
            topic_property = decided_topic['edges'][0]['end']['label']
        
        
        # Stop message
        dispatcher.utter_message("Okay, the bot has gathered enough information for now. Thank you!")
        dispatcher.utter_message("Before you leave, do you ever wonder why " + type_of_topic + " is " + topic_property + "?")
        dispatcher.utter_message("Just some random stuff for you to think about.")

        dispatcher.utter_message("(The following messages are for debug purpose and will be removed in the future!)")
        dispatcher.utter_message("Topic: " + type_of_topic + ", for user:" + user + ", was recorded.")
        dispatcher.utter_message("Reason: " + reason_of_like + ", was received, but won't be recorded.")
        dispatcher.utter_message("User did the activity recently: " + str(recent_active) + ", was recorded.")
        
        # Clear the following slots
        return [SlotSet("type_of_topic", None),
                SlotSet("reason_of_like", None),
                SlotSet("recent_active", None),]

    

# ----------------------------------------------------
# Used for second time conversation,
# i.e. user exists in the database
#   - Check database if user's "recent_active" is true
#       - If it's true, ask how did it go
#       - If it's false, ask what another sport user likes
# ----------------------------------------------------

class InquireSport(FormAction):
    
    def name(self) -> Text:
        return "inquire_sport"
    
    def run(self, dispatcher, tracker, domain):

        # Get the user's email
        user = tracker.get_slot("email")
        
        # Define column headers
        col_list = ["user", "topic", "recent_active"]

        # Read the csv file
        df = pd.read_csv("output.csv", usecols=col_list)

        # Extract the 'user' column and turn it into a list
        user_list = df["user"]
        user_list = user_list.tolist()

        # Get the user's index
        index = user_list.index(user)

        # Get the user's topic and recent activity bool
        user_topic    = df["topic"][index]          # Returns a sport type
        recent_active = df["recent_active"][index]  # Returns a boolean

        # ConceptNet API
        obj_url = requests.get('http://api.conceptnet.io/query?start=/c/en/' + user_topic + '&rel=/r/ExternalURL').json()


        # - If user did the activity: ask how did it go
        # - If user did not: ask what other sport is liked
        if recent_active:
            dispatcher.utter_message("So last time we talked about " + user_topic +
                                     ", and you did that recently. How did it go?")
        else:
            # Randomly pick one of the search result to ask - used if recent activity is False            
            if (len(obj_url['edges']) > 1):
                edge_index = random.randint(0, len(obj_url['edges'])-1)
                topic_url = obj_url['edges'][edge_index]['end']['term']
                dispatcher.utter_message("So last time we talked about " + user_topic +
                                     ", here is a link you might find interesting!")
                dispatcher.utter_message(str(topic_url))
            elif (len(obj_url['edges']) == 1):
                topic_url = obj_url['edges'][0]['end']['term']
                dispatcher.utter_message("So last time we talked about " + user_topic +
                                     ", here is a link you might find interesting!")
                dispatcher.utter_message(str(topic_url))
            else:                
                dispatcher.utter_message("So last time we talked about " + user_topic +
                                     ", would you like to try it sometimes in the future?")            
            
        return []


        

# ----------------------------------------------------------------------

# Possible actions:
#   - Fetch URL to related topics, because user's interested 

    


    



class AnswerForm(FormAction):
    
    def name(self) -> Text:
        return "answer_form"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        # if the user does not exist, then we need to fill in some slots
        if tracker.get_slot('user_first_time') == False:
            return ["topic", "type_of_topic"]
        else:
            return ["type_of_animal"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "type_of_sport": [
                self.from_entity(entity="sport"),
                ],
            "type_of_animal": [
                self.from_entity(entity="animal"),
                ],
            }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> List[Dict]:

        topic = tracker.get_slot("type_of_topic")
        user = tracker.get_slot("email")

        search_term = topic
        
        obj_isa = requests.get('http://api.conceptnet.io/query?start=/c/en/' + search_term + '&rel=/r/IsA').json()
        obj_has_propertty = requests.get('http://api.conceptnet.io/query?start=/c/en/' + search_term + '&rel=/r/HasProperty').json()


        if topic == 'sport':
            topic_detail = tracker.get_slot("type_of_sport")
        elif topic == 'animal':
            topic_detail = tracker.get_slot("type_of_animal")
        
        Data = { 'User': [user],
                 'Topic': [topic],
                 'Detail': [topic_detail],
                 }

        df = pd.DataFrame(Data, columns = ['User', 'Topic', 'Detail'])

##        if not os.path.isfile('output.csv'):
##            df.to_csv('output.csv', index=False, header='columns')
##        else:
        df.to_csv('output.csv', index=False, mode='a', header=False)
            
        return []
      




## used to set specific topic related slots
##class ActionGetDetail(Action):
##    """Returns the explanation for the sales form questions"""
##
##    def name(self) -> Text:
##        return "action_get_detail"
##
##    def run(self, dispatcher, tracker, domain):
##
##        topic = tracker.get_slot("type_of_topic")
##
##        if topic == 'sport':
##            ent = next(tracker.get_latest_entity_values(topic), None)
##            return [SlotSet('type_of_sport', ent)]
##        elif topic == 'animal':
##            ent = next(tracker.get_latest_entity_values(topic), None)  
##            return [SlotSet('type_of_animal', ent)]



class ActionAskReason(Action):
    """Returns the explanation for the sales form questions"""

    def name(self) -> Text:
        return "action_ask_reason"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent'].get('name')

        topic = tracker.get_slot("type_of_topic")

        intent = tracker.latest_message["intent"].get("name")

        # retrieve the correct chitchat utterance dependent on the intent
        if topic in [
            "sport",
            "animal",
        ]:
            dispatcher.utter_message(template=f"utter_ask_reason_{topic}")
        return []



class ActionCheckUserExist(Action):

    def name(self) -> Text:
        return "action_check_user_exist"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent'].get('name')

        topic = tracker.get_slot("type_of_topic")

        intent = tracker.latest_message["intent"].get("name")

        # retrieve the correct chitchat utterance dependent on the intent
        if topic in [
            "sport",
            "animal",
        ]:
            dispatcher.utter_message(template=f"utter_ask_reason_{topic}")
        return []


class ActionReadFromCsv(Action):

    def name(self) -> Text:
        return "action_read_from_csv"

    def run(self, dispatcher, tracker, domain):
        df = pd.read_csv('output.csv')
            
        print(df)
        
        return []
