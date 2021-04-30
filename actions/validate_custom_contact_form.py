import re
from typing import Text, List, Any, Dict, Optional

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

phone_pattern = re.compile("^(0?)(3[2-9]|5[6|8|9]|7[0|6-9]|8[0-6|8|9]|9[0-4|6-9])[0-9]{7}$")


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
