import gspread
from oauth2client.service_account import ServiceAccountCredentials
from response_parser.response_parser import ResponseParser


class Sheets:

    def update(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'credentials.json', scope)
        client = gspread.authorize(creds)

        sheet = client.open('Metrics App').sheet1

        response_parser = ResponseParser()
        sprint_data = response_parser.map_tickets_to_sprints()

        sheet_data = []
        for sprint in sprint_data:
            row_data = []
            row_data.append(sprint.name)
            row_data.append(sprint.start_date)
            row_data.append(sprint.end_date)
            row_data.append(len(sprint.Ticket))
            sheet_data.append(row_data)

        row_count = 1
        while row_count < len(sheet_data):
            sheet.insert_row(sheet_data[row_count], row_count)
            row_count += 1
