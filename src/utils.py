import smtplib
import html2text
import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from logger import logger


def prepare_comment(issue: dict, assignees: dict, duedate):
    """
    Prepare the comment from the given arguments and return it
    """

    comment = ''
    if assignees:
        for assignee in assignees:
            comment += f'@{assignee["login"]} '
    else:
        logger.info(f'No assignees found for issue #{issue["number"]}')

    comment += f'The issue is due on: {duedate.strftime("%b %d, %Y")}'
    logger.info(f'Issue {issue["title"]} | {comment}')

    return comment


def prepare_email_message(issue, assignees, duedate):
    """
    Prepare the email message, subject and mail_to addresses
    """
    subject = f'Re: [{config.repository}] {issue["title"]} (#{issue["number"]})'
    _assignees = ''
    mail_to = []
    if assignees:
        for assignee in assignees:
            _assignees += f'@{assignee["name"]} '
            mail_to.append(assignee['email'])
    else:
        logger.info(f'No assignees found for issue #{issue["number"]}')

    message = f'Assignees: {_assignees}' \
              f'<br>The issue is due on: {duedate.strftime("%b %d, %Y")}' \
              f'<br><br>{issue["url"]}'

    return [subject, message, mail_to]


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
