def iter_except(function, exception):
    """Iter-like that stops on exception."""
    try:
        while True:
            yield function()
    except exception:
        return

