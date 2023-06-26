"""This module contains the main Seems API."""
import inspect
import traceback
import types
import unittest

import seems.domains as domains

from typing import Callable, List

SEEMS_TESTS = []

def _Tests():
    """Returns the list of unit tests to run."""
    return SEEMS_TESTS

# Since unit tests are declared as decorators above functions, we need to
# rewrite assertion failures to highlight the correct line number.
def _rewrite_tb(func):
    # This is nested 4 levels deep, so we need to go three levels up the stack.
    # The stack looks like this:
    #
    # 0: _rewrite_tb()
    # 1: Nested Unittest.TestCase class test() function declaration.
    # 2: CreateTestCase() function.
    # 3: @Seems decorator.
    # 4: User's function declaration.
    #
    # We get the traceback by raising an exception and then catching it, since
    # we can't create frame objects directly.
    try:
        raise NotImplementedError()
    except NotImplementedError as e:
        # Get the stack frame of the caller of the decorator.
        caller_stack = e.__traceback__.tb_frame.f_back.f_back.f_back.f_back
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AssertionError as test_failure_error:
            # Create a new single-element traceback using the caller's stack frame.
            # This will make the error appear to come from the line where the
            # decorator was applied, rather than the line where the unit test
            # failed.
            test_failure_error.__traceback__ = types.TracebackType(
                tb_next=None,
                tb_frame=caller_stack,
                tb_lasti=caller_stack.f_lasti,
                tb_lineno=caller_stack.f_lineno
            )
            raise test_failure_error
    return wrapper

class IntegerReturnValueTest(unittest.TestCase):
    def __init__(self, func: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.func = func
    
    @_rewrite_tb
    def test(self):
        for i in domains.INTEGERS:
            result = self.func(i)
            self.assertIsInstance(result, int)

def CreateTestCase(test_name: str, func: Callable, verifier: Callable, domain: List) -> unittest.TestCase:
    # Create a new unittest test case that calls function func on each element
    # of domain.
    class Test(unittest.TestCase):
        @_rewrite_tb
        def test(self):
            for i in domain:
                result = func(i)
                if not verifier(i, result):
                    self.fail(f"Test {test_name} Failed on input {i}.")
    Test.__name__ = test_name
    Test.__qualname__ = test_name
    return Test

class ReturnValue(object):
    @staticmethod
    def IsEven(func: Callable, **kwargs) -> bool:
        """Creates a unit test for the given function.

        Implemented as a decorator. Generates a unit test and then returns the
        function unchanged.

        Optionally, a custom test domain can be provided 
        via the `domain` keyword argument. The default will use
        domains.DomainFromType(), defined in domains.py.
        """
        if 'domain' in kwargs:
            domain = kwargs['domain']
        else:
            domain = domains.INTEGERS
        test_case = CreateTestCase(f'IsEven {func.__name__}', func, lambda x, y: y % 2 == 0, domain)
        # Add the test case to the list of tests to run. Use the original function's name.
        #Test.__name__ = func.__name__
        SEEMS_TESTS.append(test_case)
        return func
    
    @staticmethod
    def IsInteger(func: Callable, **kwargs) -> bool:
        """Creates a unit test for the given function.

        Implemented as a decorator. Generates a unit test and then returns the
        function unchanged.

        Optionally, a custom test domain can be provided 
        via the `domain` keyword argument. The default will use
        domains.DomainFromType(), defined in domains.py.
        """
        if 'domain' in kwargs:
            domain = kwargs['domain']
        else:
            domain = domains.INTEGERS
        test_case = CreateTestCase(f'IsInteger {func.__name__}', func, lambda x, y: isinstance(y, int), domain)
        # Add the test case to the list of tests to run. Use the original function's name.
        #Test.__name__ = func.__name__
        SEEMS_TESTS.append(test_case)
        return func
        