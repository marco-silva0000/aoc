f = open("1/test.txt")
elfs = [[]]
for l in f.readlines():
    print(l)
    if l != "\n":
        elfs[-1].append(int(l))
    else:
        elfs.append([])

print(elfs)
print(len(elfs))
max_elf = max([sum(elf_food) for elf_food in elfs])
print(max_elf)

all_elfs_total = [sum(elf_food) for elf_food in elfs]
all_elfs_total.sort(reverse=True)
print(sum(all_elfs_total[:3]))
