from expects import expect

from spec.custom_matchers.contain_exactly_function_called import contain_exactly_function_called

from pysellus import loader

with description('the loader module loads all functions in the top level of each file in the passed directory'):
    with it('when there is only one file'):
            expect(loader.load('spec/fixtures/one_file/')).to(
                contain_exactly_function_called('a_function', 'another_function')
            )

    with it('when there is more than one file'):
        expect(loader.load('spec/fixtures/multiple_files/')).to(
            contain_exactly_function_called('file_1_function_a',
                                            'file_1_function_b',
                                            'file_2_function_a',
                                            'file_2_function_b',
                                            'file_3_function_a',
                                            'file_3_function_b')
        )
