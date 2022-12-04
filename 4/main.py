
def bitshift(section):
    start, finish = section.split('-')
    size = int(finish) - int(start) + 1
    size_mask = 0
    for n in range(size):
        size_mask |= 1 << n + 1
    result = size_mask << (int(start))
    result = result >> 2
    # todo, find out why it's shifted too much
    return result


f = open("4/input.txt")
lines = iter(f.readlines())
result = 0
result2 = 0
for sections in lines:
    elf1, elf2 = sections.split(',')
    elf1_bit = bitshift(elf1)
    elf2_bit = bitshift(elf2)
    or_result = elf1_bit | elf2_bit
    print(sections)
    print(f"{elf1_bit:#0128b}")
    print(f"{elf2_bit:#0128b}")

    if elf1_bit == or_result or elf2_bit == or_result:
        result += 1
    if not elf1_bit & elf2_bit == 0:
        result2 += 1

print(result)
print(result2)


f.close()
