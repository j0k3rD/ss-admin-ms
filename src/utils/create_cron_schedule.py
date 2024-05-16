from celery.schedules import crontab


def create_cron_schedule(
    scheduling_type,
    start_datetime,
    end_datetime,
    day_of_week=None,
    day_of_month=None,
    day_of_year=None,
):
    start_time = start_datetime.time()
    print(start_time)
    end_time = end_datetime.time()
    print(end_time)

    if scheduling_type == "diario":
        cron_string = f"{start_time.minute} {start_time.hour} * * *"
        cron_value = crontab(
            hour=start_time.hour,
            minute=start_time.minute,
        )
    elif scheduling_type == "semanal":
        cron_string = f"{start_time.minute} {start_time.hour} * * {day_of_week}"
        cron_value = crontab(
            day_of_week=day_of_week,
            hour=start_time.hour,
            minute=start_time.minute,
        )
    elif scheduling_type == "mensual":
        cron_string = f"{start_time.minute} {start_time.hour} {day_of_month} * *"
        cron_value = crontab(
            day_of_month=day_of_month,
            hour=start_time.hour,
            minute=start_time.minute,
        )
    elif scheduling_type == "anual":
        cron_string = (
            f"{start_time.minute} {start_time.hour} {day_of_month} {day_of_year} *"
        )
        cron_value = crontab(
            day_of_month=day_of_month,
            month_of_year=day_of_year,
            hour=start_time.hour,
            minute=start_time.minute,
        )
    else:
        raise ValueError(f"Tipo de programación no soportado: {scheduling_type}")

    if end_datetime <= start_datetime:
        cron_string = ""

    return cron_value
