'''
[Splash WhatsApp] - WhatsApp listener client that displays messages on
                    screen.
File: splashwp_textutils.py - contains functions for text manipulation.

Copyright (c) <2014> Alberto Lorenzo <alorenzo.md@gmail.com>
'''

__author__ = 'Alberto Lorenzo'
__version__ = '1.1.0'
__date__ = '25/06/2014'
__email__ = 'alorenzo.md@gmail.com'
__license__ = 'GNU GPLv3'

from subprocess import Popen, PIPE, STDOUT    # For running commands
from math import *    # For expression evaluation


# Needed because QLabel widget (used as splash screen widget) doesn't split
# text into lines automatically unlike QTextBrowser widget.
def splitIntoLines(text, characters):
    '''Divides a string into lines of a given maximum length in characters,
    trying not to split words, using the HTML carriage return symbol '<br>'.

    Args:
      text (str): string to be splitted into lines.
      characters (int): the desired maximum length.

    Returns:
      The content of parameter 'text' with '<br>' as the carriage return.
    '''

    # PyQt ignores regular carriage '\n' return so it has to be changed by its
    # HTML counterpart '<br>'.
    index = 0
    length = len(text)
    while index < length:
        try:
            index = text.index('\n')
            text = text[:index] + '<br>' + text[index + 1:]
        except ValueError:
            break

    out = ''
    while length > characters:
        try:
            index = text.rindex(' ', 0, characters)
            out += text[:index] + '<br>'
            text = text[index + 1:]
        except ValueError:    # Too long words will be splitted.
            out += text[:characters] + '<br>'
            text = text[characters:]
    out += text

    return out


def setBold(text):
    '''Adds the text the HTML symbols for bold characters.

    Args:
      text (str): the text to be set up in bold.
    '''

    out = '<b>' + text + '</b>'

    return out


def setItalic(text):
    '''Ads the text the HTML symbols for italic characters.

    Args:
      text (str): the text to be set up in italics.
    '''

    out = '<i>' + text + '</i>'

    return out


def evaluate(text):
    '''Evaluates passed text if a valid expression.

    Args:
      text (str): the text to be evaluated.
    '''

    try:
        out = str(eval(text))
    except NameError:
        out = text
    except SyntaxError:
        out = text

    return out


def calculate(text):
    '''Appends its evaluation to passed text if a valid expression.

    Args:
      text (str): the text to be evaluated.
    '''

    try:
        out = text + ' = ' + str(eval(text))
    except NameError:
        out = text
    except SyntaxError:
        out = text

    return out


def execute(text):
    '''Tells the OS to execute the content of text if a valid command.

    Args:
      text (str): the command to be executed.
    '''

    out = text
    args = text.split(' ')    # Popen needs a list of arguments not a string
    # To manage using whitespaces in paths i.e, replace it with '$_' symbol.
    args = [element.replace('$_', ' ') for element in args]
    try:
        Popen(args, stdout=PIPE, stderr=STDOUT)
    except:    # Since a huge amount of different errors may ocur.
        pass
    if len(args) == 1:
        out = '<b>[' + args[0] + ']</b>'
    else:
        out = '<b>[' + ' '.join(args) + ']</b>'
    return out

# This is the set of current supported commands:
commands = {'$bold': setBold, '$ital': setItalic, '$eval': evaluate,
            '$calc': calculate, '$exec': execute}


def parseCommands(text, command=None):
    '''Parses the commands encountered inside the passed text. It calls
    recursively to itself to manage this task.

    Args:
      text (str): the text to be parsed.
      command (str): the command to be aplied, employed in recursively calls.
    '''

    out = text
    # In order to avoid errors, stop parsing if the number of the left brackets
    # differs from the right brackets. Stop parsing if at a certain moment,
    # there are more right brackets than left brackets.
    length = len(text)
    lbrackets = 0
    rbrackets = 0
    for index in range(length):
        if out[index] == '{':
            lbrackets += 1
        elif out[index] == '}':
            rbrackets += 1
        if rbrackets > lbrackets:
            break
    # If everything it's ok, begin recursively parsing:
    if lbrackets == rbrackets and '{}' not in out:    # {} throw exceptions.
        while '{' in out:
            lindex = out.index('{')
            lbrackets = 0
            rbrackets = 0
            for rindex in range(lindex, length):
                if out[rindex] == '{':
                    lbrackets += 1
                elif out[rindex] == '}':
                    rbrackets += 1
                if lbrackets == rbrackets:
                    out = out[:lindex - 5] + \
                        str(parseCommands(out[lindex + 1:rindex],
                                          out[lindex - 5:lindex])) + \
                        out[rindex + 1:]
                    break
    # When there're no more brackets to parse, aply the proper command.
    if command and command in commands:
        out = commands[command](out)

    return out
