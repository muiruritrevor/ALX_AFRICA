def instagram_login(username, password):
    """
    This function log in a user 
    into their instagram.com account
    """
    if username == "revy" and password == "enterpass":
        response = "success"
    else:
        response = "failure"

    return response

result = instagram_login("revy", "enterpass")
print(result)

