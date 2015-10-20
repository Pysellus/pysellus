from expects import expect

from spec.custom_matchers.contain_exactly_function_called import contain_exactly_function_called

from pysellus import loader

with description('the loader module loads all top-level functions in a directory or file'):
    with it('should load every function when there is only one file'):
        expect(loader.load_test_files('spec/fixtures/one_file/')).to(
            contain_exactly_function_called('a_function',
                                            'another_function')
        )

    with it('should load every function of the specified file'):
        expect(loader.load_test_files('spec/fixtures/multiple_files/file_1.py')).to(
            contain_exactly_function_called('file_1_function_a',
                                            'file_1_function_b')
        )

    with it('should load every function when there is more than one file'):
        expect(loader.load_test_files('spec/fixtures/multiple_files/')).to(
            contain_exactly_function_called('file_1_function_a',
                                            'file_1_function_b',
                                            'file_2_function_a',
                                            'file_2_function_b',
                                            'file_3_function_a',
                                            'file_3_function_b')
        )

    with it("should only load setup functions"):
        expect(loader.load_test_files('spec/fixtures/file_with_helper_functions/')).to(
            contain_exactly_function_called('function')
        )
