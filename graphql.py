import requests


def get_project(project_number):
    # GraphQL query
    query = """
    query GetProject($project_number: Int!) {
        repository(owner: "petrandr", name: "requests") {
            projectV2(number: $project_number) {
                id
                fields(first: 20) {
                    nodes {
                      ... on ProjectV2Field {
                        id
                        name
                      }
                      ... on ProjectV2SingleSelectField {
                        id
                        name
                        options {
                          id
                          name
                        }
                      }
                    }
                  }
            }
        }
    }
    """

    variables = {
        'project_number': project_number
    }
    response = requests.post(
        'https://api.github.com/graphql',
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {github_token}"}
    )
    return response.json().get('data').get('repository').get('projectV2')