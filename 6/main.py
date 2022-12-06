from collections import defaultdict


f = open("6/input.txt")
code = f.read()
window_size = 4
window_size2 = 14
packet_start = 0
for i in range(window_size, len(code)):
    start_index = i-window_size
    test = code[start_index:i]
    test_set = set([c for c in test])
    if len(test_set) == window_size:
        print(test)
        print(start_index)
        print(i)
        packet_start = i
        break


for i in range(packet_start + window_size2, len(code)):
    start_index = i-window_size2
    test = code[start_index:i]
    test_set = set([c for c in test])
    if len(test_set) == window_size2:
        print(test)
        print(start_index)
        print(i)
        break

f.close()
