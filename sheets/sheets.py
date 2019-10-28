import pygsheets
from jira_requests.config_utils import ConfigUtils
from response_parser.response_parser import ResponseParser


class Sheets:

    def update(self):
        response_parser = ResponseParser()
        sheets = response_parser.map_sheets_to_sheets()
        for sheet in sheets:
            self.write_sheet(sheet)

    def write_sheet(self, sheet):
        client = pygsheets.authorize()
        config_utils = ConfigUtils()
        sheet_name = config_utils.get_query_config_data()['worksheetName']

        worksheet = client.open(sheet_name)
        try:
            worksheet.add_worksheet(sheet.name)
        except:
            print(
                f'*** Sheet already exists, updating sheet {sheet.name}. ***')

        working_sheet = worksheet.worksheet_by_title(sheet.name)
        sheet_data = self.load_data_to_cell_objects(sheet)
        working_sheet.insert_rows(row=0, number=len(
            sheet_data) + 1, values=sheet_data)
        self.create_chart(working_sheet, sheet_data, sheet.chart_title)

    def load_data_to_cell_objects(self, query):
        sheet_data = []
        sheet_data.append(query.headers)

        response_parser = ResponseParser()
        sprint_data = response_parser.map_tickets_to_sprints(query)

        wow_formula = '=SUM(D2:D{index})/COUNT(D2:D{index})'

        index = 1
        for sprint in sprint_data:
            index += 1
            row_data = []
            row_data.append(sprint.name)
            row_data.append(sprint.start_date.split('T')[0])
            row_data.append(sprint.end_date.split('T')[0])
            row_data.append(len(sprint.Ticket))
            row_data.append(wow_formula.format(index=index))
            sheet_data.append(row_data)

        return sheet_data

    def create_chart(self, wks, sheet_data, chart_title):
        config_utils = ConfigUtils()
        sheet_data_length = len(sheet_data)
        sprint_range = ('A2', 'A{index}'.format(index=sheet_data_length))
        data_range = [('D2', 'D{index}'.format(
            index=sheet_data_length)),
            ('E2', 'E{index}'.format(index=sheet_data_length))]

        wks.add_chart(sprint_range, data_range,
                      chart_title, pygsheets.ChartType.LINE)
