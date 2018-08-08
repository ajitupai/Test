import sys


class Sign(object):
    """
    class contains list of signs
    """
    ASTERISK = '*'
    DOT = '.'
    PLUS = '+'
    MINUS = '-'


def get_next_line():
    """
    Iterator to return each line at a time
    """
    for line in sys.stdin:
        yield line

# Generator
genr = get_next_line()


def generate_main_line(line, main_line_count):
    """
    Function to generate line numbers for a given line

    Args:

        line(string): line to which numbers has to be prepended
        main_line_count(string): Line counter of previous line if any,
                                 otherwise would be zero for first line
                                 example: 1, 1.1, 1.1.2

    Returns(string):

        Returns the updated main line counter, which will be helpful
        if any further lines are present
        where there is a need to add a line number

    """
    if line.count(Sign.ASTERISK) == 1:
        main_line_count = int(str(main_line_count).split(Sign.DOT)[0])
        old_txt = Sign.ASTERISK
        main_line_count += 1
        new_txt = main_line_count
    else:
        if line.count(Sign.ASTERISK) == len(str(main_line_count).split(Sign.DOT)):
            lst = str(main_line_count).split(Sign.DOT)
            number = int(str(main_line_count).split(Sign.DOT)[line.count(Sign.ASTERISK) - 1])
            number += 1
            lst[line.count(Sign.ASTERISK) - 1] = str(number)
            main_line_count = Sign.DOT.join(lst)
        elif line.count(Sign.ASTERISK) > len(str(main_line_count).split(Sign.DOT)):
            lst = str(main_line_count).split(Sign.DOT)
            lst.append('1')
            main_line_count = Sign.DOT.join(lst)
        elif line.count(Sign.ASTERISK) < len(str(main_line_count).split(Sign.DOT)):
            lst = str(main_line_count).split(Sign.DOT)
            del lst[line.count(Sign.ASTERISK) - len(str(main_line_count).split(Sign.DOT)):]
            lst[-1] = str(int(lst[-1]) + 1)
            main_line_count = Sign.DOT.join(lst)
        old_txt = reduce(lambda x, y: str(x) + Sign.ASTERISK if x > 0 else '**',
                         range(line.count(Sign.ASTERISK)))
        new_txt = main_line_count

    print line.replace(old_txt, str(new_txt))
    return main_line_count


def put_expand_collapse(current_line, next_line):
    """
    Function to identify and prepend expand collapse signs to line

    Args:
        current_line(string) - Current Line
        next_line(string) - Next Line
    """
    current_line_dot_count = current_line.count(Sign.DOT)
    next_line_dot_count = next_line.count(Sign.DOT)
    current_line = current_line.replace(Sign.DOT, '')
    if not next_line_dot_count or current_line_dot_count == next_line_dot_count:
        print ' ' * current_line_dot_count + Sign.MINUS + current_line
    else:
        print ' ' * current_line_dot_count + Sign.PLUS + current_line


def parse_file():
    """
     Function to parse input file and generate desired output
    """
    current_line = next(genr, None)
    main_line_count = 0
    while current_line:
        next_line = next(genr, None)
        while next_line is not None and not next_line.strip():
            next_line = next(genr, None)
        if Sign.ASTERISK in current_line:
            main_line_count = generate_main_line(current_line, main_line_count)
        elif Sign.DOT in current_line:
            if not next_line:
                put_expand_collapse(current_line, '')
            elif Sign.DOT in next_line:
                put_expand_collapse(current_line, next_line)
            elif Sign.ASTERISK in next_line:
                put_expand_collapse(current_line, '')
            elif Sign.ASTERISK not in next_line and Sign.DOT not in next_line:
                next_line_lst = []

                while next_line is not None and Sign.ASTERISK not in next_line and Sign.DOT not in next_line:
                    next_line_lst.append(next_line)
                    next_line = next(genr, None)

                if not next_line:
                    put_expand_collapse(current_line, '')
                elif Sign.DOT in next_line:
                    put_expand_collapse(current_line, next_line)
                elif Sign.ASTERISK in next_line:
                    put_expand_collapse(current_line, '')
                for line in next_line_lst:
                    if line.strip():
                        print line

            elif Sign.DOT in current_line:
                put_expand_collapse(current_line, '')
            else:
                print current_line
        else:
            print current_line
        current_line = next_line


if __name__ == '__main__':
    parse_file()
