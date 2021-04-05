# content of test_sysexit.py
import pytest
import liblo


def f():
    target = liblo.Address('bad')


def test_mytest():
    with pytest.raises(liblo.AddressError):
        f()
