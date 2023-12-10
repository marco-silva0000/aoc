from typing import List, Set, Dict, Tuple, Optional, Union

f = open("4/test.txt")
f = open("4/input.txt")


class Game:
    def __init__(
        self, game_id: int, winning_numbers: Set[int], my_numbers: Set[int], points: int
    ):
        self.game_id = game_id
        self.winning_numbers = winning_numbers
        self.my_numbers = my_numbers
        self.points = points

    def __repr__(self):
        return f"Game({self.game_id}, {self.winning_numbers}, {self.my_numbers} {self.points})"

    def __str__(self):
        return f"Game({self.game_id}, {self.winning_numbers}, {self.my_numbers} {self.points})"


part1 = 0
games = dict()
games_list = []
for l in f.readlines():
    l = l.strip()
    print(l)
    game_id, numbers = l.split(": ")
    game_id = game_id.removeprefix("Card ")
    game_id = int(game_id)
    winning_numbers, my_numbers = numbers.split(" | ")
    winning_numbers = set(map(int, filter(None, winning_numbers.split(" "))))
    my_numbers = set(map(int, filter(None, my_numbers.split(" "))))
    matching_numbers = winning_numbers.intersection(my_numbers)
    print(matching_numbers)
    if len(matching_numbers) > 0:
        points = pow(2, len(matching_numbers) - 1)
        print(f"points: {points}")
        part1 += points
    else:
        points = 0
    game = Game(game_id, winning_numbers, my_numbers, len(matching_numbers))
    games[game_id] = game
    games_list.append(game)

for index, game in enumerate(games_list):
    print(game)
    if game.points > 0:
        print(list(range(game.game_id + 1, game.game_id + 1 + game.points, 1)))
        for id_to_add in range(game.game_id + 1, game.game_id + 1 + game.points, 1):
            games_list.insert(index + 1, games[id_to_add])
print(part1)
print(len(games_list))
