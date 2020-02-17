import sys


def main():
    argv = sys.argv
    print(argv)

    if argv[1] == '--task':
        if argv[2] == 'all_keyword':
            print("send_all_keyword_tasks()")
            pass
        else:
            args = dict([arg.split('=') for arg in sys.argv[2:]])
            print(args)


if __name__ == '__main__':
    main()