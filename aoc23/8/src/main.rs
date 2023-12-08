use itertools::Itertools;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    if !current_dir.ends_with("/7") {
        current_dir += "/7"
    }
    let contents = fs::read_to_string(current_dir + "/input2.txt").expect("couldn't read file");
    let lines = contents.lines();

    // println!("{:?}", lines);
    let result = lines.into_iter().map(|l| {
        // println!("{:?}", l);
        // Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        l.split_once(' ')
    })
}
