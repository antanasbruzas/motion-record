# content of test_sysexit.py
import pytest


def f():
    target = liblo.Address('bad')


def test_mytest():
    with pytest.raises(AddressError):
        f()
