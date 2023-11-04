import os

repository_owner = os.environ['GITHUB_REPOSITORY_OWNER']
repository = os.environ['GITHUB_REPOSITORY']
repository_name = repository.split('/')[1]
server_url = os.environ['GITHUB_SERVER_URL']

token = os.environ['INPUT_TOKEN']
project_number = int(os.environ['INPUT_PROJECT_NUMBER'])

api_endpoint = os.environ.get('INPUT_API_ENDPOINT')
if not api_endpoint:
    api_endpoint = os.environ['GITHUB_GRAPHQL_URL']

duedate_field_name = os.environ.get('INPUT_DUEDATE_FIELD_NAME')
if not duedate_field_name:
    duedate_field_name = 'Due Date'

notification_type = os.environ.get('INPUT_NOTIFICATION_TYPE')
if not notification_type:
    notification_type = 'comment'

if notification_type not in ['comment', 'aws_email']:
    raise Exception(f'Unsupported notification type {notification_type}')

email_from_address = os.environ.get('INPUT_EMAIL_FROM_ADDRESS')
