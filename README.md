# QA Metrics Application
QMA is a Python script that helps automate your defect and sub-defect reports. It accomplishes this by pulling from the Jira API and posting to the Google Sheets API to generate reports/charts on your week-over-week health.

After the inital setup, all you'll need to do afterwards is open the terminal, navigate to the root of the metrics_app directory and run `python3 main.py`.

## Setup
### Config Files
In order to access the APIs, you'll need to add a couple of config files containing those keys along with some information for:
- What JQL query you want to run
- What you want your chart headers to look like

You'll need to add a folder at the root of your directory called `configs`, with the two files:
- query_config.json
- user_config.json

#### query_config.json
```
{
    "ticketApi": "<jira_api_endpoint>",
    "projectNum": "<project_number>",
    "worksheetName": "Metrics App",
    "sheetName": "External Quality",
    "sheets": [
        {
            "sheetName": "External Quality",
            "ticketJql": "project = <project_name> AND issuetype = Defect ORDER BY created DESC",
            "chartTitle": "External Quality (Defects in Production)",
            "headers": [
                "Sprint #",
                "Start Date",
                "End Date",
                "Defects",
                "WoW Trend"
            ]
        },
        {
            "sheetName": "Internal Quality",
            "ticketJql": "project = <project_name> AND issuetype = Sub-Defect ORDER BY created DESC",
            "chartTitle": "Internal Quality (Defects while Testing)",
            "headers": [
                "Sprint #",
                "Start Date",
                "End Date",
                "Sub Defects",
                "WoW Trend"
            ]
        }
    ]
}
```

#### user_config.json
```
{
    "username": "<jira_username>",
    "authToken": "<jira_auth_token>"
}
```

### Jira API Key
In order to make requests to Jira Cloud, you'll need an API key.

Instructions on how to get the key can be found here: https://confluence.atlassian.com/cloud/api-tokens-938839638.html

Once you retrieve the key, you'll need to add your credentials to the `user_config.json` file you created in your `configs` folder.

The two fields you'll need to add are `username`, which is the email you use to login to Jira Cloud, and `authToken`, which is the API token you obtained through the instructions above.

### Google Sheets API Key

This part of the process takes several steps. In order to post data to a Google Sheet, you'll need to create a new project in the Google Developer console and enable OAuth authentication for the project. Information on the process can be found here: https://developers.google.com/sheets/api/guides/authorizing#APIKey

Once you finish creating the OAuth authentication, you'll be prompted to download a `client_secret.json` file. After downloading, you'll need to make sure the file is named `client_secret.json` and place it at the root of the `metrics_app` directory.

After running the project for the first time, you'll see some prompts in the terminal to enable several Google APIs. Follow the instructions in the terminal in order to complete these. This might take several minutes to take effect.
