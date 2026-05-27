from datetime import datetime


def time_tool(query=None):

    now = datetime.now()

    return now.strftime(
        "%Y-%m-%d %H:%M:%S"
    )