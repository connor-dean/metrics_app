import pprint
from jira_requests.jira_requests import make_ticket_request, make_sprint_request, get_query_config_data
from models.ticket import Ticket
from models.sprint import Sprint
from models.sheet import Sheet


def map_data_to_sheets():
    print('\n📈 Grabbing chart info 📉')

    sheets = []

    sheet_config = get_query_config_data()['sheets']
    for sheet in sheet_config:
        name = sheet['sheetName']
        ticket_jql = sheet['ticketJql']
        chart_title = sheet['chartTitle']
        headers = sheet['headers']
        sheet = Sheet(name, ticket_jql, chart_title, headers)
        sheets.append(sheet)
        pprint.pprint(vars(sheet))

    return sheets


def map_tickets_to_sprints(query):
    sprints = parse_response_to_sprints()
    tickets = parse_response_to_tickets(query)

    for sprint in sprints:
        start_date = sprint.start_date
        end_date = sprint.end_date

        for ticket in tickets:
            created_date = ticket.created_date
            if created_date > start_date and created_date < end_date:
                sprint.Ticket.append(ticket)

    return sprints


def parse_response_to_sprints():
    print('\n🏃 Grabbing sprint info 🏃')

    sprints = []

    sprint_response = make_sprint_request()['values']
    for sprint in sprint_response:
        name = sprint['name']
        startDate = sprint['startDate'] if 'startDate' in sprint else 'N/A'
        endDate = sprint['endDate'] if 'endDate' in sprint else 'N/A'
        sprint = Sprint(name, startDate, endDate)
        sprints.append(sprint)
        pprint.pprint(vars(sprint))

    return sprints


def parse_response_to_tickets(query):
    print('\n🎟  Grabbing ticket info 🎟')

    tickets = []

    ticket_response = make_ticket_request(query)['issues']
    for ticket in ticket_response:
        issue = ticket['key']
        title = ticket['fields']['summary']
        labels = ticket['fields']['labels']
        created = ticket['fields']['created']
        ticket = Ticket(issue, title, labels, created)
        tickets.append(ticket)
        pprint.pprint(vars(ticket))

    return tickets
