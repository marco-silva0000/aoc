use std::collections::HashSet;
use std::env;
use std::fs;

fn is_unique(part: &[char]) -> bool {
    let mut uniques = HashSet::new();
    part.iter().for_each(|c: &char| {
        uniques.insert(c);
    });
    return uniques.len() == part.len();
}

fn find_non_repeating_sequence(input: &str, window_size: usize) -> Option<(usize, String)> {
    for (i, part) in input.chars().collect::<Vec<char>>().windows(window_size).enumerate() {
        if is_unique(part) {
            return Some((i + window_size, part.into_iter().collect::<String>()));
        }
    }
   return None;
}


fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let today = "/6";
    if !current_dir.ends_with(today) {
        current_dir += today
    }
    let contents = fs::read_to_string("6/input.txt").expect("couldn't read file");
    let input = contents.as_str();
    let (com_start, com_string) = find_non_repeating_sequence(input, 4).unwrap();
    let (message_start, message_string) = find_non_repeating_sequence(&input[com_start..], 14).unwrap();
    println!("{:?}", input);
    println!("{:?}", com_string);
    println!("{:?}", com_start);
    println!("{:?}", message_string);
    println!("{:?}", message_start + com_start);
}
