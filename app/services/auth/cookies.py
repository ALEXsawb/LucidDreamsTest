from fastapi import Response


def set_access_token_in_cookies(response: Response, access_token: str, expire_in_minute: int) -> None:
    response.set_cookie('access_token', access_token, expire_in_minute * 60, expire_in_minute * 60,
                        '/', None, False, True, 'lax')


def set_logged_in_cookies(response: Response, expire_in_minute: int) -> None:
    response.set_cookie('logged_in', 'True', expire_in_minute * 60, expire_in_minute * 60,
                        '/', None, False, False, 'lax')

