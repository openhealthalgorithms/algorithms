def format_params(params):
    return {
        key: float(value) if type(value) is int else value
        for key, value in params.items()
    }
