import csv

from rasa_sdk import Action
from rasa_sdk.events import SlotSet


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
