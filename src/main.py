from datetime import datetime, timedelta
import logging as logger
import config
import utils
import graphql

# Set LogLevel
logger.basicConfig(level=print)


def prepare_comment(issue: dict, assignees: dict, duedate: datetime):
    """
    Prepare the comment from the given arguments and return it
    """

    comment = ''
    if assignees:
        for assignee in assignees:
            comment += f'@{assignee["login"]} '
    else:
        print(f'No assignees found for issue #{issue["number"]}')

    comment += f'The issue is due on: {duedate.strftime("%b %d, %Y")}'
    print(f'Issue #{duedate} | {comment}')

    return comment


def prepare_email_message(issue, assignees, duedate):
    """
    Prepare the email message, subject and mail_to addresses
    """

    subject = f'DUE SOON | #{issue["number"]} {issue["title"]}'
    _assignees = ''
    mail_to = []
    if assignees:
        for assignee in assignees:
            _assignees += f'@{assignee["name"]} '
            mail_to.append(assignee['email'])
    else:
        print(f'No assignees found for issue #{issue["number"]}')

    message = f'Assignees: {_assignees}' \
              f'<br>The issue is due on: {duedate.strftime("%b %d, %Y")}' \
              f'<br><br>{config.server_url}/{config.repository}/issues/{issue["number"]}'

    return [subject, message, mail_to]


def main():
    # Get the issues
    issues = graphql.get_repo_issues(
        owner=config.repository_owner,
        repository=config.repository_name,
        duedate_field_name=config.duedate_field_name
    )

    # Check if there are issues available
    if not issues:
        print('No issues has been found')
        return

    # Get the date for tomorrow
    tomorrow = datetime.now().date() + timedelta(days=1)

    # Loop through issues
    for issue in issues:
        projectNodes = issue['projectItems']['nodes']

        # If no project is assigned to the
        if not projectNodes:
            continue

        # Check if the desire project is assigned to the issue
        project = next((entry for entry in projectNodes if entry['project']['number'] == config.project_number), None)

        # The fieldValueByName contains the date for the DueDate Field
        if not project['fieldValueByName']:
            continue

        # Get the duedate value and convert it to date object
        duedate = project["fieldValueByName"]["date"]
        duedate_obj = datetime.strptime(duedate, "%Y-%m-%d").date()

        # Check if the project item is due soon or not
        if duedate_obj != tomorrow:
            continue

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        # Handle notification type
        if config.notification_type == 'comment':
            # Prepare the notification content
            comment = prepare_comment(
                issue=issue,
                assignees=assignees,
                duedate=tomorrow
            )
            # Add the comment to the issue
            graphql.add_issue_comment(issue['id'], comment)
        elif config.notification_type == 'aws_email':
            # Prepare the email content
            subject, message, to = prepare_email_message(
                issue=issue,
                assignees=assignees,
                duedate=tomorrow
            )

            # Send the email
            utils.send_aws_email(
                from_email=config.email_from_address,
                to_email=to,
                subject=subject,
                message=message
            )


if __name__ == "__main__":
    main()
