from flask import Flask, jsonify, render_template
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

app = Flask(__name__, static_url_path='/static')
load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER')

def send_email(mail_content):
    msg = EmailMessage()
    msg.set_content(mail_content)
    msg['Subject'] = 'She said YES!'
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_RECEIVER

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/yes.html', methods=['GET'])  
def yes_page():
    return render_template('yes.html')

@app.route('/send-email', methods=['POST'])
def send_email_route():
    try:
        mail_content = 'Congratulations, she said YES!'
        send_email(mail_content)
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Error sending email'}), 500

if __name__ == '__main__':
    app.run(port=4000)
