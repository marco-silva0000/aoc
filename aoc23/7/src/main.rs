use itertools::Itertools;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::ops::Index;

const part1_rank: &str = "23456789TJQKA";
const part2_rank: &str = "J23456789TQKA";

#[derive(Debug, Copy, Clone, PartialEq, Eq, PartialOrd, Ord)]
enum HandRank {
    HighCard = 1,
    OnePair = 2,
    TwoPairs = 3,
    ThreeOfAKind = 4,
    FullHouse = 5,
    FourOfAKind = 6,
    FiveOfAKind = 7,
}

#[derive(Debug)]
struct Hand {
    cards: Vec<char>,
    rank: HandRank,
    rank2: HandRank,
    bid: usize,
    part1_power: Vec<usize>,
    part2_power: Vec<usize>,
}

impl Hand {
    fn new(hand: &str, bid: usize) -> Hand {
        use HandRank::*;
        let counts = hand.chars().counts();
        let values = counts.values().sorted().join("");
        let rank = match values.as_str() {
            "5" => FiveOfAKind,
            "14" => FourOfAKind,
            "23" => FullHouse,
            "113" => ThreeOfAKind,
            "122" => TwoPairs,
            "1112" => OnePair,
            "11111" => HighCard,
            value => unreachable!("invalid hand `{}`", value),
        };
        let jokers = counts.get(&'J').unwrap_or(&0);
        let mut counts2 = counts.clone();
        // println!("counts: {:?}", counts);
        counts2.remove(&'J');
        let values2 = counts2.values().sorted().join("");
        // println!("values2: {:?}", values2);

        let rank2 = if jokers == &5 {
            FiveOfAKind
        } else {
            let mut final_thingy = String::new();
            let (rest, last) = values2.as_str().split_at(values2.len() - 1);
            // println!("rest: {:?}, last: {:?}", rest, last);
            let last_with_joker =
                (last.parse::<usize>().or::<usize>(Ok(0)).unwrap().clone() + jokers);
            // println!("last_with_joker: {:?}", last_with_joker);
            // println!(
            //     "last_with_joker: {:?}",
            //     last_with_joker.to_string().as_str()
            // );
            final_thingy.push_str(rest);
            final_thingy.push_str(last_with_joker.to_string().as_str());
            // println!("final_thingy: {:?}", final_thingy);

            match final_thingy.as_str() {
                "5" => FiveOfAKind,
                "14" => FourOfAKind,
                "23" => FullHouse,
                "113" => ThreeOfAKind,
                "122" => TwoPairs,
                "1112" => OnePair,
                "11111" => HighCard,
                value => unreachable!("invalid hand `{}`", value),
            }
        };
        let part1_power = hand.chars().map(|c| part1_rank.find(c).unwrap()).collect();
        let part2_power = hand.chars().map(|c| part2_rank.find(c).unwrap()).collect();
        Self {
            cards: hand.chars().collect(),
            rank,
            rank2,
            bid,
            part1_power,
            part2_power,
        }
    }
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    if !current_dir.ends_with("/7") {
        current_dir += "/7"
    }
    let contents = fs::read_to_string(current_dir + "/input.txt").expect("couldn't read file");
    let lines = contents.lines();

    let hands = lines
        .into_iter()
        .map(|l| l.split_once(' ').unwrap())
        .map(|(hand, bid)| (hand, bid.parse::<usize>().unwrap()));
    let part1 = hands
        .clone()
        .map(|(hand, bid)| Hand::new(hand, bid))
        .sorted_by(|a, b| {
            let a_rank = a.rank as usize;
            let b_rank = b.rank as usize;
            if a_rank == b_rank {
                for i in 0..5 {
                    if a.part1_power[i] != b.part1_power[i] {
                        return a.part1_power[i].cmp(&b.part1_power[i]);
                    }
                }
            }
            a_rank.cmp(&b_rank)
        })
        .enumerate()
        .map(|(i, hand)| (hand.bid * (i + 1)))
        .sum::<usize>();

    // .sorted_by(|a, b| {
    //     println!("a {:?}", a.0);
    //     todo!();
    //     // sorted_counts
    //     //     .index::<usize>(a.0)
    //     //     .cmp(&sorted_counts.index(b.0))
    // });
    println!("part1: {:?}", part1);

    let part2 = hands
        .clone()
        .map(|(hand, bid)| Hand::new(hand, bid))
        .sorted_by(|a, b| {
            let a_rank = a.rank2 as usize;
            let b_rank = b.rank2 as usize;
            if a_rank == b_rank {
                for i in 0..5 {
                    if a.part2_power[i] != b.part2_power[i] {
                        return a.part2_power[i].cmp(&b.part2_power[i]);
                    }
                }
            }
            a_rank.cmp(&b_rank)
        })
        .enumerate()
        .map(|(i, hand)| (hand.bid * (i + 1)))
        .sum::<usize>();
    println!("part2: {:?}", part2);
}
