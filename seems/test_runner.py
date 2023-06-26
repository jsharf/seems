import unittest
import seems
import fire
import importlib
import importlib.util
import sys

def main(module_name_or_file_path: str, *args, **kwargs):
    # Determine if this is a path or a module name. Import accordingly.
    if module_name_or_file_path.endswith('.py'):
        # It's a path name.
        module_name = module_name_or_file_path[:-3]
        spec = importlib.util.spec_from_file_location(module_name, module_name_or_file_path)
        foo = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = foo
        spec.loader.exec_module(foo)
    else:
        # It's a module.
        module = importlib.import_module(module_name_or_file_path)
    
    # Aggregate all tests.
    suites = []
    for test in seems._Tests():
        suites.append(unittest.TestLoader().loadTestsFromTestCase(test))
    
    # Run the tests.
    aggregate_suite = unittest.TestSuite(suites)
    runner = unittest.TextTestRunner(*args, **kwargs)
    runner.run(aggregate_suite)

if __name__ == '__main__':
    fire.Fire(main)
