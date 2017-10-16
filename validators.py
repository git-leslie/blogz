def validate_title(text):

    error = 0

    if not text:
        error = 'Add a freaking title'
    return error


def validate_body(body):

    error = 0

    if not body:
        error = "Omg geeze did you forget the body??"
    return error