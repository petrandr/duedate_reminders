from pprint import pprint

import requests

import config
import utils
import graphql


def main():
    # project = graphql.get_project(
    #     project_number=config.inputs['project_number'],
    #     owner=config.repository_owner,
    #     repository=config.repository
    # )
    # print(project)
    issues = graphql.get_repo_issues(
        owner=config.repository_owner,
        repository=config.repository
    )
    pprint(issues)
    # utils.set_github_action_output('myOutput', my_output)


if __name__ == "__main__":
    main()
