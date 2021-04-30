import csv

from rasa_sdk import Action
from rasa_sdk.events import FollowupAction


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
