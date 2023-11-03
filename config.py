import os

repository_owner = os.environ['GITHUB_REPOSITORY_OWNER']
repository = os.environ['GITHUB_REPOSITORY'].split('/')[1]
env = 'local' if os.environ.get('ENV') == 'local' else 'prod'
inputs = {}

for key, value in os.environ.items():
    if key.startswith('INPUT'):
        inputs[key[len('INPUT_'):].lower()] = value

if not inputs.get('api_endpoint'):
    inputs['api_endpoint'] = 'https://api.github.com/graphql'

