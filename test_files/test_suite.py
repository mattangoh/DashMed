import os
import unittest

if __name__ == "__main__":
    
    #Ensuring we are located where test_suite is saved
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f'Running tests in directory: {current_script_dir}')

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir = current_script_dir, pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)