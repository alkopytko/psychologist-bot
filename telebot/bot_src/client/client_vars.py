from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class UD:
    problem = 'problem'
    budget = 'budget'


class CallBacks:
    request = 'request'
    counsellor = 'counsellor'


class Keyboards:
    class Buttons:
        request = InlineKeyboardButton(text='Publish new request', callback_data=CallBacks.request)
        counsellor = InlineKeyboardButton(text='My counsellor', callback_data=CallBacks.counsellor)

    @classmethod
    def start(cls):
        return InlineKeyboardMarkup([[cls.Buttons.request], [cls.Buttons.counsellor]])


class TextMessages:
    hello = 'Welcome to BOT! BOT is a mental health platform, where you can find a psychologists according to ' \
            'your needs and opportunities. '

    request_enter = 'Please, describe your problem in several sentences.\n' \
                    'If you want to cancel, use /cancel command'
