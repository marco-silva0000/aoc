import datetime


def main(*args, **kwargs):
    print("Advent of Code 2023")

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
        if part == "all":
            print(module.part1(parsed_data))
            print(module.part2(parsed_data))
        elif part == "1":
            print(module.part1(parsed_data))
        elif part == "2":
            print(module.part2(parsed_data))
        else:
            print("Part must be 1, 2, or all")
        print("Module:", module)
    except ImportError as e:
        print(e)
        return
