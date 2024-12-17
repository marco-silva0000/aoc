# Notes?
Register A: 27575648
Register B: 0
Register C: 0

Program: 2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0
Program: 2,4,1,2,7,5,4,1,5,1,7,5,5,0,3,3,0

b = a%8       # 2, 4  bst
b = b xor 2   # 1, 2  bxl
c = a/2**b    # 7, 5  cdv
b = b ^ c     # 4, 1  bxc
b = b xor 3   # 1, 3  bxl
print(b%8)    # 5, 5  out
a = a/2**3       # 0, 3  adv
jump to 0     # 3, 0  jnz

2 = 010

x xor 2 = 2

val = 2^2


001000 > 3,0
find 0,3 > 011101
3, 0    0, 3
001000 011101

55 -> 101001
test with
001000 011101 101001

13
011010
001000 011101 101001 011010

411355 100100011100111110

test with
001000 011101 100 100 011 100 111 110

149302
4,1,1,3,5,5  100 100  011 100 110 110
149310
4,1,1,3,5,5

7,5,4,1,1,3 262475
001 000 000 000 101 001 011
         1   1   4   5   7


21234
1,2,7,5,4
101 001 011 110 010
 4   5   7   2   1

48628
2,4,1,2,7,0
001 011 110 111 110 100
     7   2   1   4   2
001 000 011 101 101 001 011 010 000 000 101 001 011 110 111 110 100
001 000 011 101 101 001 011 010 000 000 101 001 011 110 111 110 100
 0   3   3   0   5   5   7   1   5   1   4   5   7   2   1   4   2

2,4,1,2,7,5,4,1,5,1,7,5,5,0,3,3,0
Program: 2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0

001 000 011 101 101 001 011 010 000 101 001 011 110 111 110 100
 0   3   3   0   5   5   7   1   1   4   5   7   2   1   4   2

2,4,1,2,7,5,1,5,1,7,5,5,0,3,3,0
Program: 2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0
001 000 011 101 101 001 011 010 000 101 001 011 110 111 110 100
 0   3   3   0   5   5   7   1   5   5   1   5   7   2   1   4   2

18657
4,1,3,5,5
100 100 011 100 001
 5   5   3   1  4

544773
4,1,1,3,5,5,1
010 000 101 000 000 000 101
 1   5   5   3   1   1    4

001 000 011 101 101 001 101 000 000 000 101 011 110 111 110 100
001 000 011 101 101 001  x   x   x   x   x   x 110 111 110 100








# comands on console?

7%8
6%8
5%8
8%8
9%8
;29R1 <<3
1 <<3
format(1 <<3, "b")
format(1 <<3, "16b")
format(1 <<3, "16b0")
format(1 <<3, "0:16b")
format(1 <<3, "016b")
format(1 <<3 + 450, "016b")
format((1 <<3) + 450, "016b")
format((1<<3) + 450, "016b")
format((1<<9) + 450, "016b")
format(450, "016b")
format(int(7/3), "08b")
format(int(7), "08b")
format(int(256), "08b")
format(int(512), "08b")
format(int(511), "08b")
format(int(511/2**3), "08b")
format(int(511/(2**3)), "08b")
format(int(511/(2**3)), "16b")
format(int(511/(2**3)), "016b")
format(int(10/(2**3)), "016b")
format(int(10), "016b")
format(int(15), "016b")
format(int(9), "016b")
format(int(7), "016b")
format(int(633), "016b")
format(int(63), "016b")
format(int(63)/(2**3), "016b")
format(int(63/(2**3)), "016b")
format(int(63/(2**3)), "016b")
format(int(53/(2**3)), "016b")
format(int(53), "016b")
format(int(53%8), "016b")
format(int(53%8)^2, "016b")
format(int(53/(2**7)), "016b")
7^0
2^2
0^2
bin17
format(int(17), "016b")
format(int(17), "016b")
a=17
format(a%8, "016b")
format(a%8 ^ 2, "016b")
format(a/(2**2), "016b")
format(int(a/(2**2)), "016b")
format(a%8 ^ 2 ^ 4, "016b")
format(a%8 ^ 2 ^ 4, "016b")
format((a%8 ^ 2 ^ 4)%8, "016b")
5
a<<3+5
bin(a<<3+5)
bin((a<<3)+5)
bin(a)
1%8
1/4
q^2
0^2
format(int(16/4), "016b")
format(int(16), "016b")
format(int(4/4), "016b")
format(int(4), "016b")
format(int(4/4), "016b")
4>>2
a%8
a%8 ^ (a>>2)
a%8 ^ (a>>2) ^ 8
a%8 ^ (a>>2) ^ 8
4>>4
a>>(a^2)
(a%8)^2
a
A = 1
(A%8)^2
int(a/(2**3))
a>>3
(A%8)^2
(A%8)^2>>3
(a%8)^2>>3
(a%8)^2
(a%8)^2 ^ (a>>(a%8)^8)
(a%8)^2 ^ (a>>(a%8)^8) ^ 8
(a%8)^2 ^ (a>>(a%8)^8) ^ 8 % 8
b=(a%8)^2
b
a>>b
int(a/(2**b))
(a%8)^2
a>>(a%8)^2
((a%8)^2) ^ (a>>(a%8)^2)
(((a%8)^2) ^ (a>>(a%8)^2)) ^ 8
(((a%8)^2) ^ (a>>(a)^2)) ^ 8
(((a%8)^2) ^ (a>>(a%8)^2)) ^ 8
b = a%8^2
b
c=a>>b
c
b^c
b^c^8
a>>b
a/(2**b)
1^8
9%8
a
bin(17)
a
b=a%8
b
b=b^2
b
c=int(a/(2**b))
c
b ^ c
b ^ c ^ 3
(((a%8)^2) ^ (a>>(a%8)^2)) ^ 3
b ^ c ^ 8
(((a%8)^2) ^ (a>>(a)^2)) ^ 3
(((a%8)^2) ^ (a>>(a%8)^2)) ^ 3
(((a%8)^2) ^ (a>>a^2)) ^ 3
(((A%8)^2) ^ (A>>A^2)) ^ 3
A
b = A%8
b
b = b ^ 2
b
c = int(A/(2**b))
c
c = int(A>>b)
c
 int(a>>b)
