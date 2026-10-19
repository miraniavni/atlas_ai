from db import check_connection


def test_check_connection():
    assert check_connection() == 1