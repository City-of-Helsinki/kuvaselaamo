import logging


class ExtraDataFilter(logging.Filter):
    """This filter ensures that the log entry has a property named `data`
    so that our log formats may use that property without KeyErrors in
    case the log entries don't always add that specific key as an extra
    parameter."""
    def filter(self, record):
        if 'data' not in record.__dict__:
            record.__dict__['data'] = ''

        return True
