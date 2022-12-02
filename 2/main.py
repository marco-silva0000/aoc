f = open('2/input.txt')

ROCK = 'rock'
PAPER = 'paper'
SCISSORS = 'scissors'

WIN = 'Z'
DRAW = 'Y'
LOSE = 'X'


def to_tool(char: str):
    if char in ['A', 'X']:
        return ROCK
    if char in ['B', 'Y']:
        return PAPER
    if char in ['C', 'Z']:
        return SCISSORS


def battle(p1, p2) -> int:
    if p1 == p2:
        return 1
    if p1 == ROCK:
        if p2 == PAPER:
            return 2
        else:
            return 0
    if p1 == PAPER:
        if p2 == SCISSORS:
            return 2
        else:
            return 0
    if p1 == SCISSORS:
        if p2 == ROCK:
            return 2
        else:
            return 0

def tool_score(tool):
    if tool == ROCK:
        return 1
    elif tool == PAPER:
        return 2
    else:
        return 3


def play(opponent: str, me:str):
    score = tool_score(me) + battle(opponent, me) * 3
    return score

nemesis_map = {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}

def find_tool(opponent: str, outcome:str):
    if outcome == DRAW:
        return opponent
    if outcome == LOSE:
        return nemesis_map[nemesis_map[opponent]]
    else:
        return nemesis_map[opponent]


def play2(opponent: str, outcome:str):
    my_tool = find_tool(opponent, outcome)
    score = tool_score(my_tool) + battle(opponent, my_tool) * 3
    return score


scores = []
scores2 = []
for l in f.readlines():
    scores.append(play(to_tool(l[0]), to_tool(l[2])))
    scores2.append(play2(to_tool(l[0]), l[2]))

print(sum(scores))
print(sum(scores2))


f.close()
