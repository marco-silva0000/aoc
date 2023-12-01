from collections import defaultdict


f = open("5/input.txt")
lines = iter(f.readlines())
crates_height = 8
crates = defaultdict(list)
crates2 = defaultdict(list)
instructions = []
for i, l in enumerate(lines):
    if i < crates_height:
        for c in range(0, len(l), 4):
            if l[c + 1] != ' ':
                crates[int(c/4 + 1)].append(l[c + 1])
                crates2[int(c/4 + 1)].append(l[c + 1])
    if i >crates_height + 1:
        ammount, from_to = l.lstrip('move ').split(" from ")
        origin, destiny = from_to.split(" to ")
        origin = int(origin)
        destiny = int(destiny)
        ammount = int(ammount)
        # print(ammount)
        # print(origin)
        # print(destiny)
        # part 1
        for j in range(ammount):
            print(j)
            print(crates)
            item = crates[origin].pop(0)
            crates[destiny].insert(0, item)
            print(crates)
        # part 2
        chunk = crates2[origin][:ammount]
        crates2[origin] = crates2[origin][ammount:]
        chunk.extend(crates2[destiny])
        crates2[destiny] = chunk
        




result = [crates[i][0] for i in range(1, len(crates.keys()) + 1)]
print("".join(result))
print(result)

result2 = [crates2[i][0] for i in range(1, len(crates2.keys()) + 1)]
print("".join(result2))
print(result2)

f.close()
