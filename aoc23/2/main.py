
f = open("2/test.txt")
f = open("2/input.txt")

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14

class ValidationError(Exception):
    pass

def validate_draws(draws, check_max=True):
    max_red = 0
    max_green = 0
    max_blue = 0
    for draw in draws.split(";"):
        draw = draw.strip()
        # print(draw)
        for part in draw.split(","):
            part = part.strip()
            # print(part)
            number, color = part.split(" ")
            number = int(number)
            if color == "red":
                max_red = max(max_red, number)
                if check_max and number > MAX_RED:
                    print(f"invalid game id: {game_id}, because of RED")
                    raise ValidationError
            elif color == "green":
                max_green = max(max_green, number)
                if check_max and number > MAX_GREEN:
                    print(f"invalid game id: {game_id}, because of GREEN")
                    raise ValidationError
            elif color == "blue":
                max_blue = max(max_blue, number)
                if check_max and number > MAX_BLUE:
                    print(f"invalid game id: {game_id}, because of BLUE")
                    raise ValidationError
    return max_red, max_green, max_blue


valid_game_ids = []
valid_game_powers = []
for l in f.readlines():
    l = l.strip()
    print(l)
    game_id, draws = l.split(":")
    game_id = game_id.removeprefix("Game ")
    game_id = int(game_id)
    try:
        validate_draws(draws)
        valid_game_ids.append(game_id)
    except ValidationError:
        pass
    r,g,b = validate_draws(draws, check_max=False)
    valid_game_powers.append(r*g*b)

print(valid_game_ids)
print(sum(valid_game_ids))
print(valid_game_powers)
print(sum(valid_game_powers))

