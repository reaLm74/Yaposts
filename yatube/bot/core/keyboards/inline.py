from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_menu = [
    [InlineKeyboardButton(
        text="📝 Последние 10 постов",
        callback_data='posts'
    )],
    [InlineKeyboardButton(
        text="👨‍🏫 Авторы постов",
        callback_data='authors'
    )],
    [InlineKeyboardButton(
        text="📚 Группы постов",
        callback_data='groups'
    )],
]

select_menu = InlineKeyboardMarkup(
    inline_keyboard=keyboard_menu,
)
