from functools import cmp_to_key

f = open("13/input.txt")
pairs = []
pair = [None, None]
pair_index = 0
for i, l in enumerate(f.readlines()):
    l = l.strip()
    print(l)
    if l == "":
        pairs.append(
            (pair[0], pair[1]),
        )
    else:
        print(f"will set pair {pair_index} with {l}")
        exec(f"pair[{pair_index}] = {l}")
        pair_index += 1
        if pair_index > 1:
            pair_index = 0

pairs.append(
    (pair[0], pair[1]),
)
f.close()

pairs2 = []
for pair in pairs:
    pairs2.extend([pair[0], pair[1]])
divider_1 = [[2]]
divider_2 = [[6]]
pairs2.append(divider_1)
pairs2.append(divider_2)

print("pairs")
print(pairs)


def pair_compair(left, right, iter=0):
    spaces = " " * iter
    print(f"{spaces}- Compare {left} vs {right}")
    if type(left) == int and type(right) == int:
        if left == right:
            return None
        is_left_smaller = left < right
        if is_left_smaller:
            print(f"{spaces} - Left side is smaller, so inputs are in the right order")
        else:
            print(
                f"{spaces} - Right side is smaller, so inputs are not in the right order"
            )
        return is_left_smaller
    elif type(left) == int:
        print(f"{spaces} - Mixed types; convert left to {[left]} and retry comparison")
        return pair_compair([left], right, iter + 1)
    elif type(right) == int:
        print(
            f"{spaces} - Mixed types; convert right to {[right]} and retry comparison"
        )
        return pair_compair(left, [right], iter + 1)
    else:  # Both are lists
        for i, new_left in enumerate(left):
            try:
                new_right = right[i]
                result = pair_compair(new_left, new_right, iter + 1)
                if result is None:
                    continue
                return result
            except IndexError:
                print(
                    f"{spaces} - Right side ran out of items, so inputs are not in the right order"
                )
                return False
        else:
            if len(left) == len(right):
                return None
            print(
                f"{spaces} - Left side ran out of items, so inputs are in the right order"
            )
            return True


results = []
for i, pair in enumerate(pairs):
    print(f"== Pair {i+1} ==")
    result = pair_compair(pair[0], pair[1])
    results.append(
        (
            (i + 1),
            result,
        )
    )
    print(f"")

print(results)
print(sum([i for i, result in results if result]))


def comparator(*args):
    left = args[0]
    right = args[1]
    if pair_compair(left, right):
        return -1
    return 1


sorted_pairs = sorted(pairs2, key=cmp_to_key(comparator))
divider_1_index = sorted_pairs.index(divider_1) + 1
divider_2_index = sorted_pairs.index(divider_2) + 1
print(divider_1_index * divider_2_index)
