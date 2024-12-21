from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email Configuration
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL

app = Flask(__name__)

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email():
    subject = "Rapport om tomt kaffelager"
    body = "Det er rapportert om tomt / snart tomt for kaffe på loungen."

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['POST'])
def report():
    send_email()
    return jsonify({"message": "Report sent successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
