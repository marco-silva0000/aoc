f = open("25/input.txt")
numbers = []

def from_snafu(snafu):
    power = len(l) - 1
    number = []
    for c in snafu:
        print("c", c)
        if c == '-':
            c = '-1'
        elif c == '=':
            c = '-2'
        place = pow(5, power)
        print(place)
        number.append(int(c)*place)
        power -= 1

    return sum(number)

for l in f.readlines():
    l = l.strip()
    print("l", l)
    power = len(l) - 1
    number = []
    numbers.append(from_snafu(l))

def to_base_5(n):
    s = ""
    carry = 0
    while n:
        c = n % 5
        n //= 5
        if c == 4:
            c = '-'
            n += 1
        elif c == 3:
            c = '='
            n += 1
        s = str(c) + s
    return s

def to_snafu(snafu):
    result = to_base_5(snafu)
    print(result)
    return result



print(numbers)
result = sum(numbers)
print(result)
print(to_snafu(result))



