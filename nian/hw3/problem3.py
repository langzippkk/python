"""
>>> lines = ['I went to Poland.',
...          'He went to Spain.',
...          'We are very happy.']
>>> for line in grep('went', lines):
...     print(line)
I went to Poland.
He went to Spain.
>>> for line in grep('i', lines, ignore_case=True):
...     print(line)
I went to Poland.
He went to Spain.
>>> for line in grep('foobar', lines):
...     print(line)

"""


def grep(pattern, lines, ignore_case=False):
    for line in lines:
        if ignore_case == True:
            if pattern.lower() in line.lower():
                yield line
        if ignore_case == False:
            if pattern in line:
                yield line


if __name__ == '__main__':

    # Example usage.  Feel free to change this; it won't be graded.

    lines = ['I went to Poland.',
             'He went to spain.',
             'She is very happy.']

    print('Find "went", case sensitive:')
    for line in grep('went', lines):
        print(line)

    print('\nFind "i", case sensitive: ')
    for line in grep('i', lines):
        print(line)

    print('\nFind "i", case insensitive: ')
    for line in grep('i', lines, ignore_case=True):
        print(line)
