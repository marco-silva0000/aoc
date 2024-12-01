from collections import Counter

numbers_dict = {
    key: index
    for index, key in enumerate(
        "one two three four five six seven eight nine".split(" "), start=1
    )
}
digits_dict = {str(key): index for index, key in enumerate(range(1, 10), start=1)}
numbers_dict.update(digits_dict)
reverse_numbers_dict = {key[::-1]: value for key, value in numbers_dict.items()}

f = open("day-1/test.txt")
f = open("day-1/input.txt")


part1_result = []
part2_result = []
p1_1 = []
p1_2 = []
p2_1 = []
p2_2 = []
for l in f.readlines():
    l = l.strip()
    print(l)
    data = l.split()
    p1_1.append(data[0])
    p1_2.append(data[1])
    p2_1.append(data[0])
    p2_2.append(data[1])

p1_1 = sorted(p1_1)
p1_2 = sorted(p1_2)

result1 = 0
for i in range(len(p1_1)):
    first = int(p1_1.pop(0))
    second = int(p1_2.pop(0))
    print(
        f"diffing {first} with {second} in abs {first - second} adding it to {result1}"
    )
    result1 += abs(first - second)


print(result1)

counter = Counter(p2_2)
result2 = 0
for val in p2_1:
    result2 += int(val) * counter[val]

print(result2)
