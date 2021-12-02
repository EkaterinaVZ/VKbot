from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

TEMPLATE_PATH = "files/base_ticket.png"
FONT_PATH = "files/Roboto-Regular.ttf"
FONT_SIZE = 15
FONT_SIZE_MINI = 10

BLACK = (0, 0, 0, 255)
NAME_OFFSET = (45, 190)
CITY_FROM = (45, 220)
CITY_TO = (45, 240)
FLIGHT_OFFSET = (45, 275)
NUMBER_OF_SEATS = (45, 295)
PHONE_NUMBER = (65, 335)
EMAIL_OFFSET = (65, 345)

AVATAR_SIZE = 60
AVATAR_OFFSET = (300, 30)


def generate_ticket(name, email, city_from, city_to, phone_number, flight, number_of_seats):
    base = Image.open(TEMPLATE_PATH).convert("RGBA")
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    font_mini = ImageFont.truetype(FONT_PATH, FONT_SIZE_MINI)

    draw = ImageDraw.Draw(base)
    draw.text(NAME_OFFSET, "Name: " + name, font=font, fill=BLACK)
    draw.text(CITY_FROM, "City from: " + city_from, font=font, fill=BLACK)
    draw.text(CITY_TO, "City to: " + city_to, font=font, fill=BLACK)
    draw.text(FLIGHT_OFFSET, "Flight: " + flight, font=font, fill=BLACK)
    draw.text(NUMBER_OF_SEATS, "Seats: " + number_of_seats, font=font, fill=BLACK)
    draw.text(EMAIL_OFFSET, "Email: " + email, font=font_mini, fill=BLACK)
    draw.text(PHONE_NUMBER, "Phone number: " + phone_number, font=font_mini, fill=BLACK)

    response = requests.get(url=f"https://i.pravatar.cc/{AVATAR_SIZE}?u={email}")
    avatar_file = BytesIO(response.content)
    avatar = Image.open(avatar_file)

    base.paste(avatar, AVATAR_OFFSET)
    temp_file = BytesIO()
    base.save(temp_file, "png")
    temp_file.seek(0)
    # with open("files/ticket_example.png", "wb") as f:
    #     base.save(f, "png")
    return temp_file
#
# generate_ticket("Иванов Иван Иваныч", "artprojectt@mail.ru", "Москва", "Екатеринбург", "89120094452",
#                  "06-04-2021 19.15", "4")
