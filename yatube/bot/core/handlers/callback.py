import requests
from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils.html import strip_tags


def get_10_posts(url):
    response = requests.get(url).json()
    keyboard = [
        [InlineKeyboardButton(
            text=f'{strip_tags(post["text"])}',
            callback_data=f'post_{post["id"]}'
        )] for post in response['results'] if post['is_published']
    ]
    if response["previous"] is not None and response["next"] is not None:
        keyboard.append(
            [InlineKeyboardButton(
                text='◀️ Назад',
                callback_data=f'previous_{response["previous"]}'
            ), InlineKeyboardButton(
                text='В начало',
                callback_data='posts'
            ), InlineKeyboardButton(
                text='Вперед  ▶️',
                callback_data=f'next_{response["next"]}'
            )]
        )
    elif response["previous"] is not None:
        keyboard.append(
            [InlineKeyboardButton(
                text='◀️ Назад',
                callback_data=f'previous_{response["previous"]}'
            ), InlineKeyboardButton(
                text='В начало',
                callback_data='posts'
            )]
        )
    elif response["next"] is not None:
        keyboard.append(
            [InlineKeyboardButton(
                text='Вперед  ▶️',
                callback_data=f'next_{response["next"]}'
            )]
        )
    return keyboard


async def select_next_10_post(call: CallbackQuery, bot: Bot):
    url = 'http://127.0.0.1:8000/api/v1/posts/'
    if call.data.startswith('next_'):
        url = call.data[5:]
    elif call.data.startswith('previous_'):
        url = call.data[9:]
    markup = InlineKeyboardMarkup(inline_keyboard=get_10_posts(url))
    await call.message.edit_text(text="Наши посты", reply_markup=markup)


def post_menu(response):
    if response["group"]:
        keyboard = [
            [InlineKeyboardButton(
                text='Все посты автора',
                callback_data=f'user_{response["author"]}!0'
            )],
            [InlineKeyboardButton(
                text='Все посты группы',
                callback_data=f'group_{response["group"]}!0'
            )],
            [InlineKeyboardButton(text='Назад', callback_data='posts')]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(
                text='Все посты автора',
                callback_data=f'user_{response["author"]}!0'
            )],
            [InlineKeyboardButton(text='Назад', callback_data='posts')]
        ]
    return keyboard


async def select_post(call: CallbackQuery, bot: Bot):
    url = f'http://127.0.0.1:8000/api/v1/posts/{call.data[5:]}/'
    response = requests.get(url).json()
    text = f'{strip_tags(response["text"])}'
    markup = InlineKeyboardMarkup(inline_keyboard=post_menu(response))
    await call.message.edit_text(text=text, reply_markup=markup)


def get_10_user_group_posts(response, start_post=0):
    if response.get('slug'):
        url = f'group_{response["slug"]}'
    else:
        url = f'user_{response["id"]}'
    keyboard = [
        [InlineKeyboardButton(
            text=f'{strip_tags(post["text"])}',
            callback_data=f'post_{post["id"]}'
        )] for post in response['posts'][start_post: start_post + 10]
        if post['is_published']
    ]
    len_response = len(response['posts'])
    if 10 <= start_post <= len_response - 10:
        keyboard.append(
            [InlineKeyboardButton(
                text='◀️ Назад',
                callback_data=f'{url}!{start_post - 10}'
            ), InlineKeyboardButton(
                text='В начало',
                callback_data=f'{url}!0'
            ), InlineKeyboardButton(
                text='Вперед  ▶️',
                callback_data=f'{url}!{start_post + 10}'
            )]
        )
    elif 0 == start_post <= len_response - 10:
        keyboard.append(
            [InlineKeyboardButton(
                text='Вперед  ▶️',
                callback_data=f'{url}!{start_post + 10}'
            )]
        )
    elif 10 <= start_post >= len_response - 10:
        keyboard.append(
            [InlineKeyboardButton(
                text='◀️ Назад',
                callback_data=f'{url}!{start_post - 10}'
            ), InlineKeyboardButton(
                text='В начало',
                callback_data=f'{url}!0'
            )]
        )
    return keyboard


async def select_post_user(call: CallbackQuery, bot: Bot):
    user, start_post = call.data[5:].split('!')
    url = f'http://127.0.0.1:8000/api/v1/user/{user}/'
    response = requests.get(url).json()
    text = f'Посты пользователя ' \
           f'{response["first_name"]} {response["last_name"]}'
    markup = InlineKeyboardMarkup(
        inline_keyboard=get_10_user_group_posts(response, int(start_post)),
    )
    await call.message.edit_text(text=text, reply_markup=markup)


async def select_post_group(call: CallbackQuery, bot: Bot):
    group, start_post = call.data[6:].split('!')
    url = f'http://127.0.0.1:8000/api/v1/groups/{group}/'
    response = requests.get(url).json()
    text = f'Посты группы {response["title"]}'
    markup = InlineKeyboardMarkup(
        inline_keyboard=get_10_user_group_posts(response, int(start_post)),
    )
    await call.message.edit_text(text=text, reply_markup=markup)


def get_10_authors(response):
    keyboard = [
        [InlineKeyboardButton(
            text=f'{author["first_name"]} {author["last_name"]}',
            callback_data=f'user_{author["id"]}!0'
        )] for author in response['results'] if len(author['posts']) > 0
    ]
    return keyboard


async def select_author(call: CallbackQuery, bot: Bot):
    url = 'http://127.0.0.1:8000/api/v1/user/'
    response = requests.get(url).json()
    text = 'Авторы постов'
    markup = InlineKeyboardMarkup(inline_keyboard=get_10_authors(response))
    await call.message.edit_text(text=text, reply_markup=markup)


def get_10_groups(response):
    keyboard = [
        [InlineKeyboardButton(
            text=f'{group["title"]}',
            callback_data=f'group_{group["slug"]}!0'
        )] for group in response['results'] if len(group['posts']) > 0
    ]
    return keyboard


async def select_group(call: CallbackQuery, bot: Bot):
    url = 'http://127.0.0.1:8000/api/v1/groups/'
    response = requests.get(url).json()
    text = 'Группы постов'
    markup = InlineKeyboardMarkup(inline_keyboard=get_10_groups(response))
    await call.message.edit_text(text=text, reply_markup=markup)
