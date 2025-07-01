import string

def clean_message(msg):
    msg = msg.lower()
    msg = msg.translate(str.maketrans('', '', string.punctuation))
    return msg
