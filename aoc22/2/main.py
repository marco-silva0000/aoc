from enum import Enum


f = open("2/input.txt")


class Tool(str, Enum):
    ROCK = "rock"
    PAPER = "paper"
    SCISSORS = "scissors"

    @staticmethod
    def from_str(char: str):
        if char in ["A", "X"]:
            return Tool.ROCK
        elif char in ["B", "Y"]:
            return Tool.PAPER
        elif char in ["C", "Z"]:
            return Tool.SCISSORS
        else:
            raise ValueError("Invalid tool code")


class Outcome(str, Enum):
    WIN = "Z"
    DRAW = "Y"
    LOSE = "X"


nemesis_map = {
    Tool.ROCK: Tool.PAPER,
    Tool.PAPER: Tool.SCISSORS,
    Tool.SCISSORS: Tool.ROCK,
}


def battle(p1: Tool, p2: Tool) -> int:
    if p1 == p2:
        return 0
    if p1 == nemesis_map[p2]:
        return -1
    else:
        return 1


def tool_score(tool: Tool):
    if tool == Tool.ROCK:
        return 1
    elif tool == Tool.PAPER:
        return 2
    else:
        return 3


def play(opponent: Tool, me: Tool):
    score = tool_score(me) + (battle(opponent, me) + 1) * 3
    return score


def find_tool(opponent: Tool, outcome: Outcome):
    if outcome == Outcome.DRAW:
        return opponent
    if outcome == Outcome.LOSE:
        return nemesis_map[nemesis_map[opponent]]
    else:
        return nemesis_map[opponent]


def play2(opponent: Tool, outcome: Outcome):
    my_tool = find_tool(opponent, outcome)
    score = tool_score(my_tool) + (battle(opponent, my_tool) + 1) * 3
    return score


scores = []
scores2 = []
for l in f.readlines():
    scores.append(play(Tool.from_str(l[0]), Tool.from_str(l[2])))
    scores2.append(play2(Tool.from_str(l[0]), Outcome(l[2])))

print(sum(scores))
print(sum(scores2))


f.close()
