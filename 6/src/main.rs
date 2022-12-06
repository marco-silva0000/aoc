use std::collections::HashSet;
use std::env;
use std::fs;

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let today = "/6";
    if !current_dir.ends_with(today) {
        current_dir += today
    }
    let contents = fs::read_to_string("6/input.txt").expect("couldn't read file");
    let input = contents.as_str();
    println!("{:?}", input);
    let inter = input.chars().collect::<Vec<char>>();
    let window_size = 4;
    let window_size2 = 14;
    let mut packet_start = 0;
    let mut windows = inter.windows(window_size);
    for i in 0..input.len() {
        let part = windows.next().unwrap();
        let mut uniques = HashSet::new();
        part.iter().for_each(|c: &char| {
            uniques.insert(c);
        });
        if uniques.len() == window_size {
            packet_start = i + window_size;
            println!("{:?}", part);
            println!("{:?}", packet_start);
            break;
        }
    }
    let mut windows2 = inter[packet_start..].windows(window_size2);
    for i in 0..input.len() {
        let part = windows2.next().unwrap();
        let mut uniques = HashSet::new();
        part.iter().for_each(|c: &char| {
            uniques.insert(c);
        });
        if uniques.len() == window_size2 {
            println!("{:?}", part);
            println!("{:?}", packet_start + i + window_size2);
            break;
        }
    }
}
