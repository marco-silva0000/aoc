numbers_dict = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
reverse_numbers_dict = {key[::-1]: value for key, value in numbers_dict.items()}

f = open("1/input.txt")


def match_first(iterable, predicate):
    for i in iterable:
        try:
            return predicate(i)
        except:
            pass


def part2_process_line(l):
    current_word = ""
    first_digit = None
    second_digit = None
    for c in l:
        # print("c", c)
        # print("current_word", current_word)
        try:
            first_digit = int(c)
            break
        except:
            current_word += c
            current_word = current_word[-5:]
            if current_word in numbers_dict.keys():
                first_digit = numbers_dict[current_word]
                break
            elif current_word[1:] in numbers_dict.keys():
                first_digit = numbers_dict[current_word[1:]]
                break
            elif current_word[2:] in numbers_dict.keys():
                first_digit = numbers_dict[current_word[2:]]
                break
    return first_digit


part1_result = []
part2_result = []
for l in f.readlines():
    l = l.strip()
    print(l)
    first = match_first(l, lambda x: int(x))
    last = match_first(l[::-1], lambda x: int(x))
    # part1_result.append(int(f"{first}{last}"))
    first_part_2 = part2_process_line(l)
    last_part_2 = part2_process_line(l[::-1])
    part2_result.append(int(f"{first_part_2}{last_part_2}"))


print(f"part1: {sum(part1_result)}")
print(part2_result)
print(f"part2: {sum(part2_result)}")
