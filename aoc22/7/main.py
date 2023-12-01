from collections import defaultdict
from typing import List


class FSItem():
    def __init__(self, path: str, size=0, kind='dir') -> None:
        self.path = path
        self.size = size
        self.files: list[FSItem] = []
        self.kind = kind

    def add_dir(self, path, name):
        print("add dir")
        print(f"{path}")
        print(f"{name}")
        print(f"{path.split('/')}")
        current, *rest = path.split("/")
        rest_str = "/".join(rest)
        print(f"current: {current}")
        print(f"rest: {rest}")
        print(f"rest_str: {rest_str}")
        if not rest_str:
            self.files.append(FSItem(name))
        else:
            list(filter(lambda x: x.path == rest[0], self.files))[0].add_dir(rest_str, name)

    def add_file(self, path, name, size):
        print("add file")
        current, *rest = path.split("/")
        rest_str = "/".join(rest)
        print("rest_str")
        print(rest_str)
        print("name")
        print(name)
        print("current")
        print(current)
        if not rest_str:
            self.files.append(FSItem(name, int(size), kind='file'))
        else:
            list(filter(lambda x: x.path == rest[0], self.files))[0].add_file(rest_str, name, size)

    def update_size(self):
        result = 0
        for file in self.files:
            if file.size:
                result += file.size
            else:
                file.update_size()
                result += file.size
        self.size = result
        return result

    def __str__(self) -> str:
        return f"FSItem({self.path}, {self.size}, {[str(file) for file in self.files]})"

    def __radd__(self, other):
        return other + self.size

    def __lt__(self, other):
        return self.size < other.size

    def children(self):
        result = [self]
        for file in self.files:
            result.extend(file.children()) 
        return result

    def to_string(self, n=0) -> str:
        new_line = "\n"
        files_str = "".join([file.to_string(n+1) for file in self.files])
        return f"{'  '*n}- {self.path} ({self.kind}{', ' + str(self.size) if self.size else ''}){new_line}{files_str}"




CD = 'cd'
LS = 'ls'

f = open("7/input.txt")
comand_prefix = "$ "
current_dir = '/'
last_command = None

fs = FSItem('/')
for l in f.readlines():
    print(fs.to_string())
    l = l.strip()
    print(f"l: {l}")
    print(f"current_dir: {current_dir}")
    if l.startswith(comand_prefix):
        comand = l.removeprefix(comand_prefix)
        if comand.startswith(CD):
            last_command = CD
            program, args = comand.split(" ")
            if args == "..":
                print('before')
                print(current_dir)
                print(current_dir.split("/"))
                current_dir = "/".join(current_dir.split('/')[:-2]) + "/"
                print('after')
                print(current_dir)
            elif args == "/":
                current_dir = args
            else:
                print('will set current_dir')
                print(args)
                current_dir += f"{args}/"
                print(current_dir)
        elif comand.startswith(LS):
            last_command = LS
        else:
            raise ValueError(f'error parsing program: {l}')
    else:
        if last_command == LS:
            if l.startswith("dir"):
                _, name = l.split("dir ")
                fs.add_dir(current_dir, name)
                print('added files[] on current_dir{current_dir}')
            else:
                size, name = l.split(" ")
                fs.add_file(current_dir, name, size)
        elif last_command == CD:
            pass
        else:
            raise ValueError(f'error parsing input: {l}')
print(fs)
print(fs.to_string())
print(fs.update_size())
print(fs.to_string())
print([str(f) for f in fs.children()])
part1: List[FSItem] = list(filter(lambda x: x.size < 100000 and x.kind == 'dir', fs.children()))
print([str(f) for f in part1])
print(sum(part1))
max = fs.size
print(f"max:{max}")
unused = 70000000 - max
print(f"unused:{unused}")
needed_to_free_up = 30000000 - unused
print(f"needed_to_free_up:{needed_to_free_up}")
part2: List[FSItem] = list(filter(lambda x: x.size > needed_to_free_up and x.kind == 'dir', fs.children()))
# print([str(f) for f in part2])
part2.sort()
# print([str(f) for f in part2])
print("min(part2)")
print(min(part2).size)

f.close()
