import datetime
import contextvars
import logging


def main(*args, **kwargs):
    print("Advent of Code 2025")

    # print args
    import sys

    sysargs = sys.argv
    try:
        day = sysargs[1]
    except IndexError:
        day = str(datetime.datetime.now().day)
    try:
        part = sysargs[2]
    except IndexError:
        part = "all"

    print("Day: " + day)
    print("Part: " + part)
    if not day.isdigit():
        print("Day must be a number")
        return

    import importlib

    try:
        module_name = f"day-{day}.main"
        print("Module: " + module_name)
        module = importlib.import_module(module_name)

        data = module.get_data()
        parsed_data = module.parse(data)

        tests = filter(lambda x: x.startswith("test"), module.__dict__.keys())
        part1_tests = filter(lambda x: x.endswith("_part1"), tests)
        part2_tests = filter(lambda x: x.endswith("_part2"), tests)
        if part == "all":
            logging_ctx = contextvars.ContextVar("logging")
            logging_ctx.set(logging.DEBUG)
            for test in part1_tests:
                t = getattr(module, test)()
                print(t)
            for test in part2_tests:
                t = getattr(module, test)()
                print(t)
            logging_ctx.set(logging.INFO)
            print(module.run_part1(parsed_data))
            print(module.run_part2(parsed_data))
        elif part == "1":
            logging_ctx = contextvars.ContextVar("logging")
            logging_ctx.set(logging.DEBUG)
            for test in part1_tests:
                t = getattr(module, test)()
                print(t)
            logging_ctx.set(logging.INFO)
            print(module.run_part1(parsed_data))
        elif part == "2":
            logging_ctx = contextvars.ContextVar("logging")
            logging_ctx.set(logging.DEBUG)
            print("Only Part 2")
            for test in part2_tests:
                t = getattr(module, test)()
                print(t)
            logging_ctx.set(logging.INFO)
            print(module.run_part2(parsed_data))
        else:
            print("Part must be 1, 2, or all")
        print("Module:", module)
    except ImportError as e:
        print(e)
        return


if __name__ == "__main__":
    main()
