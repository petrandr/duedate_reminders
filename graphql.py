import requests
import config


def get_repo_issues(owner, repository, duedate_field_name, after=None, issues=None):
    query = """
    query GetRepoIssues($owner: String!, $repo: String!, $duedate: String!, $after: String) {
          repository(owner: $owner, name: $repo) {
            issues(first: 100, after: $after, states: [OPEN]) {
              nodes {
                id
                title
                number
                assignees(first:100) {
                  nodes {
                    name
                    email
                    login
                  }
                }
                projectItems(first: 10) {
                  nodes {
                    project {
                      number
                      title
                    }
                    fieldValueByName(name: $duedate) {
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
        'duedate': duedate_field_name,
        'after': after
    }

    response = requests.post(
        config.api_endpoint,
        json={"query": query, "variables": variables},
        headers={"Authorization": f"Bearer {config.token}"}
    )

    if response.json().get('errors'):
        print(response.json().get('errors'))

    pageinfo = response.json().get('data').get('repository').get('issues').get('pageInfo')
    if issues is None:
        issues = []
    issues = issues + response.json().get('data').get('repository').get('issues').get('nodes')
    if pageinfo.get('hasNextPage'):
        return get_repo_issues(owner=owner, repository=repository, after=pageinfo.get('endCursor'), issues=issues)

    return issues


def add_issue_comment(issueId, comment):
    mutation = """
    mutation AddIssueComment($issueId: ID!, $comment: String!) {
        addComment(input: {subjectId: $issueId, body: $comment}) {
            clientMutationId
        }
    }
    """

    variables = {
        'issueId': issueId,
        'comment': comment
    }
    response = requests.post(
        config.api_endpoint,
        json={"query": mutation, "variables": variables},
        headers={"Authorization": f"Bearer {config.token}"}
    )
    if response.json().get('errors'):
        print(response.json().get('errors'))

    return response.json().get('data')
