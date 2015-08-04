from doublex import Spy, Mock
from expects import expect, equal
from doublex_expects import have_been_called

from pysellus import registrar
from pysellus.registrar import expect as expect_

with description('the registrar module'):
    with it('should call every function passed to it'):
        function_list = [
            Spy().a_function,
            Spy().another_function
        ]
        registrar.register(function_list)

        for function in function_list:
            expect(function).to(have_been_called.once)

    with it('should add a function list to the dictionary of streams to functions'):
        stream = Mock()
        function_list = [
            Spy().a_function,
            Spy().another_function
        ]

        expect_(stream)(*function_list)

        for function in function_list:
            expect(function).to_not(have_been_called)

        expect(
            len(registrar.stream_to_testers[stream])
        ).to(equal(len(function_list)))

    with it('should merge multiple function lists if applied to the same stream'):
        stream = Mock()

        first_function_list = [
            Spy().first_function,
            Spy().second_function
        ]

        second_function_list = [
            Spy().third_function,
            Spy().fourth_function
        ]

        expect_(stream)(*first_function_list)
        expect_(stream)(*second_function_list)

        expect(
            len(registrar.stream_to_testers[stream])
        ).to(equal(len(first_function_list + second_function_list)))
