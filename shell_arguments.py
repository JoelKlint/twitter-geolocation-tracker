import argparse

class ShellArguments:

    def get_args():
        program_description = "A program that stores information from twitter according to a specified filter"

        parser = argparse.ArgumentParser(description=program_description)

        parser.add_argument('filter', metavar='filter', nargs='+', help='filter for twitter API')
        parser.add_argument('--verbose', '-v', action='store_true', help='increase verbosity')
        
        return parser.parse_args()
