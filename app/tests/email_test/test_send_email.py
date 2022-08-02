''' 

import re
from textwrap import dedent
from packaging import version



from flask_redmail import RedMail
from flask import Flask
from redmail import EmailSender
import redmail 


def dummy_send(msg):
    pass

def remove_email_content_id(s:str, repl="<ID>"):
    return re.sub(r"(?<================)[0-9]+(?===)", repl, s)

# Why cls_dummy_smtp ?
def test_send(cls_dummy_smtp):
    app = Flask("pytest")
    app.config["EMAIL_HOST"] = "localhost"
    app.config["EMAIL_PORT"] = 0
    app.config["EMAIL_USERNAME"] = "me@example.com"
    app.config["EMAIL_PASSWORD"] = "1234" # I assume this can be anything test.
    app.config["EMAIL_SENDER"] = "no-reply@example.com"
    app.config["EMAIL_CLS_SMTP"] = cls_dummy_smtp



    email = RedMail()
    email.init_app(app)
    # change value to not none.
    a = 'fl0fkj' 
    assert email.sender is a



    with app.app_context():
        email.sender.send_message = dummy_send
        email.send(
            subject="An example",
            receivers=["me@example.com"],
            html="<h1>An example</h1>"
        )
    # change value to not none.
    assert email.sender is None

'''