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
        if not os.path.isfile('output.csv'):
            df = pd.DataFrame(columns = ['user', 'topic', 'recent_active'])  
            df.to_csv('output.csv', index=False, header='columns')
        
        #email = tracker.get_slot("email")
        #dispatcher.utter_message("Email " + email + " was recorded.")
        dispatcher.utter_message("===============================================")
        dispatcher.utter_message("The following message is for debug purpose and will be removed in the future!")            
        dispatcher.utter_message("Email received, proceeding to the next step...")
        dispatcher.utter_message("===============================================")
        return []



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
        user_list = pd.read_csv('output.csv', usecols=[0])
        user_list = user_list.user.tolist()

        # Decide on follow up action accordingly
        if email not in user_list:
            dispatcher.utter_message("===============================================")
            dispatcher.utter_message("The following message is for debug purpose and will be removed in the future!")            
            dispatcher.utter_message("User is not found in the databse, requesting more details...")
            dispatcher.utter_message("===============================================")
            return [FollowupAction("request_detail")]
        else:
            dispatcher.utter_message("===============================================")
            dispatcher.utter_message("The following message is for debug purpose and will be removed in the future!")            
            dispatcher.utter_message("User found in database...")
            dispatcher.utter_message("===============================================")
            return [FollowupAction("action_second_time")]



# ----------------------------------------------------
# Used for first time conversation
#   - Ask which sport the user likes
#   - Ask when did user last do the activity
# ----------------------------------------------------

class RequestSport(FormAction):
    def name(self) -> Text:
        return "request_detail"


    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ["type_of_topic", "recent_active"]


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "type_of_topic": [
                self.from_entity(entity="sport"),
##                self.from_entity(entity="animal"),
                self.from_text(intent="enter_data"),
                ],
            "recent_active": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
                ],
            }              
                           

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:       
        # Stop message
        dispatcher.utter_message("Okay, the bot has gathered enough information for now. Thank you!")

        return [FollowupAction("action_store_detail")]

    
# ----------------------------------------------------
# Used for storing details
#
# ----------------------------------------------------
class ActionStoreDetail(Action):
    def name(self) -> Text:
        return "action_store_detail"

    def run(self, dispatcher, tracker, domain): # -> List[EventType]:
        dispatcher.utter_message("===============================================")
        dispatcher.utter_message("The following message is for debug purpose and will be removed in the future!")            
        dispatcher.utter_message("The bot is now remembering...")
        dispatcher.utter_message("===============================================")

        user          = tracker.get_slot("email")
        type_of_topic = tracker.get_slot("type_of_topic")
        recent_active = tracker.get_slot("recent_active")
        
        Data = { 'user': [user],
                 'topic': [type_of_topic],
                 'recent_active': [recent_active]
               }
        
        # Store relevant data to a csv file
        df = pd.DataFrame(Data, columns = ['user', 'topic', 'recent_active'])
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


        dispatcher.utter_message("===============================================")
        dispatcher.utter_message("The following message is for debug purpose and will be removed in the future!")            
        dispatcher.utter_message("Only one will be used in the end product.")
        dispatcher.utter_message("===============================================")

        dispatcher.utter_message("Possible conversation end line 1:")
        dispatcher.utter_message("Before you leave, did you know that " + type_of_topic + " is " + topic_property + "?\n")
        
        dispatcher.utter_message("Possible conversation end line 2:")
        dispatcher.utter_message(template=f"utter_ask_reason_of_like")
        dispatcher.utter_message(" ")
##        dispatcher.utter_message("Possible conversation end line 3: (This route is currently not available)")
##        dispatcher.utter_message(template=f"utter_ask_continue:")

##        dispatcher.utter_message("\n\n(The following messages are for debug purpose and will be removed in the future!)")
##        dispatcher.utter_message("Topic: " + type_of_topic + ", for user:" + user + ", was recorded.")
##        dispatcher.utter_message("User did the activity recently: " + str(recent_active) + ", was recorded.")
            
        # Clear the following slots
        return [SlotSet("type_of_topic", None),
                SlotSet("recent_active", None),]



