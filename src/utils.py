import smtplib
import html2text
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(from_email: str, to_email: list, subject: str, html_body: str):
    smtp_server = smtplib.SMTP(config.smtp_server, config.smtp_port)
    smtp_server.starttls()
    smtp_server.login(config.smtp_username, config.smtp_password)

    # Create the plain text version of the email
    text_body = html2text.html2text(html_body)

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = ", ".join(to_email)
    message['Subject'] = subject

    # Attach the plain text version
    # message.attach(MIMEText(text_body, 'plain'))

    # Attach the HTML version
    message.attach(MIMEText(html_body, 'html'))

    # Send the email
    text = message.as_string()
    smtp_server.sendmail(from_email, to_email, text)

    smtp_server.quit()
