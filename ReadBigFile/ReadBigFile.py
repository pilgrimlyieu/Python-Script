"""
Adapted From https://www.cnblogs.com/wangyangang/p/python-read-big-file-last-n-lines.html
"""

import linecache
import os

def get_line_count(filename):
    count = 0
    with open(filename, 'r') as f:
        while True:
            buffer = f.read(1024)
            if not buffer:
                break
            count += buffer.count('\n')
    return count

file = os.path.join(os.path.split(os.path.abspath(__file__))[0], "Text.txt")
n = 1
linecache.clearcache()
# line_count = get_line_count(file)
# print('num: ', line_count)
# line_count = line_count - n + 1
line_count = 90000000
for i in range(n):
    last_line = linecache.getline(file, line_count)
    print(line_count, last_line)
    line_count += 1