int(a>>b)
b
a
format(a, "016b")
format(a<<3, "016b")
format(a<<3+5, "016b")
format((a<<3)+5, "016b")
a2 = (a<<3)+5
(((a2%8)^2) ^ (a2>>a2^2)) ^ 3
format(a, "016b")
(((a%8)^2) ^ (a>>a^2)) ^ 3
    def my_ops(a):
        return (((a % 8) ^ 2) ^ (a >> a ^ 2)) ^ 3

def my_ops(a):
    return (((a % 8) ^ 2) ^ (a >> a ^ 2)) ^ 3
my_ops(1)
my_ops(2)
my_ops(3)
my_ops(4)
my_ops(5)
(((a%8)^2) ^ (a>>a^2)) ^ 3
def my_ops2(a):
     (((a%8)^2) ^ (a>>a^2)) ^ 3
my_ops2(1)
def my_ops2(a):
     return (((a%8)^2) ^ (a>>a^2)) ^ 3
my_ops2(1)
my_ops2(2)
my_ops2(3)
a3=3
b = a%8
b ^ 2
b = a3%8
b
b ^ 2
a3/(2**1)
int(a3/(2**1))
a3>>1
c = a3>>1
1 ^ c
0 ^ 3
(((a3%8)^2) ^ (a3>>a3^2)) ^ 3
((a3%8)^2)
(((a3%8)^2) ^ (a3>>a3%8^2)) ^ 3
(((a3%8)^2) ^ (a3>>(a3%8)^2)) ^ 3
(((a3%8)^2) ^ (a3>>(a3%8)^2))
(a3>>(a3%8)^2))
(a3>>(a3%8)^2)
(((a3%8)^2) ^ (a3>>(a3%8))) ^ 3
(((a3%8)^2) ^ (a3>>(a3%8)))
c
(((a3%8)^2) ^ (a3>>((a3%8)^2)))
(((a3%8)^2) ^ (a3>>((a3%8)^2))) ^ 3
def f(a):
    return (((a%8)^2) ^ (a>>((a%8)^2))) ^ 3
f
f(0)
for i in range(10):
    print(f(i))
1<<3
(1<<3) + 3
f(11)
from day-17.part2 import *
from day-17.main import *
from .part2 import *
from .main import *
f(2)
from .main import *
f(2)
from .part2 import *
from part2 import *
f(2)
for i in range(10):
    print(f(i))
for i in range(10):
    print(f"{i}->{f(i)}")
for i in range(20):
    print(f"{i}->{f(i)}")
ops = "2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0".split(",")
run(ops, 13, 0, 0)
ops
int("011011001", 2)
run(ops, 217, 0, 0)
run(ops, 27575648, 0, 0)
ops = map(int,"2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0".split(","))
run(ops, 27575648, 0, 0)
ops = list(ops)
run(ops, 27575648, 0, 0)
run(ops, 217, 0, 0)
int("011011001", 2)
int("1011011001", 2)
run(ops, 729, 0, 0)
run(ops, 0, 0, 0)
run(ops, 1, 0, 0)
run(ops, 2, 0, 0)
run(ops, 3, 0, 0)
run(ops, 14, 0, 0)
run(ops, 17, 0, 0)
format(17,"08b")
int("00010101", 2)
run(ops, 21, 0, 0)
for i in range(20):
    run(ops, i, 0, 0)
