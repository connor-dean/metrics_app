import gspread
from oauth2client.service_account import ServiceAccountCredentials
from response_parser.response_parser import ResponseParser
from jira_requests.request_utils import RequestUtils


class Sheets:

    def update(self):
        sheet = self.get_sheet_info()

        sheet_data = self.load_data_to_cell_objects(sheet)

        # TODO see if we can genericize this in the config file
        wow_formula = '=SUM(D2:D{index})/COUNT(D2:D{index})'

        row_index = 1
        while row_index - 1 < len(sheet_data):
            print('Writing to sheet ...') if row_index == 1 else print(
                sheet_data[row_index - 1])

            sheet.insert_row(sheet_data[row_index - 1], row_index)

            # Appending formulas to a Cell object will return it with a prepended
            # ', which results in the sheet not reading the formula
            if row_index > 1:
                sheet.update_cell(
                    row_index, 5, wow_formula.format(index=row_index))

            row_index += 1

        print('The sheet has been updated successfully.')

    def get_sheet_info(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'credentials.json', scope)
        client = gspread.authorize(creds)

        request_utils = RequestUtils()
        sheet_name = request_utils.get_query_data()["sheetName"]

        return client.open(sheet_name).sheet1

    def load_data_to_cell_objects(self, sheet):
        sheet_data = []
        sheet_data.append(self.get_headers(sheet))

        response_parser = ResponseParser()
        sprint_data = response_parser.map_tickets_to_sprints()

        index = 1
        for sprint in sprint_data:
            index += 1
            row_data = []
            row_data.append(sprint.name)
            row_data.append(sprint.start_date.split('T')[0])
            row_data.append(sprint.end_date.split('T')[0])
            row_data.append(len(sprint.Ticket))
            sheet_data.append(row_data)

        return sheet_data

    def get_headers(self, sheet):
        request_utils = RequestUtils()
        return request_utils.get_query_data(
        )["headers"]
