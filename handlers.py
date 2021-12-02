#!/usr/bin/venv python 3
"""
Handler - функция, которая на вход принимает text (текст входящего сообщения) и context (dict), а возвращает bool:
True если шаг пройден, False если данные введены неправильно.
"""
import re

import settings_schedule
from generate_ticket import generate_ticket

re_city = re.compile(r"\b^москва$|^екатеринбург$|^краснодар$|^владивосток$\b")
re_date = re.compile(r"\b(0[1-9]|1[0-9]|2[0-9]|3[01])-(0[1-9]|1[012])-(202[1])\b")
re_number = re.compile(r"\b[1-5]\b")
re_text = re.compile(r"\b(да|нет)\b")
re_phone_number = re.compile(r"^\+?[78][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$")
re_name = re.compile(r"^[\w\-\s]{3,40}$")
re_email = re.compile(r"\b[a-zA-z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b")


def handle_city(text, context):
    match = re.match(re_city, text)
    if match:
        if "city_from" not in context:
            context["city_from"] = text.title()

        else:
            context["city_to"] = text.title()
        return True
    else:
        return False


def handle_date(text, context):
    match = re.match(re_date, text)
    if match:
        context["date"] = text
        if settings_schedule.get_schedule(context):
            return True
        else:
            context["answer"] = "нет такого рейса"
            return True
    else:
        return False


def handle_number(text, context):
    match = re.match(re_number, text)
    if match:
        if "flight" not in context:
            context["flight"] = context["flight_schedule"].split("; ")[int(text)]
        else:
            context["number_of_seats"] = text
        return True
    else:
        return False


def handle_comment(text, context):
    if text != "нет":
        context["comment"] = text
    else:
        context["comment"] = ""
    return True


def handle_text(text, context):
    match = re.match(re_text, text)
    if match:
        if text == "нет":
            context["return"] = "выход"
        return True
    else:
        return False


def handle_phone_number(text, context):
    match = re.match(re_phone_number, text)
    if match:
        context["phone_number"] = text
        return True
    else:
        return False


def handle_name(text, context):
    match = re.match(re_name, text)
    if match:
        context["name"] = text.title()
        return True
    else:
        return False


def handle_email(text, context):
    matches = re.findall(re_email, text)
    if len(matches) > 0:
        context["email"] = matches[0]
        return True
    else:
        return False


def handler_generate_ticket(text, context):
    return generate_ticket(name=context["name"],
                           email=context["email"],
                           city_from=context["city_from"],
                           city_to=context["city_to"],
                           phone_number=context["phone_number"],
                           flight=context["flight"],
                           number_of_seats=context["number_of_seats"],
                           )
