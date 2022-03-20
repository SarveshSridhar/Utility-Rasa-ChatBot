# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import dateparser
import arrow

city_database = {
    'chennai': 'Asia/Kolkata',
    'london': 'Europe/Dublin',
    'amsterdam': 'Europe/Amsterdam',
    'mumbai': 'Asia/Kolkata',
    'lisbon': 'Europe/Lisbon'
}

class ActionRememberPlace(Action):
    def name(self) -> Text:
        return "action_remember_place"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text,Any]]:

            current_place = next(tracker.get_latest_entity_values("place"), None)
            utc = arrow.utcnow()

            if not current_place:
                msg = f"It's {utc.format('HH:mm')} utc now, You can also give me the place you live for me to remember!!"
                dispatcher.utter_message(text=msg)
                return []
            
            tz_string = city_database.get(current_place, None)

            if not tz_string:
                msg = f"I don't recognize {current_place}. Is it spelled correctly? Or try another place"
                dispatcher.utter_message(text=msg)
                return []

            msg = f"I have now remembered the place you live!! The place you live is in {current_place} with place zone {city_database[current_place]}. "
            dispatcher.utter_message(text=msg)

            return [SlotSet("residential_location", current_place)]

class TellTimeDifference(Action):

    def name(self) -> Text:
        return "action_time_difference"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            time_from = tracker.get_slot("residential_location")
            time_to = next(tracker.get_latest_entity_values("place"),None)

            if not time_to:
                msg = f"To calculate the time difference between two cities, please provide the city name."
                dispatcher.utter_message(text=msg)
                return []
            if not time_from:
                msg = f"I don't know where you live, Please provide the city where you reside"
                dispatcher.utter_message(text=msg)
                return []

            tz_string = city_database.get(time_to,None)
            if not tz_string:
                msg = f"I dont recognize {time_to}, is it spelled correctly??"
                dispatcher.utter_message(text=msg)
                return []

            t1 = arrow.utcnow().to(city_database[time_to])
            t2 = arrow.utcnow().to(city_database[time_from])
            max_t, min_t = max(t1,t2), min(t1,t2)
            diff_seconds = dateparser.parse(str(max_t)[:19]) - dateparser.parse(str(min_t)[:19])
            diff_hours = int(diff_seconds.seconds/3600)

            msg = f"There is a time difference of {min(diff_hours, 24-diff_hours)}H time difference."
            dispatcher.utter_message(text=msg)
            
            return []


class ActionTellTime(Action):

    def name(self) -> Text:
        return "action_tell_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_place = next(tracker.get_latest_entity_values("place"), None)
        utc = arrow.utcnow()

        if not current_place:
            msg = "It's" + utc.format('HH:mm') + " utc now. You can also give me a place."
            dispatcher.utter_message(text = msg)
            return []
        
        tz_string = city_database.get(current_place, None)

        if not tz_string:
            msg = f"I don't recognize {current_place}. Is it spelled correctly? Or try another place"
            dispatcher.utter_message(text=msg)
            return []

        msg = f"Its {utc.to(city_database[current_place]).format('HH:mm')} in {current_place} now."
        dispatcher.utter_message(text=msg)

        return []
