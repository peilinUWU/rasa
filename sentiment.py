import typing
from typing import Any, Optional, Text, Dict, List, Type

from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata

import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

class SentimentAnalyzer(Component):
    """A pre-trained sentiment component"""

    name = "sentiment"
    # provides = ["entities"] # depricated 
    # requires = []           # depricated 
    defaults = {}
    language_list = ["en"]
    
    @classmethod
    def required_components(cls) -> List[Type[Component]]:
        """Specify which components need to be present in the pipeline."""

        return []
    

    def __init__(self, component_config=None):
        super(SentimentAnalyzer, self).__init__(component_config)

        
    def train(self, training_data, cfg, **kwargs):
        """Not needed, because the the model is pretrained"""
        pass


    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""
        
        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "sentiment",
                  "extractor": "sentiment_extractor"}

        return entity


    def process(self, message, **kwargs):
        """Retrieve the text message, pass it to the classifier
            and append the prediction results to the message class."""

        sid = SentimentIntensityAnalyzer()
        res = sid.polarity_scores(message.text)
        key, value = max(res.items(), key=lambda x: x[1])

        entity = self.convert_to_rasa(key, value)

        message.set("entities", [entity], add_to_output=True)
        

    def persist(self, file_name, model_dir):
        """Pass because a pre-trained model is already persisted"""
        pass
