import os
import boto3
import config

ses_client = None
if config.notification_type == 'aws_email':
    ses_client = boto3.client('ses')


# Set the output value by writing to the outputs in the Environment File, mimicking the behavior defined here:
#  https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter
def set_github_action_output(output_name, output_value):
    f = open(os.path.abspath(os.environ["GITHUB_OUTPUT"]), "a")
    f.write(f'{output_name}={output_value}')
    f.close()


def send_aws_email(from_email: str, to_email: list, subject: str, message: str):
    # Send the email
    response = ses_client.send_email(
        Source=f'GitHub <{from_email}>',
        Destination={'ToAddresses': to_email},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Html': {'Data': message}}
        }
    )

    return response
