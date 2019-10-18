from .ticket import Ticket


class Sprint:

    def __init__(self, name, start_date, end_date, Ticket=[]):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.Ticket = []
