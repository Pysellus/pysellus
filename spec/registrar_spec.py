from doublex import Spy, Mock
from expects import expect, equal
from doublex_expects import have_been_called

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

    with it('should merge n function lists if applied to the same stream'):
        spy = Spy()
        stream = Mock()

        first_function_list = [
            spy.first_function,
            spy.second_function
        ]

        second_function_list = [
            spy.third_function,
            spy.fourth_function
        ]

        expect_(stream)(*first_function_list)
        expect_(stream)(*second_function_list)

        expect(registrar.stream_to_observers[stream]).to(equal(first_function_list +
                                                               second_function_list))
