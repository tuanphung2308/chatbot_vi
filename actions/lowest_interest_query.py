import csv

from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction


class LowestBankInterestQuery(Action):
    def name(self):
        return "lowest_interest_query"

    def run(self, dispatcher, tracker, domain):
        with open('banking_interest.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            min_row = csv_reader[0]

            for row in csv_reader:
                if row[2] < min_row[2]:
                    min_row = row
            dispatcher.utter_message(
                text=f"Hiện tại, theo tỉ giá tháng 4, lãi suất thấp nhất trong các ngân hàng là của {min_row[0]} với {min_row[2]}%.")
            dispatcher.utter_message(text=f"Em còn có thể giúp đỡ được gì cho anh/chị không ạ?")
            return []
