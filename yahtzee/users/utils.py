import os
import secrets

from PIL import Image
from flask import url_for
from flask_mail import Message

from yahtzee import app, mail


def save_picture(form_picture):
    """
    This function renames a form field picture with a unique path.
    It then saves new filename to filesystem.

    :return picture_filename: The new unique filename with basename 8 byte hex.
    """
    # create a new unique path for the form_picture to prevent collisions
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(
                        app.root_path,
                        'static/profile_pics',
                        picture_filename
                        )

    # resize to maximum image size
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # use the save method on the resized i picture at the unique picture_path
    i.save(picture_path)

    return picture_filename


def send_reset_email(user):
    """
    Gets a token from passed-in user and mail.send a reset password email.

    :param user: unauthenticated user
    """
    # get token for passed-in user from User model's get_reset_token() method
    token = user.get_reset_token()

    # create a Message instance
    msg = Message(
            'Password Reset Request',
            sender='noreply@demo.com',
            recipients=[user.email]
            )

    # add msg body with url_for link containing route, token and _external
    # boolean True to make link absolute url (relative works when inside app)
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not maket this request then ignore this email.
"""

    # send the email msg
    mail.send(msg)
