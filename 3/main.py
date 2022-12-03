from enum import Enum


f = open("3/input.txt")

def get_score(c: str) -> int:
    score = ord(c)
    if score <= 90: # uppercase
        score += -64 + 26
    else:
        score -= 96
    return score


def find_common(first: str, second: str) -> str:
    for c in first:
        if c in second:
            return c
    raise ValueError('no common items found')

def find_commons(first: str, second: str) -> str:
    result = ""
    for c in first:
        if c in second:
            if c not in result:
                result += c
    return result

repeated_findings = []
def calc_first(l: str):
    half = int(len(l)/2)
    first = l[:half]
    second = l[half:]
    common = find_common(first, second)
    repeated_findings.append(get_score(common))

lines = iter(f.readlines())
badge_findings = []
for first_bag in lines:
    calc_first(first_bag)
    second_bag = next(lines)
    calc_first(second_bag)
    third_bag = next(lines)
    calc_first(third_bag)
    badge = find_commons(find_commons(first_bag, second_bag), third_bag).strip()
    badge_findings.append(get_score(badge))




print(repeated_findings)
print(sum(repeated_findings))
print(badge_findings)
print(sum(badge_findings))


f.close()
