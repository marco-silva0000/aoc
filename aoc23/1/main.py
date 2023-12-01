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
    l = l.strip()
    for c in l:
        print("c", c)
        print("current_word", current_word)
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
    print("first_digit", first_digit)
    current_word = ""
    for c in l[::-1]:
        print("c", c)
        print("current_word", current_word)
        try:
            second_digit = int(c)
            break
        except:
            current_word = c + current_word
            current_word = current_word[:5]
            if current_word in numbers_dict.keys():
                second_digit = numbers_dict[current_word]
                break
            elif current_word[:-1] in numbers_dict.keys():
                second_digit = numbers_dict[current_word[:-1]]
                break
            elif current_word[:-2] in numbers_dict.keys():
                second_digit = numbers_dict[current_word[:-2]]
                break
    print("second_digit", second_digit)
    return int(f"{first_digit}{second_digit}")
    

part1_result = []
part2_result = []
for l in f.readlines():
    print(l)
    first = match_first(l, lambda x: int(x))
    last = match_first(l[::-1], lambda x: int(x))
    # part1_result.append(int(f"{first}{last}"))
    part2_result.append(part2_process_line(l))


print(f"part1: {sum(part1_result)}")
print(part2_result)
print(f"part2: {sum(part2_result)}")
