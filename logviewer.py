import sys
import termcolor
import re

info = {'regex': r'INFO', 'color': 'green'}
debug = {'regex': r'DEBUG', 'color': 'blue'}
warning = {'regex': r'WARNING', 'color': 'yellow'}
error = {'regex': r'ERROR', 'color': 'red'}


def process(text):
    func = lambda x: termcolor.colored(text, 'white')
    for f in (info, warning, debug, error):
        if len(re.findall(f['regex'], text)):
            func = lambda x: termcolor.colored(text, f['color'])
            break
    return func(text)


if len(sys.argv) != 2:
    filename = './.log/bot.log'
else:
    filename = sys.argv[1]

last_lines = 50

print(f"Looking for logs in {filename}")
prev = 0
while True:
    try:
        lines = open(filename, 'r').read().split('\n')[-last_lines:]
        lines.remove('')
        length = len(lines)
        if prev != length:
            for line in lines[prev-length:]:
                print(process(line))
        prev = length
    except KeyboardInterrupt:
        break