# ----------------------------------------------------
# Custom action for continuing for question generation
#
# ----------------------------------------------------
class ActionMoreTopic(Action):
    def name(self) -> Text:
        return "action_more_topic"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent'].get('name')

        if intent == "affirm":
            dispatcher.utter_message("What would you like to talk about?")
            dispatcher.utter_message("(Enter free text. Currently it relies completely on ConceptNet, reply may be unexpected or does not make sense)")

            return []
        else:            
            dispatcher.utter_message("Okay, bye.")
            return []



class ActionMoreTopicProcess(Action):
    def name(self) -> Text:
        return "action_more_topic_process"

    def run(self, dispatcher, tracker, domain):
        search_term = tracker.latest_message["text"]

        # Q1
        obj_has_prerequisite = requests.get('http://api.conceptnet.io/query?start=/c/en/' + search_term + '&rel=/r/HasPrerequisite').json()
        if len(obj_has_prerequisite['edges'])> 0:
            edge_index = random.randint(0, len(obj_has_prerequisite['edges'])-1)
            prerequisite = obj_has_prerequisite['edges'][edge_index]['end']['label']
            dispatcher.utter_message("Q1: Can you " + search_term + " without " + prerequisite + "?")

        # Q2
        obj_has_property = requests.get('http://api.conceptnet.io/query?start=/c/en/' + search_term + '&rel=/r/HasProperty').json()
        if len(obj_has_property['edges'])> 0:
            edge_index = random.randint(0, len(obj_has_property['edges'])-1)
            has_property = obj_has_property['edges'][edge_index]['end']['label']
            dispatcher.utter_message("Q2: Is " + search_term + " really " + has_property + "?") 

        # Q3
        obj_antonym = requests.get('http://api.conceptnet.io/query?start=/c/en/' + search_term + '&rel=/r/Antonym').json()
        if len(obj_antonym['edges'])> 0:
            edge_index = random.randint(0, len(obj_antonym['edges'])-1)
            antonym = obj_antonym['edges'][edge_index]['end']['label']
            dispatcher.utter_message("Q3: I'm guessing you dislike " + antonym + "?")

        # Q4
        obj_synonym = requests.get('http://api.conceptnet.io/query?start=/c/en/' + search_term + '&rel=/r/Synonym').json()
        if len(obj_synonym['edges'])> 0:
            edge_index = random.randint(0, len(obj_synonym['edges'])-1)
            synonym = obj_synonym['edges'][edge_index]['end']['label']
            dispatcher.utter_message("Q4: Maybe you also like " + synonym + "?")

        # Q5
        obj_has_first_subevent = requests.get('http://api.conceptnet.io/query?start=/c/en/' + search_term + '&rel=/r/HasFirstSubevent').json()
        if len(obj_has_first_subevent['edges'])> 0:
            edge_index = random.randint(0, len(obj_has_first_subevent['edges'])-1)
            first_subevent = obj_has_first_subevent['edges'][edge_index]['end']['label']
            dispatcher.utter_message("Q5: Ever tried " + search_term + " without " + first_subevent + "?")

        return []        

