from datetime import datetime, timedelta
from logger import logger
import config
import utils
import graphql


def notify_expiring_issues():
    if config.is_enterprise:
        # Get the issues
        issues = graphql.get_project_issues(
            owner=config.repository_owner,
            owner_type=config.repository_owner_type,
            project_number=config.project_number,
            duedate_field_name=config.duedate_field_name,
            filters={'open_only': True}
        )
    else:
        # Get the issues
        issues = graphql.get_repo_issues(
            owner=config.repository_owner,
            repository=config.repository_name,
            duedate_field_name=config.duedate_field_name
        )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    # Get the date for tomorrow
    tomorrow = datetime.now().date() + timedelta(days=1)

    # Loop through issues
    for issue in issues:
        if config.is_enterprise:
            projectItem = issue
            issue = issue['content']
        else:
            projectNodes = issue['projectItems']['nodes']

            # If no project is assigned to the
            if not projectNodes:
                continue

            # Check if the desire project is assigned to the issue
            projectItem = next((entry for entry in projectNodes if entry['project']['number'] == config.project_number),
                               None)

        # The fieldValueByName contains the date for the DueDate Field
        if not projectItem['fieldValueByName']:
            continue

        # Get the duedate value and convert it to date object
        duedate = projectItem["fieldValueByName"]["date"]
        duedate_obj = datetime.strptime(duedate, "%Y-%m-%d").date()

        # Check if the project item is due soon or not
        if duedate_obj != tomorrow:
            continue

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        # Handle notification type
        if config.notification_type == 'comment':
            # Prepare the notification content
            comment = utils.prepare_expiring_issue_comment(
                issue=issue,
                assignees=assignees,
                duedate=tomorrow
            )

            if not config.dry_run:
                # Add the comment to the issue
                graphql.add_issue_comment(issue['id'], comment)

            logger.info(f'Comment added to issue #{issue["number"]} ({issue["id"]}) with due date on {tomorrow}')
        elif config.notification_type == 'email':
            # Prepare the email content
            subject, message, to = utils.prepare_expiring_issue_email_message(
                issue=issue,
                assignees=assignees,
                duedate=tomorrow
            )

            if not config.dry_run:
                # Send the email
                utils.send_email(
                    from_email=config.smtp_from_email,
                    to_email=to,
                    subject=subject,
                    html_body=message
                )

            logger.info(f'Email sent to {to} for issue #{issue["number"]} with due date on {tomorrow}')


def notify_missing_duedate():
    issues = graphql.get_project_issues(
        owner=config.repository_owner,
        owner_type=config.repository_owner_type,
        project_number=config.project_number,
        duedate_field_name=config.duedate_field_name,
        filters={'empty_duedate': True, 'open_only': True}
    )

    # Check if there are issues available
    if not issues:
        logger.info('No issues has been found')
        return

    for projectItem in issues:
        # if projectItem['id'] != 'MDEzOlByb2plY3RWMkl0ZW0xMzMxOA==':
        #     continue
        issue = projectItem['content']

        # Get the list of assignees
        assignees = issue['assignees']['nodes']

        if config.notification_type == 'comment':
            # Prepare the notification content
            comment = utils.prepare_missing_duedate_comment(
                issue=issue,
                assignees=assignees,
            )

            if not config.dry_run:
                # Add the comment to the issue
                graphql.add_issue_comment(issue['id'], comment)

            logger.info(f'Comment added to issue #{issue["number"]} ({issue["id"]})')
        elif config.notification_type == 'email':
            # Prepare the email content
            subject, message, to = utils.prepare_missing_duedate_email_message(
                issue=issue,
                assignees=assignees
            )

            if not config.dry_run:
                # Send the email
                utils.send_email(
                    from_email=config.smtp_from_email,
                    to_email=to,
                    subject=subject,
                    html_body=message
                )
            logger.info(f'Email sent to {to} for issue #{issue["number"]}')


def main():
    logger.info('Process started...')
    if config.dry_run:
        logger.info('DRY RUN MODE ON!')

    if config.notify_for == 'expiring_issues':
        notify_expiring_issues()
    elif config.notify_for == 'missing_duedate':
        notify_missing_duedate()
    else:
        raise Exception('Unsupported value for argument \'notify_for\'')


if __name__ == "__main__":
    main()
