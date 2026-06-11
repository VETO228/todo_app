import pytest
import sqlite3
from database import check_user


def test_user_creation():
    assert check_user("admin", 123) == True
    assert check_user("vadim", 111) == True
    assert check_user("qwerty", 1) == False
    
test_user_creation()