# ----------------------------------------------------
# Custom action used for second time interaction
#
# ----------------------------------------------------
class ActionSecondTime(Action):
    def name(self) -> Text:
        return "action_second_time"

    def run(self, dispatcher, tracker, domain): # -> List[EventType]:
        
        # Define column headers
        col_list = ["user", "topic", "recent_active"]

        # Read the csv file
        df = pd.read_csv("output.csv", usecols=col_list)

        # Extract the 'user' column and turn it into a list
        user_list = df["user"]
        user_list = user_list.tolist()

        # Get the user's index
        user = tracker.get_slot("email")
        index = user_list.index(user)

        # Get the user's topic and recent activity bool
        user_topic    = df["topic"][index]          # Returns a sport type
        recent_active = df["recent_active"][index]  # Returns a boolean


        # - If user did the activity: ask how did it go
        # - If user did not: ask what other sport is liked
        

        
        if recent_active:
            dispatcher.utter_message("So last time we talked about " + user_topic +
                                     " and you did that recently. How did it go?")
        else:
            dispatcher.utter_message("===============================================")
            dispatcher.utter_message("The following message is for debug purpose and will be removed in the future!")            
            dispatcher.utter_message("Only one will be used in the end product.")
            dispatcher.utter_message("===============================================")
        
            dispatcher.utter_message("Possible reply 1:")
            dispatcher.utter_message("So last time we talked about " + user_topic +
                                     ", you think you will do that in the near future?\n")
                
            dispatcher.utter_message("Possible reply 2 (using API):")
            
            # ConceptNet API
            obj_url = requests.get('http://api.conceptnet.io/query?start=/c/en/' + user_topic + '&rel=/r/ExternalURL').json()
        
            # Randomly pick one of the search result to ask - used if recent activity is False            
            if (len(obj_url['edges']) > 1):
                edge_index = random.randint(0, len(obj_url['edges'])-1)
                topic_url = obj_url['edges'][edge_index]['end']['term']
                dispatcher.utter_message("So last time we talked about " + user_topic +
                                         ", here is a link you might find interesting!")
                dispatcher.utter_message(str(topic_url))
            elif (len(obj_url['edges']) == 1):
                topic_url = obj_url['edges'][0]['end']['term']
                dispatcher.utter_message("You like " + user_topic +
                                         ", right? Check this out!\n" + topic_url)
                dispatcher.utter_message(str(topic_url))
            else:                
                dispatcher.utter_message("So last time we talked about " + user_topic +
                                         ", would you like to try it sometimes in the future?")

        return []


# ----------------------------------------------------
# Start the conversation based
# on if the user exists or not  
# ----------------------------------------------------
##class ActionStartConversation(Action):
##    def name(self) -> Text:
##        return "action_start_conversation"
##
##
##    def run(self, dispatcher, tracker, domain): # -> List[EventType]:
##
##        # Use the email to check if user exists
##        email = tracker.get_slot("email")
##        user_list = pd.read_csv('output.csv', usecols=[0])
##        user_list = user_list.user.tolist()
##
##        # If user exists
##        if email in user_list:
##            
##        else: # User does not exist
##            dispatcher.utter_message("User does not exist. (This message is for debug purpose and will be removed in the future!)")
##            # Trigger the story for first time conversation
##            #return self.start_story_events("user.first_time")
##            return [SlotSet("user_first_time", True)]


        
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
# Used for second time conversation,
# i.e. user exists in the database
#   - Check database if user's "recent_active" is true
#       - If it's true, ask how did it go
#       - If it's false, ask what another sport user likes
# ----------------------------------------------------

##class InquireSport(FormAction):
##    
##    def name(self) -> Text:
##        return "inquire_sport"
##    
##    def run(self, dispatcher, tracker, domain):
##
##        # Get the user's email
##        user = tracker.get_slot("email")
##        
##        # Define column headers
##        col_list = ["user", "topic", "recent_active"]
##
##        # Read the csv file
##        df = pd.read_csv("output.csv", usecols=col_list)
##
##        # Extract the 'user' column and turn it into a list
##        user_list = df["user"]
##        user_list = user_list.tolist()
##
##        # Get the user's index
##        index = user_list.index(user)
##
##        # Get the user's topic and recent activity bool
##        user_topic    = df["topic"][index]          # Returns a sport type
##        recent_active = df["recent_active"][index]  # Returns a boolean
##
##        # ConceptNet API
##        obj_url = requests.get('http://api.conceptnet.io/query?start=/c/en/' + user_topic + '&rel=/r/ExternalURL').json()
##
##
##        # - If user did the activity: ask how did it go
##        # - If user did not: ask what other sport is liked
##        if recent_active:
##            dispatcher.utter_message("So last time we talked about " + user_topic +
##                                     ", and you did that recently. How did it go?")
##        else:
##            # Randomly pick one of the search result to ask - used if recent activity is False            
##            if (len(obj_url['edges']) > 1):
##                edge_index = random.randint(0, len(obj_url['edges'])-1)
##                topic_url = obj_url['edges'][edge_index]['end']['term']
##                dispatcher.utter_message("So last time we talked about " + user_topic +
##                                     ", here is a link you might find interesting!")
##                dispatcher.utter_message(str(topic_url))
##            elif (len(obj_url['edges']) == 1):
##                topic_url = obj_url['edges'][0]['end']['term']
##                dispatcher.utter_message("So last time we talked about " + user_topic +
##                                     ", here is a link you might find interesting!")
##                dispatcher.utter_message(str(topic_url))
##            else:                
##                dispatcher.utter_message("So last time we talked about " + user_topic +
##                                     ", would you like to try it sometimes in the future?")            
##            
##        return []


        

