# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#

import os
import pandas as pd

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
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


##class ActionChitchat(Action):
##    """Returns the chitchat utterance dependent on the intent"""
##
##    def name(self) -> Text:
##        return "action_choose_topic"
##
##    def run(self, dispatcher, tracker, domain) -> List[EventType]:
##
##        intent = tracker.latest_message["intent"].get("name")
##
##        # retrieve the correct chitchat utterance dependent on the intent
##        if intent in [
##            "sport",
##            "animal",
##            "food",
##            "travel",
##            ]:
##            
##            dispatcher.utter_message(template=f"utter_{intent}")
##
##            #return [SlotSet("topic", intent)]
##            return[]


class AnswerForm(FormAction):
    
    def name(self) -> Text:
        return "answer_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        if tracker.get_slot('type_of_topic') == 'sport':
            return ["type_of_sport", "reason_sport"]
        elif tracker.get_slot('type_of_topic') == 'animal':
            return ["type_of_animal", "reason_animal"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
##        user_intent = tracker.latest_message["intent"].get("name")
        return {
            "type_of_sport": [
                self.from_entity(entity="sport"),
                ],
            "reason_sport": [
                self.from_entity(entity="reason"),
                ],
            "type_of_animal": [
                self.from_entity(entity="animal"),
                ],
            "reason_sport": [
                self.from_entity(entity="reason"),
                ],
            }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> List[Dict]:

        topic = tracker.get_slot("type_of_topic")

        if topic == 'sport':
            topic_detail = tracker.get_slot("type_of_sport")
        elif topic == 'animal':
            topic_detail = tracker.get_slot("type_of_animal")
        
        Data = { 'Name': 'placeholder',
                 'Topic': [topic],
                 'Detail': [topic_detail],
                 }

        df = pd.DataFrame(Data, columns = ['Name', 'Topic', 'Detail'])

        if not os.path.isfile('output.csv'):
            df.to_csv('output.csv', index=False, header='columns')
        else:
            df.to_csv('output.csv', index=False, mode='a', header=False)
            
        return []
      

class ActionGetTopic(Action):
    """Returns the explanation for the sales form questions"""

    def name(self) -> Text:
        return "action_get_topic"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent'].get('name')
        dispatcher.utter_message("Rasa got topic: "+intent)

        return [SlotSet('type_of_sport', intent)]


class ActionGetDetail(Action):
    """Returns the explanation for the sales form questions"""

    def name(self) -> Text:
        return "action_get_detail"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent'].get('name')
        dispatcher.utter_message("Rasa got detail: "+intent)

        return [SlotSet('reason_sport', intent)]
