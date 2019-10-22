from jira_requests.ticket_request import TicketRequest
from jira_requests.sprint_request import SprintRequest
from models.ticket import Ticket
from models.sprint import Sprint


class ResponseParser:

    def map_tickets_to_sprints(self):
        sprints = self.parse_response_to_sprints()
        tickets = self.parse_response_to_tickets()

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

        sprint_response = self.parse_sprint_response()["values"]
        for sprint in sprint_response:
            name = sprint["name"]
            startDate = sprint["startDate"] if "startDate" in sprint else "N/A"
            endDate = sprint["endDate"] if "endDate" in sprint else "N/A"
            sprint = Sprint(name, startDate, endDate)
            sprints.append(sprint)

        return sprints

    def parse_sprint_response(self):
        sprint_request = SprintRequest()
        response = sprint_request.make_sprint_request()
        return response

    def parse_response_to_tickets(self):
        tickets = []

        ticket_response = self.parse_ticket_response()
        for ticket in ticket_response:
            issue = ticket["key"]
            title = ticket["fields"]["summary"]
            labels = ticket["fields"]["labels"]
            created = ticket["fields"]["created"]

            ticket = Ticket(issue, title, labels, created)
            tickets.append(ticket)

        return tickets

    def parse_ticket_response(self):
        ticket_request = TicketRequest()
        response = ticket_request.make_ticket_request()
        return response["issues"]
