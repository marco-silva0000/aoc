numbers_dict = {
    key: index
    for index, key in enumerate(
        "one two three four five six seven eight nine".split(" "), start=1
    )
}
digits_dict = {str(key): index for index, key in enumerate(range(1, 10), start=1)}
numbers_dict.update(digits_dict)
reverse_numbers_dict = {key[::-1]: value for key, value in numbers_dict.items()}

f = open("1/test.txt")
f = open("1/input.txt")


def get_first_non_error_result(iterable, predicate):
    for i in iterable:
        try:
            return predicate(i)
        except:
            pass


def part2_process_line(l, matching_dict=numbers_dict):
    current_word = ""
    dict_keys = list(matching_dict.keys())
    first_digit = None
    for c in l:
        # print("c", c)
        # print("current_word", current_word)
        current_word += c
        current_word = current_word[-5:]
        if c in matching_dict:
            first_digit = matching_dict[c]
            break
        elif current_word in dict_keys:
            first_digit = matching_dict[current_word]
            break
        elif (substring := current_word[1:]) in dict_keys:
            # print("substring", substring)
            first_digit = matching_dict[substring]
            break
        elif (substring := current_word[2:]) in dict_keys:
            # print("substring", substring)
            first_digit = matching_dict[substring]
            break
    return first_digit


part1_result = []
part2_result = []
for l in f.readlines():
    l = l.strip()
    print(l)
    first = get_first_non_error_result(l, lambda x: int(x))
    last = get_first_non_error_result(l[::-1], lambda x: int(x))
    # part1_result.append(int(f"{first}{last}"))
    first_part_2 = part2_process_line(l)
    last_part_2 = part2_process_line(l[::-1], matching_dict=reverse_numbers_dict)
    part2_result.append(int(f"{first_part_2}{last_part_2}"))


print(part1_result)
print(f"part1: {sum(part1_result)}")
print(part2_result)
print(f"part2: {sum(part2_result)}")
