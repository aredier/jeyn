import sys
import os


# have test helpers importable:
# https://stackoverflow.com/questions/33508060/create-and-import-helper-functions-in-tests-without-creating-packages-in-test-di
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))
