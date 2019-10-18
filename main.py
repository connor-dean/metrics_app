from parser_test.parser_test import Parser
from jira_requests.sprint_request import SprintRequest

if __name__ == '__main__':
    parser = Parser()
    parser.parse_issues_to_tickets()

    # request = SprintRequest()
    # request.make_sprint_request()