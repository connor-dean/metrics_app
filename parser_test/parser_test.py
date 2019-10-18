from jira_requests.defect_request import DefectRequest
from jira_requests.sprint_request import SprintRequest
from models.ticket import Ticket
import json
from pprint import pprint

class Parser:

    def parse_sprint_response(self):
        sprint_request = SprintRequest()
        response = sprint_request.make_sprint_request()
        return response

    def parse_issues_to_tickets(self):
        tickets = [Ticket]

        for issues in self.parse_issues_response():
            issue = issues["key"]
            title = issues["fields"]["summary"]
            labels = issues["fields"]["labels"]
            created = issues["fields"]["created"]
            
            ticket = Ticket(issue, title, labels, created)

            pprint(vars(ticket))

            tickets.append(ticket)

        return tickets

    def parse_issues_response(self):
        defect_request = DefectRequest()
        response = defect_request.make_defect_request()
        return response["issues"]
