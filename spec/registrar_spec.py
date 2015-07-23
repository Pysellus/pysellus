from expects import expect, equal
from doublex_expects import *
from doublex import Spy, Mock

from pysellus import registrar
from pysellus.registrar import expect as expect_

with description('the registrar module'):
    with it('should call every function passed to it'):
        spy = Spy()
        function_list = [
            spy.a_function,
            spy.another_function
        ]
        registrar.register(function_list)

        for function in function_list:
            expect(function).to(have_been_called.once)

    with it('should add a function list to the dictionary of streams to functions'):
        spy = Spy()
        stream = Mock()
        function_list = [
            spy.a_function,
            spy.another_function
        ]

        expect_(stream)(*function_list)

        for function in function_list:
            expect(function).to_not(have_been_called.once)

        expect(registrar.stream_to_observers[stream]).to(equal(function_list))