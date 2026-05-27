def calculator_tool(query):

    try:

        result = eval(query)

        return str(result)

    except Exception:

        return "Invalid calculation."