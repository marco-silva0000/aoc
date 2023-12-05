use itertools::Itertools;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    if !current_dir.ends_with("/4") {
        current_dir += "/4"
    }
    let contents = fs::read_to_string(current_dir + "/input.txt").expect("couldn't read file");
    let lines = contents.lines();

    // println!("{:?}", lines);
    let result = lines.into_iter().map(|l| {
        // println!("{:?}", l);
        // Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        l.split_once(':')
            .unwrap()
            .1
            .split('|')
            .map(|part| {
                // println!("{:?}", part);
                part.split_whitespace()
                    .fold(HashSet::new(), |mut acc, val| {
                        // println!("{:?}", val);
                        acc.insert(val.parse::<usize>().unwrap());
                        acc
                    })
            })
            .into_iter()
            .reduce(|acc, val| {
                // println!("{:?} {:?}", acc, val);
                acc.intersection(&val).cloned().collect()
            })
            .unwrap()
            .iter()
            .count()
    });
    let part1 = result
        .clone()
        .filter(|x| *x > 0)
        .map(|x| 2_i32.pow(x as u32 - 1))
        .sum::<i32>();
    println!("{:?}", part1);
    let mut part2_result: HashMap<usize, usize> = HashMap::new();

    result.clone().enumerate().for_each(|(i, x)| {
        // println!("Card {:?} has {:?} matching numbers, so you win one copy each of the next {:?} cards: cards {:?}", i+1, x, x, i + 2..i + 2 + x);
        *part2_result.entry(i + 1).or_insert(0) += 1;
        if x > 0 {
            let value_to_insert = part2_result.entry(i + 1).or_insert(1).to_owned();
            for j in i + 1..i + 1 + x {
                // println!("inserting {:?} on {:?}",value_to_insert, j + 1);
                *part2_result.entry(j + 1).or_insert(0) += value_to_insert;
            }
        }
    });
    println!("{:?}", result.clone().collect::<Vec<usize>>());

    println!("{:?}", part2_result.values().sum::<usize>());
}
