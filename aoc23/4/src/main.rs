use itertools::Itertools;
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
    let result = lines
        .into_iter()
        .map(|l| {
            // println!("{:?}", l);
            // Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            // add max of each color to numbers
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
        })
        .filter(|x| *x > 0)
        .map(|x| 2_i32.pow(x as u32 - 1))
        .sum::<i32>();

    println!("{:?}", result);
}