ops
a
for i in range(40):
    run(ops, i, 0, 0)
001000
for i in range(1000):
    r = run(ops, i, 0, 0)
    if r.startswith("0,3"):
        print(i)
        print(r)
bin(541)
for i in range(1000):
    r = run(ops, i, 0, 0)
    if r.startswith("5,5"):
        print(i)
        print(r)
for i in range(100000):
    r = run(ops, i, 0, 0)
    if r.startswith("5,5,0,3"):
        print(i)
        print(r)
34665
bin(34665)
for i in range(100000):
    r = run(ops, i, 0, 0)
    if r.startswith("1,3,5,5"):
        print(i)
        print(r)
bin(2330)
run(ops, int("001000011101101001011010",2), 0, 0)
for i in range(100000):
    r = run(ops, i, 0, 0)
    if r.startswith("4,1,1,3"):
        print(i)
        print(r)
for i in range(1000000):
    r = run(ops, i, 0, 0)
    if r.startswith("4,1,1,3,5"):
        print(i)
        print(r)
bin(149310)
run(ops, int("001000011101100100011100111110",2), 0, 0)
bin(149302)
run(ops, int("001000011101100100011100110110",2), 0, 0)
for i in range(10000000):
    r = run(ops, i, 0, 0)
    if r.startswith("4,1,1,3,5,5,0"):
        print(i)
        print(r)
for i in range(1000000):
    r = run(ops, i, 0, 0)
    if r.startswith("4,1,1,3,5,5"):
        print(i)
        print(r)
for i in range(1000000):
    r = run(ops, i, 0, 0)
    if r.startswith("7,5,4,1,1,3"):
        print(i)
        print(r)
bin(262475)
for i in range(1000000):
    r = run(ops, i, 0, 0)
    if r.startswith("1,2,7,5"):
        print(i)
        print(r)
bin(21234)
for i in range(100000):
    r = run(ops, i, 0, 0)
    if r.startswith("2,4,1,2"):
        print(i)
        print(r)
bin()48628
bin(48628)
run(ops, int("001000011101101001011010000000101001011110111110100",2), 0, 0)
run(ops, int("001000011101101001011010000101001011110111110100",2), 0, 0)
run(ops, int("0010000111011010010110100001010010111101 11110100",2), 0, 0)
run(ops, int("001000011101101001011010000101001011110111110100",2), 0, 0)
for i in range(100000):
    r = run(ops, i, 0, 0)
    if r.startswith("4,1,3"):
        print(i)
        print(r)
for i in range(100000):
    r = run(ops, i, 0, 0)
    if r.startswith("4,1,3,5,5"):
        print(i)
        print(r)
bin(18657)
for i in range(100000):
    r = run(ops, i, 0, 0)
    if r.startswith("4,1,1,3,5,5"):
        print(i)
        print(r)
for i in range(1000000):
    r = run(ops, i, 0, 0)
    if r.startswith("4,1,1,3,5,5"):
        print(i)
        print(r)
bin(544773)
run(ops, int("001000011101101001101000000000101011110111110100",2), 0, 0)
int("001000011101101001101000000000101011110111110100",2)
int("")
int("111111111111111", 2)
int("111111111111111", 2)
int("111111111111111")
int("111111111111111", 2)
start="001000011101101001"
end="011110111110100"
for i in range(32767+1):
    a = int(start + format(i, "015b") + end)
    r = run(ops, i, 0, 0)
    if r == "2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0":
        print("found result")
        print(a)
for i in range(2**15):
    a = int(start + format(i, "015b") + end)
    r = run(ops, a, 0, 0)
    if r == "2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0":
        print("found result")
        print(a)
start
format(1, "015b")
run(ops, int("001000011101101001101000000000101011110111110100",2), 0, 0)
end="110111110100"
for i in range(2**18):
    a = int(start + format(i, "018b") + end)
    r = run(ops, a, 0, 0)
    if r == "2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0":
        print("found result")
        print(a)

r
a
for i in range(2**18):
    a = int(start + format(i, "018b") + end, 2)
    r = run(ops, a, 0, 0)
    if r == "2,4,1,2,7,5,4,1,1,3,5,5,0,3,3,0":
        print("found result")
        print(a)

run(ops, 37221261688308, 0, 0)

