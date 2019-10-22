import pygsheets
from jira_requests.request_utils import RequestUtils
from response_parser.response_parser import ResponseParser


class Sheets:

    def update(self):
        wks = self.get_worksheet()
        sheet_data = self.load_data_to_cell_objects()
        wks.insert_rows(row=0, number=len(sheet_data) + 1, values=sheet_data)

        request_utils = RequestUtils()
        sheet_data_length = len(sheet_data)
        header_range = ('A2', 'A{index}'.format(index=sheet_data_length))
        data_range = [('D2', 'D{index}'.format(
            index=sheet_data_length)),
            ('E2', 'E{index}'.format(index=sheet_data_length))]
        chart_header = request_utils.get_query_data()["chartName"]

        wks.add_chart(header_range, data_range,
                      chart_header, pygsheets.ChartType.LINE)

    def get_worksheet(self):
        gc = pygsheets.authorize()

        request_utils = RequestUtils()
        sheet_name = request_utils.get_query_data()["sheetName"]

        sh = gc.open(sheet_name)
        return sh.sheet1

    def get_headers(self):
        request_utils = RequestUtils()
        return request_utils.get_query_data(
        )["headers"]

    def load_data_to_cell_objects(self):
        sheet_data = []
        sheet_data.append(self.get_headers())

        response_parser = ResponseParser()
        sprint_data = response_parser.map_tickets_to_sprints()

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
