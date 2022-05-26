from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class UD:
    problem = 'problem'
    budget = 'budget'


class CallBacks:
    request = 'request'
    consultations = 'consultations'


class Keyboards:
    class Buttons:
        request = InlineKeyboardButton(text='Publish new request', callback_data=CallBacks.request)
        counsellor = InlineKeyboardButton(text='My consultations', callback_data=CallBacks.consultations)

    @classmethod
    def start(cls):
        return InlineKeyboardMarkup([[cls.Buttons.request], [cls.Buttons.counsellor]])


class TextMessages:
    hello = 'Welcome to BOT! BOT is a mental health platform, where you can find a psychologists according to ' \
            'your needs and opportunities. '

    ask_problem = 'Please, describe your problem in several sentences.\n' \
                  'If you want to cancel, use /cancel command'
    wrong_problem_data = 'Please, type text message'
    ask_budget = 'Please, enter your budget for one session (type digits only)'
    wrong_budget_data = 'Please, type message with only digits'
    request_success = 'Success. Wait for response'
    cancel='Ok, cancel. Go to main menu...'
