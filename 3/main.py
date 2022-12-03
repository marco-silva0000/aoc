from enum import Enum


f = open("3/input.txt")

print(ord('a'))
print(ord('z'))
print(ord('A'))
print(ord('Z'))
findings = []
for l in f.readlines():
    half = int(len(l)/2)
    first = l[:half]
    second = l[half:]
    print(f"{first}|{second}")
    for c in first:
        if c in second:
            print(c)
            score = ord(c)
            print(score)
            if score <= 90: # uppercase
                score += -64 + 26
            else:
                score -= 96
            print(score)
            findings.append(score)
            break
print(findings)
print(sum(findings))


f.close()