# ----------------------------------------------------------------------
    

##class AnswerForm(FormAction):
##    
##    def name(self) -> Text:
##        return "answer_form"
##
##    @staticmethod
##    def required_slots(tracker) -> List[Text]:
##        # if the user does not exist, then we need to fill in some slots
##        if tracker.get_slot('user_first_time') == False:
##            return ["topic", "type_of_topic"]
##        else:
##            return ["type_of_animal"]
##
##    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
##        return {
##            "type_of_sport": [
##                self.from_entity(entity="sport"),
##                ],
##            "type_of_animal": [
##                self.from_entity(entity="animal"),
##                ],
##            }
##
##    def submit(
##        self,
##        dispatcher: CollectingDispatcher,
##        tracker: Tracker,
##        domain: Dict[Text, Any],
##        ) -> List[Dict]:
##
##        topic = tracker.get_slot("type_of_topic")
##        user = tracker.get_slot("email")
##
##        search_term = topic
##        
##        obj_isa = requests.get('http://api.conceptnet.io/query?start=/c/en/' + search_term + '&rel=/r/IsA').json()
##        obj_has_propertty = requests.get('http://api.conceptnet.io/query?start=/c/en/' + search_term + '&rel=/r/HasProperty').json()
##
##
##        if topic == 'sport':
##            topic_detail = tracker.get_slot("type_of_sport")
##        elif topic == 'animal':
##            topic_detail = tracker.get_slot("type_of_animal")
##        
##        Data = { 'User': [user],
##                 'Topic': [topic],
##                 'Detail': [topic_detail],
##                 }
##
##        df = pd.DataFrame(Data, columns = ['User', 'Topic', 'Detail'])
##
####        if not os.path.isfile('output.csv'):
####            df.to_csv('output.csv', index=False, header='columns')
####        else:
##        df.to_csv('output.csv', index=False, mode='a', header=False)
##            
##        return []
      




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



##class ActionAskReason(Action):
##    """Returns the explanation for the sales form questions"""
##
##    def name(self) -> Text:
##        return "action_ask_reason"
##
##    def run(self, dispatcher, tracker, domain):
##        intent = tracker.latest_message['intent'].get('name')
##
##        topic = tracker.get_slot("type_of_topic")
##
##        intent = tracker.latest_message["intent"].get("name")
##
##        # retrieve the correct chitchat utterance dependent on the intent
##        if topic in [
##            "sport",
##            "animal",
##        ]:
##            dispatcher.utter_message(template=f"utter_ask_reason_{topic}")
##        return []



##class ActionCheckUserExist(Action):
##
##    def name(self) -> Text:
##        return "action_check_user_exist"
##
##    def run(self, dispatcher, tracker, domain):
##        intent = tracker.latest_message['intent'].get('name')
##
##        topic = tracker.get_slot("type_of_topic")
##
##        intent = tracker.latest_message["intent"].get("name")
##
##        # retrieve the correct chitchat utterance dependent on the intent
##        if topic in [
##            "sport",
##            "animal",
##        ]:
##            dispatcher.utter_message(template=f"utter_ask_reason_{topic}")
##        return []


##class ActionReadFromCsv(Action):
##
##    def name(self) -> Text:
##        return "action_read_from_csv"
##
##    def run(self, dispatcher, tracker, domain):
##        df = pd.read_csv('output.csv')
##            
##        print(df)
##        
##        return []
