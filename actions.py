# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


# from typing import Any, Dict, List, Text, Union, Optional

# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.forms import FormAction
# # from gdrive_service import GDriveService



# class PersonForm(FormAction):
    
#     """Collects person information and adds it to the spreadsheet"""

#     def name(self) -> Text:
#         """Unique identifier of the form"""
#         return "person_form"
    
    
#     @staticmethod
#     def required_slots(tracker) -> List[Text]:
#         return ["person_name"]
    
    
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

#         """A dictionary to map required slots to
#             - an extracted entity
#             - intent: value pairs
#             - a whole message
#             or a list of them, where a first match will be picked"""

#         return {
#             "person_name": [
#                 self.from_entity(entity="user.name"),
#             ],
#         }


#     def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
#         """Define what the form has to do
#             after all required slots are filled"""

#         # utter submit template
#         dispatcher.utter_message("Thanks!")
#         return []

from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction


class TopicForm(FormAction):
    """Example of a custom form action"""
    
    def name(self):
        """Unique identifier of the form"""
        
        return "topic_form"
    
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        
        # possible to introduce logic
#         if tracker.get_slot('cuisine') == 'greek':
        return ["topic"]


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        
        
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message("Submitted!")
        return []
    
    
#     def slot_mappings(slef):
#         # type: () -> Dick[Text: Union[Dict, List[Dict]]]
#         """A dictionary to map required slots to
#         - an extracted entity
#         - intent: value pairs
#         - a whole message or a list of them, where a first match will be picked"""
        
#         return {"ooutdoor_seating": [self.from_entity(entity="seating"), 
#                                      self.form_intent(intent='affirm', value = True),
#                                      self.from_intent(intent='deny', value = False)]}



# class ActionChitchat(Action):
#     """Returns the chitchat utterance dependent on the intent"""

#     def name(self) -> Text:
#         return "action_chitchat"

#     def run(self, dispatcher, tracker, domain) -> List[EventType]:
#         intent = tracker.latest_message["intent"].get("name")

#         # retrieve the correct chitchat utterance dependent on the intent
#         if intent in [
#             "ask_builder",
#             "ask_weather",
#             "ask_howdoing",
#             "ask_whatspossible",
#             "ask_whatisrasa",
#             "ask_isbot",
#             "ask_howold",
#             "ask_languagesbot",
#             "ask_restaurant",
#             "ask_time",
#             "ask_wherefrom",
#             "ask_whoami",
#             "handleinsult",
#             "nicetomeeyou",
#             "telljoke",
#             "ask_whatismyname",
#             "ask_howbuilt",
#             "ask_whoisit",
#         ]:
#             dispatcher.utter_message(template=f"utter_{intent}")
#         return []