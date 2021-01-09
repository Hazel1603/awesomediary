import uuid

from beans.item import Item
from beans.session import Session
from beans.user import User
from main import cache
from utils import default_if_blank, is_not_blank
import os
from os import path
from datetime import date 
from constants import FIRST_QUESTION, NEXT_QUESTION, BYE_MSG, RANDOM_QUESTION, RANDOM_QUESTION_ABOUT_THE_DAY

# Returns a session id for the current user, or generates a new one (UUID)
def get_current_session(user: User):
    session_key = __session_key(user)
    session_id = cache.get(session_key)

    if is_not_blank(session_id):
        return Session(session_id, False)
    else:
        new_session_id = uuid.uuid4().hex
        cache.set(session_key, new_session_id)
        return Session(new_session_id, True)

# Reads the Markdown file and returns a log of the entry
def get_journal_entry(user: User):
    filePath = "data/{}/{}.md".format(default_if_blank(user.handle,''), str(date.today()))
    f = open(filePath, "r") # Modify to get correct file based on user and date 
    
    response = "*Today's Date:*" + str(date.today()) + '\n'
    for line in f:
        if line == FIRST_QUESTION or line in NEXT_QUESTION:
            response += "*" + f.readline().rstrip('\n') + "*" + '\n'
        elif line == BYE_MSG:
            pass
        else:
            response += line
    return response

# Convert the message journal entry into a Markdown file by user and session_id
def add_to_journal(user: User, user_input):
#msg: get_message(user, session_id)

    user_folder = "data/{}".format(default_if_blank(user.handle, ''))

    if not path.exists(user_folder):
        os.mkdir(user_folder)
        
    new_file_name = user_folder + '/' + str(date.today()) + ".md"
    try:
        f1 = open(new_file_name, 'x')
        f1.write(user_input+ "<br>")
    except:
        f1 = open(new_file_name, 'a')
        f1.write("\n" + user_input+ "<br>")

    overall_file_name = user_folder + '/' + "summary.md"
    try: 
        f2 = open(overall_file_name, 'x')
        f2.write(user_input + "<br>")
    except: 
        f2 = open(overall_file_name, '1')
        f2.write(user_input+ "<br>")
    
    f1.close()
    f2.close()

def __session_key(user: User):
    return "session_{}".format(default_if_blank(user.id, ''))
