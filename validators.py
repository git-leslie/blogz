def validate_title(text):

    error = 0

    if text == "":
        error = 'You forgot a title'
    return error


def validate_body(body):

    error = 0

    if body == '':
        error = "This blog is empty!"
    return error


'''def is_blank(text):
    
    if not text:
        return True
    
    return False'''