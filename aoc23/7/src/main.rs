use itertools::Itertools;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::ops::Index;

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
    bid: usize,
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
        Self {
            cards: hand.chars().collect(),
            rank,
            bid,
        }
    }
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    if !current_dir.ends_with("/7") {
        current_dir += "/7"
    }
    let contents = fs::read_to_string(current_dir + "/input2.txt").expect("couldn't read file");
    let lines = contents.lines();

    // println!("{:?}", lines);
    let part1_rank = "23456789TJQKA";
    let sorted_counts = vec![(
        (5,),
        (4, 1),
        (3, 2),
        (3, 1, 1),
        (2, 2, 1),
        (2, 1, 1, 1),
        (1, 1, 1, 1, 1),
    )];
    // line has 7KAK7 63

    let hands = lines
        .into_iter()
        .map(|l| {
            // println!("{:?}", l);
            // Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            l.split_once(' ').unwrap()
        })
        .map(|(hand, bid)| (hand, bid.parse::<usize>().unwrap()));
    let part1 = hands
        .clone()
        .map(|(hand, bid)| Hand::new(hand, bid))
        .sorted_by(|a, b| {
            let a_rank = a.rank as usize;
            let b_rank = b.rank as usize;
            if a_rank == b_rank {
                todo!();
                // return a.cards.iter().cmp(&b.bid);
            }
            a_rank.cmp(&b_rank)
        });

    // .sorted_by(|a, b| {
    //     println!("a {:?}", a.0);
    //     todo!();
    //     // sorted_counts
    //     //     .index::<usize>(a.0)
    //     //     .cmp(&sorted_counts.index(b.0))
    // });
    println!("part1: {:?}", part1);
}
