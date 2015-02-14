from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail

account_sid = "ACdcb35266e1787a2de79a7789cb382199"
auth_token = "0e0ca7204a74f30b27c37d0565de8a9f"
client = TwilioRestClient(account_sid, auth_token)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['ICAN_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['ICAN_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_text(to, body):
    client.messages.create("+1" + str(to), from_="+12673184464", body)
