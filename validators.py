def validate_title(text):

    error = 0

    if not text:
        error = 'You forgot a title'
    return error


def validate_body(body):

    error = 0

    if not body:
        error = "This blog is empty!"
    return error

'''
def blank_post(text):
    
    if not text:
        return True
    
    return False'''