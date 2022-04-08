import unittest
from copy import deepcopy
from freezegun import freeze_time
from pony.orm import rollback, db_session
from unittest import TestCase
from unittest.mock import patch, Mock
from vk_api.bot_longpoll import VkBotMessageEvent

import settings
from chatbot import Bot
from generate_ticket import generate_ticket


def isolate_db(test_funk):
    def wrapper(*args, **kwargs):
        with db_session:
            test_funk(*args, **kwargs)
            rollback()

    return wrapper


class Test2(TestCase):
    RAW_EVENT = {
        'type': 'message_new',
        'object': {'message': {'date': 1615815564, 'from_id': 5070114, 'id': 184, 'out': 0,
                               'peer_id': 5070114, 'text': 'ghxfghjf', 'conversation_message_id': 183,
                               'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [],
                               'is_hidden': False},
                   'client_info':
                       {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback',
                                           'intent_subscribe',
                                           'intent_unsubscribe'], 'keyboard': True, 'inline_keyboard': True,
                        'carousel': False, 'lang_id': 0}}, 'group_id': 203109674,
        'event_id': '9adc69a65c7b7f5460168aea993fc4dcb91faa1b'
    }

    def test_run(self):
        count = 5
        obj = {"a": 1}
        events = [obj] * count  # [obj, obj, ...]
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch("chatbot.vk_api.VkApi"):
            with patch("chatbot.VkBotLongPoll", return_value=long_poller_listen_mock):
                chatbot = Bot("", "")
                chatbot.on_event = Mock()
                chatbot.send_image = Mock()
                chatbot.send_email = Mock()
                chatbot.run()

                chatbot.on_event.assert_called()
                chatbot.on_event.assert_any_call(obj)
                assert chatbot.on_event.call_count == count

    INPUTS = [
        "привет",
        "помоги мне с билетами",
        "как дела?",
        "что с погодой сегодня?",
        "ticket",
        "москва",
        "Екатеринбург",
        "06-04-2021",
        "2",
        "4",
        "нет",
        "89120094452",
        "Иванов Иван Иваныч",
        "Да",
        "artprojectt@mail.ru",
        "Спасибо!"
    ]
    EXPECTED_OUTPUTS = [
        settings.INTENTS[0]["answer"],
        settings.INTENTS[2]["answer"],
        settings.INTENTS[5]["answer"],
        settings.INTENTS[6]["answer"],
        settings.SCENARIOS["book_tickets"]["steps"]["step1"]["text"],
        settings.SCENARIOS["book_tickets"]["steps"]["step2"]["text"],
        settings.SCENARIOS["book_tickets"]["steps"]["step3"]["text"],
        settings.SCENARIOS["book_tickets"]["steps"]["step4"]["text"].format(city_from='Москва', city_to='Екатеринбург',
                                                                            date='06-04-2021',
                                                                            flight_schedule=
                                                                            '(по вторникам и пятницам);'
                                                                            '1) 06-04-2021 07.00; '
                                                                            '2) 06-04-2021 19.15; '
                                                                            '3) 09-04-2021 20.40; '
                                                                            '4) 13-04-2021 07.00; '
                                                                            '5) 13-04-2021 19.15'),
        settings.SCENARIOS["book_tickets"]["steps"]["step5"]["text"],
        settings.SCENARIOS["book_tickets"]["steps"]["step6"]["text"],
        settings.SCENARIOS["book_tickets"]["steps"]["step7"]["text"],
        settings.SCENARIOS["book_tickets"]["steps"]["step8"]["text"],
        settings.SCENARIOS["book_tickets"]["steps"]["step9"]["text"].format(city_from='Москва', city_to='Екатеринбург',
                                                                            date='06-04-2021',
                                                                            flight='2) 06-04-2021 19.15',
                                                                            number_of_seats='4', comment='',
                                                                            phone_number='89120094452',
                                                                            name='Иванов Иван Иваныч'),
        settings.SCENARIOS["book_tickets"]["steps"]["step10"]["text"].format(name='Иванов Иван Иваныч'),
        settings.SCENARIOS["book_tickets"]["steps"]["step11"]["text"].format(phone_number='89120094452',
                                                                             name='Иванов Иван Иваныч',
                                                                             email="artprojectt@mail.ru"),
        settings.INTENTS[8]["answer"]
    ]

    @isolate_db
    @freeze_time("2021-04-06")
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event["object"]["message"]["text"] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch("chatbot.VkBotLongPoll", return_value=long_poller_mock):
            chatbot = Bot(" ", " ")
            chatbot.api = api_mock
            chatbot.send_image = Mock()
            chatbot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs["message"])
        assert real_outputs == self.EXPECTED_OUTPUTS

    def test_image_generation(self):
        with open("files/art.jpg", "rb") as avatar_file:
            avatar_mock = Mock()
            avatar_mock.content = avatar_file.read()

        with patch("requests.get", return_value=avatar_mock):
            ticket_file = generate_ticket("Иванов Иван Иваныч", "artprojectt@mail.ru", "Москва",
                                          "Екатеринбург", "89120094452", "06-04-2021 19.15", "4")

        with open("files/ticket_example.png", "rb") as expected_file:
            expected_bytes = expected_file.read()

        assert ticket_file.read() == expected_bytes


if __name__ == '__main__':
    unittest.main()
