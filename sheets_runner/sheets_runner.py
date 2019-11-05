import pygsheets
from jira_requests.jira_requests import get_query_config_data
from response_parser.response_parser import map_data_to_sheets, map_tickets_to_sprints


def update_worksheet():
    sheets = map_data_to_sheets()
    for sheet in sheets:
        write_sheet(sheet)


def write_sheet(sheet):
    '''
    Authenticates the user, grabs the worksheet from the config file,
    writes data to the current working sheet, and creates a chart from the data.
    '''
    client = pygsheets.authorize()
    sheet_name = get_query_config_data()['worksheetName']
    worksheet = client.open(sheet_name)
    try:
        worksheet.add_worksheet(sheet.name)
    except:
        print(
            f'\n⚠️  Sheet already exists, updating sheet {sheet.name}. ⚠️')

    current_sheet = worksheet.worksheet_by_title(sheet.name)

    # TODO, update cells instead of clearing and rewriting
    current_sheet.clear()

    sheet_data = load_data_to_cell_objects(sheet)
    current_sheet.insert_rows(row=0, number=len(
        sheet_data) + 1, values=sheet_data)
    create_chart(current_sheet, sheet_data, sheet.chart_title)


def load_data_to_cell_objects(query):
    sheet_data = []
    sheet_data.append(query.headers)

    sprint_data = map_tickets_to_sprints(query)

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


def create_chart(worksheet, sheet_data, chart_title):
    sheet_data_length = len(sheet_data)
    sprint_cell_range = ('A2', f'A{sheet_data_length}')
    data_cell_range = [('D2', f'D{sheet_data_length}'),
                       ('E2', f'E{sheet_data_length}')]

    worksheet.add_chart(sprint_cell_range, data_cell_range,
                        chart_title, pygsheets.ChartType.LINE)
