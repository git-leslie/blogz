def validate_title(text):
    error = 0
    if not text:
        error = 'Add a freaking title!'
    return error


def validate_body(body):
    error = 0
    if not body:
        error = "Omg geeze did you forget the body??"
    return error



def validate_gen(text):
    error = 0
    if " " in text or len(text) < 3 or len(text) > 20 or text == "":
        error = "Username and password must be between 3-20 characters, without spaces"
    return error


def validate_verify_pw(password, verify_pw):
    error = 0
    if password != verify_pw:
        error = "Passwords do not match"
    return error