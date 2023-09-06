from datetime import date
from users.models import Profile
from django.contrib.auth import get_user_model

User = get_user_model()


def birthday(request):
    date_today = date.today().strftime('%m-%d')
    birthday = Profile.objects.filter(birth_date__iregex=date_today)
    answers_list = ', '.join(
        list(
            f'{obj.user.first_name} {obj.user.last_name}' for obj in birthday
        )
    )
    return {
        'birthday': answers_list,
    }
