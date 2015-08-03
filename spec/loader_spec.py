from expects import expect

from spec.custom_matchers.contain_exactly_function_called import contain_exactly_function_called

from pysellus import loader

with description('the loader module loads all top-level functions in a directory or file'):
    with it('should load every function when there is only one file'):
        expect(loader.load('spec/fixtures/one_file/')).to(
            contain_exactly_function_called('pscheck_a_function',
                                            'pscheck_another_function')
        )

    with it('should load every function of the specified file'):
        expect(loader.load('spec/fixtures/multiple_files/file_1.py')).to(
            contain_exactly_function_called('pscheck_file_1_function_a',
                                            'pscheck_file_1_function_b')
        )

    with it('should load every function when there is more than one file'):
        expect(loader.load('spec/fixtures/multiple_files/')).to(
            contain_exactly_function_called('pscheck_file_1_function_a',
                                            'pscheck_file_1_function_b',
                                            'pscheck_file_2_function_a',
                                            'pscheck_file_2_function_b',
                                            'pscheck_file_3_function_a',
                                            'pscheck_file_3_function_b')
        )

    with it("should only load setup functions (starting with pscheck)"):
        expect(loader.load('spec/fixtures/file_with_helper_functions/')).to(
            contain_exactly_function_called('pscheck_function')
        )
