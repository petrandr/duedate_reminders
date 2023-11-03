import requests

import config


def get_project(project_number, owner, repository):
    # GraphQL query
    query = """
    query GetProject($project_number: Int!, $owner: String!, $repo: String!) {
        repository(owner: $owner, name: $repo) {
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
        'project_number': int(project_number),
        'owner': owner,
        'repo': repository
    }
    response = requests.post(
        config.inputs['api_endpoint'],
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {config.inputs['token']}"}
    )
    if response.json().get('errors'):
        print(response.json().get('errors'))

    return response.json().get('data').get('repository').get('projectV2')


def get_repo_issues(owner, repository, after=None, issues=[]):
    # GraphQL query
    query = """
    query GetRepoIssues($owner: String!, $repo: String!, $after: String) {
          repository(owner: $owner, name: $repo) {
            issues(first: 100, after: $after, states: [OPEN]) {
              nodes {
                title
                number
                assignees(first:100) {
                  nodes {
                    name
                    email
                  }
                }
                projectItems(first: 10) {
                  nodes {
                    project {
                      number
                      title
                    }
                    fieldValueByName(name: "Due Date") {
                      ... on ProjectV2ItemFieldDateValue {
                        id
                        date
                      }
                    }
                  }
                }
              }
              pageInfo {
                endCursor
                hasNextPage
                hasPreviousPage
              }
              totalCount
            }
          }
        }
    """

    variables = {
        'owner': owner,
        'repo': repository,
        'after': after
    }

    response = requests.post(
        config.inputs['api_endpoint'],
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {config.inputs['token']}"}
    )

    if response.json().get('errors'):
        print(response.json().get('errors'))

    pageinfo = response.json().get('data').get('repository').get('issues').get('pageInfo')
    issues = issues + response.json().get('data').get('repository').get('issues').get('nodes')
    if pageinfo.get('hasNextPage'):
        return get_repo_issues(owner=owner, repository=repository, after=pageinfo.get('endCursor'), issues=issues)

    return issues
