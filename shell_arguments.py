import argparse

class ShellArguments:

    args = None

    def __init__(self):
        program_description = "A program that stores information from twitter according to a specified filter"

        parser = argparse.ArgumentParser(description=program_description)

        parser.add_argument('filter', metavar='filter', nargs='+', help='filter for twitter API')
        parser.add_argument('-v', action='store_true', help='increase verbosity')
        
        self.args = parser.parse_args()

    def get_filter(self):
        return self.args.filter

