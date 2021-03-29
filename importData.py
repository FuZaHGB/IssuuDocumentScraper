import json
import sys


class ImportData:
    """
    This class reads in the json file and parses each json object into a dictionary which is accessed through a
    generator.
    Achieves this using the json library: https://www.w3schools.com/python/python_json.asp
    Code was derived from:
    https://stackoverflow.com/questions/61851241/python-json-file-reading-generator-multi-line
    """

    def __init__(self, filename):
        self.filename = filename

    def read_json(self):
        try:
            # Encoding fixed UnicodeDecodeError; only an issue on larger files, small JSON data files worked fine
            # https://stackoverflow.com/questions/49562499/how-to-fix-unicodedecodeerror-charmap-codec-cant-decode-byte-0x9d-in-posit
            with open(self.filename, "r", encoding="utf-8") as json_file:
                line = json_file.readline()
                while line:
                    try:
                        yield json.loads(line)  # Return this JSON object as a generator
                        line = json_file.readline()
                    except json.JSONDecodeError as e:  # Attempt to catch exception before crashing
                        return e

        except FileNotFoundError:
            print('The file \'%s\' could not be found' % self.filename)
            sys.exit()
