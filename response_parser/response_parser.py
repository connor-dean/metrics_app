from jira_requests.ticket_request import TicketRequest
from jira_requests.sprint_request import SprintRequest
from jira_requests.config_utils import ConfigUtils
from models.ticket import Ticket
from models.sprint import Sprint
from models.sheet import Sheet


class ResponseParser:

    def map_tickets_to_sprints(self, query):
        sprints = self.parse_response_to_sprints()
        tickets = self.parse_response_to_tickets(query)

        for sprint in sprints:
            start_date = sprint.start_date
            end_date = sprint.end_date

            for ticket in tickets:
                created_date = ticket.created_date
                if created_date > start_date and created_date < end_date:
                    sprint.Ticket.append(ticket)

        return sprints

    def parse_response_to_sprints(self):
        sprints = []

        sprint_request = SprintRequest()
        sprint_response = sprint_request.make_sprint_request()['values']
        for sprint in sprint_response:
            name = sprint['name']
            startDate = sprint['startDate'] if 'startDate' in sprint else 'N/A'
            endDate = sprint['endDate'] if 'endDate' in sprint else 'N/A'
            sprint = Sprint(name, startDate, endDate)
            sprints.append(sprint)
            import pprint
            pprint.pprint(vars(sprint))

        return sprints

    def parse_response_to_tickets(self, query):
        tickets = []

        ticket_request = TicketRequest()
        ticket_response = ticket_request.make_ticket_request(query)['issues']
        for ticket in ticket_response:
            issue = ticket['key']
            title = ticket['fields']['summary']
            labels = ticket['fields']['labels']
            created = ticket['fields']['created']
            ticket = Ticket(issue, title, labels, created)
            tickets.append(ticket)
            import pprint
            pprint.pprint(vars(ticket))

        return tickets

    #  TODO why are you so bad at naming
    def map_sheets_to_sheets(self):
        sheets = []

        config_utils = ConfigUtils()
        sheet_config = config_utils.get_query_config_data()['sheets']
        for sheet in sheet_config:
            name = sheet['sheetName']
            ticket_jql = sheet['ticketJql']
            chart_title = sheet['chartTitle']
            headers = sheet['headers']
            sheet = Sheet(name, ticket_jql, chart_title, headers)
            sheets.append(sheet)
            import pprint
            pprint.pprint(vars(sheet))

        return sheets
