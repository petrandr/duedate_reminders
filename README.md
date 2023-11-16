# Issue Due Date Notifications

GitHub doesn't provide a built-in way to set due dates for issues and receive notifications before they are due. This
GitHub Action aims to address that by allowing you to manage due dates for issues within a central GitHub project.

## Table of Contents

- [Introduction](#introduction)
- [Custom Field Setup](#custom-field-setup)
- [Usage](#usage)
    - [Prerequisites](#prerequisites)
    - [Inputs](#inputs)
    - [Examples](#examples)
      - [Expiring Issues With Comment](#expiring-issues-with-comment)
      - [Expiring Issues With Email](#expiring-issues-with-email)
      - [Missing Due Date With Comment](#missing-due-date-with-comment)
      - [Missing Due Date With Email](#missing-due-date-with-email)

## Introduction

This GitHub Action allows you to manage due dates for issues in a central GitHub project. It integrates with a custom
date field (due date) that you can add to your GitHub project board. By using this action to your project's issues,
you can start receiving notifications: 
1. (n) Days before the Due Date. The number of Days before `(n)` depends on you
2. when the Due Date field is not provided to the project item

There are two ways to send notifications:
1. With comments: Everyone which is subscribed to the issue will receive email notification when comment is placed.
2. With emails: Assignees will receive email directly from the action. 


## Custom Field Setup

To set up the custom date field (due date) in your GitHub project board:

1. Go to your GitHub projects tab.
2. Click on "New project" and then click "Create".
3. Click on `+` icon to add new field, then click on `+ New field`
4. Add a custom field with the name "Due Date" and the field type as "Date.", then click `Save`.

## Usage

### Prerequisites

Before you can start using this GitHub Action, you'll need to ensure you have the following:

1. A GitHub repository where you want to enable this action.
2. A GitHub project board with a custom date field (due date) added.
3. A Token (Classic) with permissions to repo:*, read:user, user:email, read:project

### Inputs

| Input                                | Description                                                                                      |
|--------------------------------------|--------------------------------------------------------------------------------------------------|
| `gh_token`                           | The GitHub Token                                                                                 |
| `project_number`                     | The project number                                                                               |
| `notify_for`                         | The type of the notification (expiring_issues or missing_duedate) are about to sent. Default is `expiring_issues` |
| `duedate_field_name` _(optional)_    | THe duedate field name. The default is `Due Date`                                                |
| `notification_type` _(optional)_     | The notification type. Available values are `comment` and `email`. Default is `comment`          |
| `enterprise_github` _(optional)_     | `True` if you are using enterprise github and false if not. Default is `False`                   |
| `repository_owner_type` _(optional)_ | The type of the repository owner (oragnization or user). Default is `user`                       |
| `smtp_server` _(optional)_           | The mail server address. `Required` only when `notification_type` is set to `email`              |
| `smtp_port` _(optional)_             | The mail server port. `Required` only when `notification_type` is set to `email`                 |
| `smtp_username` _(optional)_         | The mail server username. `Required` only when `notification_type` is set to `email`             |
| `smtp_password` _(optional)_         | The mail server password. `Required` only when `notification_type` is set to `email`             |
| `smtp_from_email` _(optional)_       | The mail from email address. `Required` only when `notification_type` is set to `email`          |
| `dry_run` _(optional)_               | `True` if you want to enable dry-run mode. Default is `False`                                    |

### Examples

#### Expiring Issues With Comment
To set up due date comment notifications, you'll need to create or update a GitHub Actions workflow in your repository. Below is
an example of a workflow YAML file:

```yaml
name: 'Check Issues Due Date'

on:
  schedule:
    - cron: '0 1 * * *'

jobs:
  reminder:
    runs-on: ubuntu-latest
    steps:
      - name: Check duedate and write a comment
        uses: petrandr/duedate_reminders@latest
        with:
          gh_token: ${{ secrets.GITHUB_TOKEN }}
          project_number: 2
          notify_for: "expiring_issues"
          duedate_field_name: "Due Date"
          notification_type: "comment"
```

#### Expiring Issues With Email
To set up due date email notifications, you'll need to create or update a GitHub Actions workflow in your repository. Below is
an example of a workflow YAML file:

```yaml
name: 'Check Issues Due Date'

on:
  schedule:
    - cron: '0 1 * * *'

jobs:
  reminder:
    runs-on: ubuntu-latest
    steps:
      - name: Check duedate and send email to assignees
        uses: petrandr/duedate_reminders@latest
        with:
          gh_token: ${{ secrets.GITHUB_TOKEN }}
          project_number: 2
          notify_for: "expiring_issues"
          duedate_field_name: "Due Date"
          notification_type: "email"
          smtp_server: smtp.example.com
          smtp_port: 587
          smtp_username: ${{secrets.SMTP_USERNAME}}
          smtp_password: ${{secrets.SMTP_PASSWORD}}
          smtp_from_email: github@example.com
```

#### Missing Due Date With Comment
To set up comment notifications for a missing due date value, you'll need to create or update a GitHub Actions workflow in your repository. Below is
an example of a workflow YAML file:

```yaml
name: 'Check for missing Due Dates'

on:
  schedule:
    - cron: '0 1 * * *'

jobs:
  reminder:
    runs-on: ubuntu-latest
    steps:
      - name: Check for missing due dates and write a comment
        uses: petrandr/duedate_reminders@latest
        with:
          gh_token: ${{ secrets.GITHUB_TOKEN }}
          project_number: 2
          notify_for: "missing_duedate"
          duedate_field_name: "Due Date"
          notification_type: "comment"
```

#### Missing Due Date With Email
To set up email notifications for a missing due date value, you'll need to create or update a GitHub Actions workflow in your repository. Below is
an example of a workflow YAML file:

```yaml
name: 'Check for missing Due Dates'

on:
  schedule:
    - cron: '0 1 * * *'

jobs:
  reminder:
    runs-on: ubuntu-latest
    steps:
      - name: Check for missing due dates and send email to assignees
        uses: petrandr/duedate_reminders@latest
        with:
          gh_token: ${{ secrets.GITHUB_TOKEN }}
          project_number: 2
          notify_for: "missing_duedate"
          duedate_field_name: "Due Date"
          notification_type: "email"
          smtp_server: smtp.example.com
          smtp_port: 587
          smtp_username: ${{secrets.SMTP_USERNAME}}
          smtp_password: ${{secrets.SMTP_PASSWORD}}
          smtp_from_email: github@example.com
```