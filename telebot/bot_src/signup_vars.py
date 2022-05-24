from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Categories:
    categories = ['social', 'children', 'work', 'loss', 'eatingbehaviour', 'partner', 'parents', 'trauma', 'obsessive',
                  'compulsive', 'personalcrisis', 'addiction', ]


class CallBacks:
    skip = 'skip'
    done = 'done'


class Keyboards:
    class Buttons:
        skip = InlineKeyboardButton(text='Skip', callback_data=CallBacks.skip)
        done = InlineKeyboardButton(text='Done', callback_data=CallBacks.done)

    @classmethod
    def skip(cls):
        return InlineKeyboardMarkup([[cls.Buttons.skip]])

    @classmethod
    def categories(cls, active_list=None):
        if active_list is None:
            active_list = []
        step = 3
        keys = [
            InlineKeyboardButton(
                text=i + (' -', ' +')[i in active_list],
                callback_data=i)
            for i in Categories.categories
        ]
        return InlineKeyboardMarkup([keys[i:i + step] for i in range(0, len(keys), step)] + [[cls.Buttons.done]])


class TextMessages:
    hello = 'Please ask several questions about your education, experience, requests you work with and level of ' \
            'languages. \n' \
            'If you want to cancel, use /cancel command'
    first_name = 'Enter your first name:'
    last_name = 'Enter your last name:'
    scans = 'Upload the scans of your diplomas or student\'s I.D.'
    photo = 'Upload your profile photo (not necessary, recommended)'
    categories = 'Please choose categories of requests you are working with:'
    lang_level = 'What is your level of language? Type, please.'
    congratulations = 'Congrats! Your profile is ready. Soon it will be checked by moderator and you will be able to ' \
                      'work via Oriole. If you plan to earn money via '
