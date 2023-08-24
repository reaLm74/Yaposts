import datetime


def year(request):
    """Добавляет в контекст переменную year с годом. """
    return {
        'year': datetime.date.today().year,
    }
