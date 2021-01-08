import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from beans.user import User
from constants import TELEGRAM_API_TOKEN

import schedule
from threading import Thread
from time import sleep

bot = telebot.TeleBot(TELEGRAM_API_TOKEN)


# Send a message to Telegram chat without options
def send_message(user: User, state, session_id, response):
    # Note: state and session_id are only used for logging
    print("Sending response '{}' for user {} session {} state '{}'"
          .format(response, user.id, session_id, state))

    return bot.send_message(user.id, response)


# Send a message to Telegram chat with options, with two options in a row by default
def send_message_with_options(user: User, state, session_id, response, *options, row_width=5):
    print("Sending response '{}' with options '{}' for user {} session {} state '{}'"
          .format(response, options, user.id, session_id, state))

    # markup = types.InlineKeyboardMarkup(None, row_width)

    keyboard = [
        [InlineKeyboardButton("Hackerearth"), InlineKeyboardButton("Hackerrank")],
        [InlineKeyboardButton("Codechef"), InlineKeyboardButton("Spoj")],
        [InlineKeyboardButton("Codeforces"), InlineKeyboardButton("ALL")]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    # for option in options:
    #     markup.add(option)
    
    return bot.send_message(user.id, response, reply_markup=markup)

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def function_to_run(user: User, response):
    return bot.send_message(user.id, response)

def send_timed_message(user: User, time, response):    # Create the job in schedule.
    print("Sending response {} for user {} "
          .format(response, user.id))
    schedule.every().day.at(time).do(function_to_run, user, response)

    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.
    Thread(target=schedule_checker).start()
