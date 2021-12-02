import calendar
import datetime


def get_schedule(context):
    try:
        now = datetime.datetime.now()
        date_input = datetime.datetime.strptime(context["date"], "%d-%m-%Y")
        if date_input >= now:
            # проверяем чтбы дата не была прошлым
            city_from = context["city_from"]
            city_to = context["city_to"]
            datetime_Moscow_Yekat_fly = ["(по вторникам и пятницам)"]
            datetime_Moscow_Krasnodar_fly = ["(по средам и воскресеньям)"]
            datetime_Moscow_Vladivostok_fly = ["(по понедельникам и четвергам)"]
            datetime_Yekat_Moscow_fly = ["(по средам и пятницам)"]
            datetime_Yekat_Krasnodar_fly = ["(по средам)"]
            datetime_Yekat_Vladivostok_fly = ["(по четвергам и субботам)"]
            datetime_Vladivostok_Moscow_fly = ["(по пятницам и субботам)"]
            datetime_Vladivostok_Krasnodar_fly = ["1, 15 и 26 числа каждого месяца)"]

            for month in range(1, 13):
                cal = calendar.monthcalendar(now.year, month)
                for date in cal:
                    monday = date[0]
                    tuesday = date[1]
                    wednesday = date[2]
                    thursday = date[3]
                    friday = date[4]
                    saturday = date[5]
                    sunday = date[6]

                    # из Москвы
                    if tuesday > 0:  # рейс летает по вторникам и пятницам из Москвы в Екатеринбург
                        # вторник
                        Moscow_Yekat_datetime_am = datetime.datetime(year=now.year, month=month, day=tuesday, hour=7,
                                                                     minute=00)
                        Moscow_Yekat_datetime_pm = datetime.datetime(year=now.year, month=month, day=tuesday, hour=19,
                                                                     minute=15)
                        if Moscow_Yekat_datetime_am >= date_input:
                            datetime_Moscow_Yekat_fly.append(Moscow_Yekat_datetime_am.strftime("%d-%m-%Y %H.%M"))
                        if Moscow_Yekat_datetime_pm >= date_input:
                            datetime_Moscow_Yekat_fly.append(Moscow_Yekat_datetime_pm.strftime("%d-%m-%Y %H.%M"))

                    if friday > 0:
                        # пятница
                        Moscow_Yekat_datetime1 = datetime.datetime(year=now.year, month=month, day=friday, hour=20,
                                                                   minute=40)
                        if Moscow_Yekat_datetime1 >= date_input:
                            datetime_Moscow_Yekat_fly.append(Moscow_Yekat_datetime1.strftime("%d-%m-%Y %H.%M"))

                    if wednesday > 0:  # рейс летает по средам и воскресеньям из Москвы в Краснодар
                        # среда
                        Moscow_Krasnodar_datetime = datetime.datetime(year=now.year, month=month, day=wednesday, hour=7,
                                                                      minute=20)
                        if Moscow_Krasnodar_datetime >= date_input:
                            datetime_Moscow_Krasnodar_fly.append(Moscow_Krasnodar_datetime.strftime("%d-%m-%Y %H.%M"))

                    if sunday > 0:
                        # воскресенье
                        Moscow_Krasnodar_datetime1 = datetime.datetime(year=now.year, month=month, day=sunday, hour=21,
                                                                       minute=00)
                        if Moscow_Krasnodar_datetime1 >= date_input:
                            datetime_Moscow_Krasnodar_fly.append(Moscow_Krasnodar_datetime1.strftime("%d-%m-%Y %H.%M"))

                    if monday > 0:  # рейс летает по понедельникам и четвергам из Москвы во Владивосток
                        # понедельник
                        Moscow_Vladivostok_datetime = datetime.datetime(year=now.year, month=month, day=monday, hour=5,
                                                                        minute=30)
                        if Moscow_Vladivostok_datetime >= date_input:
                            datetime_Moscow_Vladivostok_fly.append(
                                Moscow_Vladivostok_datetime.strftime("%d-%m-%Y %H.%M"))

                    if tuesday > 0:
                        # четверг
                        Moscow_Vladivostok_datetime1 = datetime.datetime(year=now.year, month=month, day=tuesday,
                                                                         hour=17, minute=10)
                        if Moscow_Vladivostok_datetime1 >= date_input:
                            datetime_Moscow_Vladivostok_fly.append(
                                Moscow_Vladivostok_datetime1.strftime("%d-%m-%Y %H.%M"))

                    # из Екатеринбурга
                    if wednesday > 0:  # рейс летает по средам и пятницам из Екатеринбурга в Москву
                        # среда
                        Yekat_Moscow_datetime_am = datetime.datetime(year=now.year, month=month, day=wednesday, hour=10,
                                                                     minute=45)
                        Yekat_Moscow_datetime_pm = datetime.datetime(year=now.year, month=month, day=wednesday, hour=22,
                                                                     minute=30)
                        if Yekat_Moscow_datetime_am >= date_input:
                            datetime_Yekat_Moscow_fly.append(Yekat_Moscow_datetime_am.strftime("%d-%m-%Y %H.%M"))
                        if Yekat_Moscow_datetime_pm >= date_input:
                            datetime_Yekat_Moscow_fly.append(Yekat_Moscow_datetime_pm.strftime("%d-%m-%Y %H.%M"))

                    if friday > 0:
                        # пятница
                        Yekat_Moscow_datetime1 = datetime.datetime(year=now.year, month=month, day=friday, hour=12,
                                                                   minute=10)
                        if Yekat_Moscow_datetime1 >= date_input:
                            datetime_Yekat_Moscow_fly.append(Yekat_Moscow_datetime1.strftime("%d-%m-%Y %H.%M"))

                    if wednesday > 0:  # рейс летает по средам из Екатеринбурга в Краснодар
                        # среда
                        Yekat_Krasnodar_datetime = datetime.datetime(year=now.year, month=month, day=wednesday, hour=11,
                                                                     minute=25)
                        if Yekat_Krasnodar_datetime >= date_input:
                            datetime_Yekat_Krasnodar_fly.append(Yekat_Krasnodar_datetime.strftime("%d-%m-%Y %H.%M"))

                    if thursday > 0:  # рейс летает по четвергам и субботам из Екатеринбурга во Владивосток
                        # четверг
                        Yekat_Vladivostok_datetime = datetime.datetime(year=now.year, month=month, day=thursday, hour=5,
                                                                       minute=30)
                        if Yekat_Vladivostok_datetime >= date_input:
                            datetime_Yekat_Vladivostok_fly.append(Yekat_Vladivostok_datetime.strftime("%d-%m-%Y %H.%M"))

                    if saturday > 0:
                        # суббота
                        Yekat_Vladivostok_datetime1 = datetime.datetime(year=now.year, month=month, day=saturday,
                                                                        hour=17, minute=10)
                        if Yekat_Vladivostok_datetime1 >= date_input:
                            datetime_Yekat_Vladivostok_fly.append(
                                Yekat_Vladivostok_datetime1.strftime("%d-%m-%Y %H.%M"))

                    if friday > 0:  # рейс летает по пятницам и субботам из Владивостока в Москву
                        # пятница
                        Vladivostok_Moscow_datetime = datetime.datetime(year=now.year, month=month, day=friday, hour=2,
                                                                        minute=20)
                        if Vladivostok_Moscow_datetime >= date_input:
                            datetime_Vladivostok_Moscow_fly.append(
                                Vladivostok_Moscow_datetime.strftime("%d-%m-%Y %H.%M"))

                    if saturday > 0:
                        # суббота
                        Vladivostok_Moscow_datetime1 = datetime.datetime(year=now.year, month=month, day=saturday,
                                                                         hour=10, minute=45)
                        if Vladivostok_Moscow_datetime1 >= date_input:
                            datetime_Vladivostok_Moscow_fly.append(
                                Vladivostok_Moscow_datetime1.strftime("%d-%m-%Y %H.%M"))

                    for day in date:  # рейс летает 1, 15 и 26 числа каждого месяца из Владивостока в Краснодар
                        if day == 1 or day == 15 or day == 26:
                            Vladivostok_Krasnodar_datetime = datetime.datetime(year=now.year, month=month, day=day,
                                                                               hour=17, minute=00)
                            if Vladivostok_Krasnodar_datetime >= date_input:
                                datetime_Vladivostok_Krasnodar_fly.append(
                                    Vladivostok_Krasnodar_datetime.strftime("%d-%m-%Y %H.%M"))

            a = ["", "1) ", "2) ", "3) ", "4) ", "5) "]
            schedule = {
                "Москва": {
                    "Екатеринбург": "; ".join([x + y for x, y in zip(a, datetime_Moscow_Yekat_fly[:6])]),
                    "Краснодар": "; ".join([x + y for x, y in zip(a, datetime_Moscow_Krasnodar_fly[:6])]),
                    "Владивосток": "; ".join([x + y for x, y in zip(a, datetime_Moscow_Vladivostok_fly[:6])])},
                "Екатеринбург": {
                    "Москва": "; ".join([x + y for x, y in zip(a, datetime_Yekat_Moscow_fly[:6])]),
                    "Краснодар": "; ".join([x + y for x, y in zip(a, datetime_Yekat_Krasnodar_fly[:6])]),
                    "Владивосток": "; ".join([x + y for x, y in zip(a, datetime_Yekat_Vladivostok_fly[:6])])},
                "Владивосток": {
                    "Москва": "; ".join([x + y for x, y in zip(a, datetime_Vladivostok_Moscow_fly[:6])]),
                    "Краснодар": "; ".join([x + y for x, y in zip(a, datetime_Vladivostok_Krasnodar_fly[:6])])}

            }
            context["flight_schedule"] = schedule[city_from][city_to]
            return context
    except Exception:
        return False
