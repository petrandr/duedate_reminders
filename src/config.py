import os

repository_owner = os.environ['GITHUB_REPOSITORY_OWNER']
repository = os.environ['GITHUB_REPOSITORY']
repository_name = repository.split('/')[1]
server_url = os.environ['GITHUB_SERVER_URL']

gh_token = os.environ['INPUT_GH_TOKEN']
project_number = int(os.environ['INPUT_PROJECT_NUMBER'])
api_endpoint = os.environ['GITHUB_GRAPHQL_URL']
duedate_field_name = os.environ['INPUT_DUEDATE_FIELD_NAME']
notification_type = os.environ['INPUT_NOTIFICATION_TYPE']

if notification_type not in ['comment', 'email']:
    raise Exception(f'Unsupported notification type {notification_type}')

if notification_type == 'email':
    smtp_server = os.environ['INPUT_SMTP_SERVER']
    smtp_port = os.environ['INPUT_SMTP_PORT']
    smtp_username = os.environ['INPUT_SMTP_USERNAME']
    smtp_password = os.environ['INPUT_SMTP_PASSWORD']
    smtp_from_email = os.environ['INPUT_SMTP_FROM_EMAIL']
