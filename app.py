from flask import Flask, request
from flask_mail import Mail, Message
from bs4 import BeautifulSoup

import io
import csv
import markdown
import re

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route("/upload", methods=['POST'])
def readCsv():
    if request.method == 'POST':
        # Get uploaded file
        f = request.files['myFile']

        # Convert the uploaded file into Stream
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        csv_rows = list(csv.reader(stream, delimiter=","))

        emails = []
        names = []

        # Split emails and names from CSV file
        for i in range(len(csv_rows)):
            for j in range(len(csv_rows[i])):
                if is_valid_email(csv_rows[i][j]):
                    emails.append(csv_rows[i][j])
                else:
                    names.append(csv_rows[i][j])

        # print(emails)

        # Only this part is remaining
        for i in range(len(names)):
            msg = Message('Test Emails From Flask',
                          sender='nachiketbhuta@gmail.com')
            msg.body = generateMessage(names[i])
            msg.add_recipient(emails[i])
            mail.send(msg)

        return ''


# To check for valid email
def is_valid_email(email):
    if len(email) > 7:
        return bool(re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email))

# To generate body depending on markdown file
def generateMessage(name):
    html = markdown.markdown(open("body.md").read())
    soup = BeautifulSoup(html, features="lxml")
    # print(soup.get_text())
    return ("Hey {name}, " + soup.get_text() + " ").format(name=name)


if __name__ == '__main__':
    app.run(debug=True)
