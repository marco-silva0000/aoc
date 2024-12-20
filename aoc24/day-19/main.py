import os
from structlog import get_logger
import pytest

log = get_logger()

from .part1 import part1
from .part2 import part2


def parse(data: str):
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    lines = data.splitlines()
    values_list = []
    for line in lines:
        values_list.append(line)
    return values_list


def get_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    f = open(f"{current_dir}/input.txt")
    data = f.read()
    f.close()
    return data


if __name__ == "__main__":
    data = get_data()
    parsed_data = parse(data)
    print(part1(parsed_data))
    print(part2(parsed_data))


def run_part1(parsed_data):
    print(part1(parsed_data))


def run_part2(parsed_data):
    print(part2(parsed_data))


def test_part1():
    data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part1(parsed_data)
    assert result == "6"


def test_part2():
    data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "16"


def test_guubrggrburwrgbwurwubrugburwrubbgugbbguwgrbgubu_part2():
    data = """ggbwrgwu, bbbgru, wwbg, gbuuruwu, bwww, r, guw, gwgg, ggbuwwr, wwb, wrwggwr, wwrbuwu, bgrr, urugr, bww, g, wurb, gwug, ruwg, gubw, bgbbwr, gurubr, www, uwww, brug, bwgr, bbgu, gbguuww, bgu, bgrbbrg, bbu, bwuwg, bbg, bgr, rgu, rwbbb, bwrw, gwg, buuwg, bbbwuu, bbwgb, ggwwr, wrww, wgr, bwb, ugr, gbwgwgbu, wggug, wuu, rbuw, rggww, gwrguu, gru, gubu, wbgbw, uwru, gggrr, gwwuw, wbbwrr, rgg, wbwgubrr, ruwuug, bbuw, gwbwgwgr, gguwrugr, urrbgg, ubwr, wwu, gbw, ggwbu, rug, bgb, ruur, bwg, wbgrrbu, wrrguww, rrbw, brb, gbg, rrrugrb, rrr, rwr, rbg, grwurw, wurr, gguu, ubuug, bgguuwwr, bwu, wwr, ggr, brgg, bugbrgu, ggu, w, bbubrw, ug, uwrru, wbwgrbu, wb, wgw, ruwbrg, bw, burgrurb, bwgb, wgg, bwrbbrww, rbu, wgb, ubu, brwgggbb, wbgbg, brrgb, rwb, bbbggwb, uwgggw, rr, brubr, wur, ubgrwww, rgwwb, gug, rgwbw, br, gwgbu, wurbwb, ubuggw, gwbw, ugbr, bbb, gubuu, bgbb, gwubrrb, bwwubwgg, bgg, urww, gwrw, ggubug, wgu, gur, bbug, bgbbw, gurgbu, rgubbwr, urb, uurwgwb, urrwww, uuu, rbrgw, wugug, wbugr, rgruurug, b, wrrrrg, bggr, wgbu, wwgu, wwwgbb, guwbr, uuwrwbb, rbw, rrwr, wggu, gguru, bwbb, uwbbu, uuug, rbb, ugwwggb, rbr, bguu, ggrgr, bbwb, rwg, ugb, ubugwbb, wbbgbg, ruu, ubrrg, ru, ggb, ubwbwru, uuww, brggwb, gb, uggw, grw, ubbrww, bbuwgbu, buurwu, wrurg, uug, uuw, rbwrg, wuwgw, wbgrgbu, rwuwug, rbbbbug, wruru, wuw, wuugr, rg, bbr, ggg, rrrwbrgg, grgbg, uubbr, wwbu, bbrw, wwg, ururrb, wrg, brurwu, gbr, wugww, wrrw, wru, rbwr, bbrbggwg, rwbgb, rgwuwu, ggwu, uru, gbu, rgwu, guur, rgw, gugwu, brrw, wuwg, wgbg, ububu, uwuuu, urg, rur, uubbww, urr, gw, rruru, bu, rwwr, ugg, gubuw, uuuu, brbwubg, bugu, ubuu, rbbbuu, rb, wbb, bru, bgruw, wggw, rrbrb, uwu, urw, wrb, gbubwb, rugb, wrwu, bbbgrg, bbgrgw, wwur, urwg, ubwb, buwrur, rbwbrb, gub, uuwrbu, rwrgu, wrwbub, uwubu, ubb, rgrugub, bwbwu, wu, ubgwb, wrub, bggwuu, rru, gwbrg, rwrbb, bbuugr, uwr, bwur, ubgu, gwb, uuwgb, bbww, wwrubwu, gwur, gbrrgww, brgwb, guug, gwwwrr, grbgrgrb, brgu, rwww, rbgr, ugubugu, rwbuw, wrbgbww, brrurg, rgrb, rgb, wguurb, rwbu, brw, uwrgu, bug, rbguw, guu, rrgu, gwbbgg, burg, rguw, wwwruubu, ugu, grg, ugw, gbrg, urbub, gwr, wgww, wbg, ww, rburwgg, wg, gbwu, gwbr, bwgub, bub, rub, uurbbwr, rwu, rbrbbu, bbwwuww, brg, ur, bbbw, uwg, bbwgwbbw, guwb, rbbwubb, rwbwg, rwbg, wbr, bwr, wbu, rbgwb, rrg, rgwub, rbwuuu, uw, guub, wrw, gubbrgr, gbb, ggw, ubugw, rgwg, uggb, wgwr, bbw, buu, ubw, uwwuru, gbrubur, uwguu, grrbbru, gbwbugg, bwrwgu, ggbuuug, gwbwwu, ggbbr, rrb, grrru, ubbwg, bg, ub, rww, ubg, gww, gwru, uugubb, wwrugubr, rwwru, wwbw, ubrwg, wwuwww, wgwwwrwg, rw, rwrwru, wrwbb, guruw, buw, ggwwug, gwbbg, rgurgw, bwuww, gwu, grb, grbgu, urwru, bwru, bgw, bwrurbw, rwuu, uur, bwgubrb, ruw, rbwb, brwruw, gr, rbwg, uwub, gbbub, ubgwbuur, urgbgb, ubgr, grgbrw, wgbug, wug, bubg, gg, rrwggg, bubu, bb, rbug, bburbu, brr, ubr, grwgu, bur, wr, grr, rgwbrb, wbw, bgbr, bgbrb, rrw, bgwwgb, ggrwr, wbggbr, gubbrbw, bbwg, uwb

guubrggrburwrgbwurwubrugburwrubbgugbbguwgrbgubu"""
    parsed_data = parse(data)
    log.debug(parsed_data)
    result = part2(parsed_data)
    assert result == "4146963945"
