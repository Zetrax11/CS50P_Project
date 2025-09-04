import pytest
import builtins
import getpass
import os
from project import log_in, save_file, load_expenses

sample_expense = [
    {
        "Kwota": 200.0,
        "Miesiąc": "Styczeń",
        "Kategoria": "Jedzenie"},
    {
        "Kwota": 100.0,
        "Miesiąc": "Maj",
        "Kategoria": "Jedzenie"
    }
        ]

def test_log_in(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "kamil")
    monkeypatch.setattr(getpass, "getpass", lambda: "Password1")
    assert log_in() == "kamil"

    monkeypatch.setattr(builtins, "input", lambda _: "test")
    monkeypatch.setattr(getpass, "getpass", lambda: "Password3")
    assert log_in() == "test"
    
    usernames = iter(["test", "test", "test"])
    passwords = iter(["pass", "", "Password3"])
    monkeypatch.setattr(builtins, "input", lambda _: next(usernames))
    monkeypatch.setattr(getpass, "getpass", lambda: next(passwords))
    assert log_in() == "test"

    for _ in range(3):
        monkeypatch.setattr(builtins, "input", lambda _: "kamil")
        monkeypatch.setattr(getpass, "getpass", lambda: "Password2")
    assert log_in() == False

    usernames = iter(["test", "test", "test"])
    passwords = iter(["pass", "", "Password2"])
    monkeypatch.setattr(builtins, "input", lambda _: next(usernames))
    monkeypatch.setattr(getpass, "getpass", lambda: next(passwords))
    assert log_in() == False

def test_save_file():
    sample_path = "test_path.json"
    save_file(sample_path, sample_expense)
    assert os.path.isfile(sample_path) == True

def test_load_expenses():
    assert load_expenses("test_path.json") == sample_expense

    assert load_expenses("test1_path.json") == []