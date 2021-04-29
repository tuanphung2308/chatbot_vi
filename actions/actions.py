import csv
import pathlib
import re
from typing import Text, List, Any, Dict, Optional

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import AllSlotsReset, SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import requests

names = pathlib.Path("data/names.txt").read_text().split("\n")
phone_pattern = re.compile("^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$")


class CheckExistedAppointment(Action):
    def name(self):
        return "check_appointment"

    def run(self, dispatcher, tracker, domain):
        print("Check appointment")
        most_recent_state = tracker.current_state()
        sender_id = most_recent_state['sender_id']

        with open('appointment.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] == sender_id:
                    customer_name = row[1]
                    phone_number = row[2]
                    print(row)
                    print("Found record")
                    dispatcher.utter_message(
                        text=f"Em đã tiếp nhận thông tin liên lạc của anh/chị: {customer_name} - {phone_number}. "
                             f"Bọn em sẽ cố gắng liên lạc lại trong thời gian sớm nhất.")
                    dispatcher.utter_message(buttons=[{
                        'payload': '/lai_suat',
                        'title': 'Lãi suất ngân hàng'
                    }, {
                        'payload': '/thi_truong',
                        'title': 'Tình hình thị trường'
                    }, {
                        'payload': '/goodbye',
                        'title': 'Không quan tâm'
                    }],
                        text="Trong thời gian chờ đợi, anh/chị có thể tham khảo các mục sau ạ.")
                    return []
        dispatcher.utter_message(
            text=f"Qua kiểm tra, bên em vẫn chưa tiếp nhận thông tin liên lạc của anh/chị. Vì vậy, anh/chị có thể vui "
                 f"lòng cung cấp những thông tin sau ạ")
        return [FollowupAction(name='custom_contact_form')]


class AddAppointment(Action):
    def name(self):
        return "add_appointment"

    def run(self, dispatcher, tracker, domain):
        most_recent_state = tracker.current_state()
        sender_id = most_recent_state['sender_id']
        # r = requests.get(
        #     'https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}'.format(sender_id,
        #                                                                                                    fb_access_token)).json()
        # first_name = r['first_name']
        # last_name = r['last_name']
        print(sender_id)

        customer_name = tracker.slots.get("customer_name")
        phone_number = tracker.slots.get("phone_number")
        print("Add appointment action")
        print(customer_name, phone_number)

        with open('appointment.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([sender_id, customer_name, phone_number, False])
        dispatcher.utter_message(
            text=f"Em đã tiếp nhận thông tin liên lạc của anh/chị: {customer_name} - {phone_number}. "
                 f"Bọn em sẽ cố gắng liên lạc lại trong thời gian sớm nhất kể từ 24 tiếng tiếp nhận tin nhắn này.")
        return [SlotSet("customer_name", None), SlotSet("phone_number", None)]


class ValidateCustomContactForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_custom_contact_form"

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
    ) -> Optional[List[Text]]:
        return slots_mapped_in_domain

    async def extract_gave_info_correctly(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        intent = tracker.get_intent_of_latest_message()
        return {"gave_info_correctly": intent == "affirm"}

    def validate_customer_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `customer_name` value."""

        # If the name is super short, it might be wrong.
        print(f"First name given = {slot_value} length = {len(slot_value)}")
        if len(slot_value) <= 1:
            dispatcher.utter_message(text=f"Tên của anh/chị có vẻ không hợp lệ. Xin vui lòng nhập lại.")
            return {"customer_name": None}
        else:
            return {"customer_name": slot_value}

    def validate_phone_number(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `phone_number` value."""
        # Clean slot value
        slot_value = slot_value.strip().replace(' ', '')

        # If the phone is super short, it might be wrong.
        print(f"Phone number given = {slot_value} length = {len(slot_value)}")
        if not phone_pattern.match(slot_value):
            dispatcher.utter_message(text=f"Số điện thoại của có vẻ không hợp lệ. Xin vui lòng nhập lại.")
            print('not valid folder number')
            return {"phone_number": None}
