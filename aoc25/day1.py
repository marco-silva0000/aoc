from collections import deque

dial = deque(range(0,100))
print(dial)
dial.rotate(50)
print(dial)

result = 0

def rotate_left(n: int):
    dial.rotate(n)

def rotate_right(n: int):
    dial.rotate(n*-1)

# rotate_left(1)
# assert dial[0] == 51
# rotate_left(1)
# assert dial[0] == 52
# rotate_right(1)
# assert dial[0] == 51
# rotate_right(1)
# print(dial)
# assert dial[0] == 50
# rotate_left(49)
# print(dial)
# assert dial[0] == 99
# rotate_right(99)
# assert dial[0] == 0
# print(dial)
# rotate_right(1)
# print(dial)
# assert dial[0] == 99

with open("input1.txt") as f:
    lines = f.readlines()
    def rotate_n_left(n: int):
        global result
        for _ in range(n):
            rotate_left(1)
            if dial[0] == 0:
                result += 1

    def rotate_n_right(n: int):
        global result
        for _ in range(n):
            rotate_right(1)
            if dial[0] == 0:
                result += 1

    for line in lines:
        letter = line[0]
        number = int(line[1:])
        if letter == "R":
            rotate_n_right(number)
        else:
            rotate_n_left(number)
        print(f"Dial is rotated '{letter}{number}' to point to {dial[0]}")

print(result)

