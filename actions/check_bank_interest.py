import csv

from rasa_sdk import Action
from rasa_sdk.events import SlotSet, FollowupAction


class CheckBankInterest(Action):
    def name(self):
        return "check_bank_interest"

    def run(self, dispatcher, tracker, domain):
        if tracker.get_latest_entity_values('banks') is not None:
            bank_list = list(tracker.get_latest_entity_values('banks'))
            if len(bank_list):
                bank_name = list(tracker.get_latest_entity_values('banks'))[0]
                print(bank_name)

                with open('banking_interest.csv') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        if row[0] == bank_name or row[1] == bank_name:
                            dispatcher.utter_message(
                                text=f"Cảm ơn anh/chị đã quan tâm về lãi suất của ngân hàng {bank_name}. "
                                     f"Lãi suất tháng 4 của ngân hàng {bank_name} là {row[2]}%. "
                                     f"Tỉ suất cho vay của ngân hàng là {row[3]}%.")
                            dispatcher.utter_message(
                                text=f"Em còn có thể giúp đỡ gì cho anh/chị không ạ?.")
                            return []
        dispatcher.utter_message(
            text=f"Bọn em không tìm thấy thông tin về ngân hàng {bank_name}."
                 f"Tuy nhiên, để được hỗ trợ một cách nhanh nhất, anh chị có thể để lại thông tin để bọn em liên lạc hỗ trợ.")
        return [FollowupAction(name='custom_contact_form')]
