from response_parser.response_parser import ResponseParser
from jira_requests.sprint_request import SprintRequest

if __name__ == '__main__':
    parser = ResponseParser()
    parser.map_tickets_to_sprints()
