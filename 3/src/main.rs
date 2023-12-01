use itertools::Itertools;
use std::env;
use std::fs;

fn get_score(c: char) -> i32 {
    let mut score = c as i32;

    if score <= 90 {
        // uppercase
        score += -64 + 26;
    } else {
        score -= 96;
    }
    // println!("{:?}=>{:?}->{:?}", c as i32, c, score);
    return score;
}

fn find_common(first: &str, second: &str) -> Option<char> {
    // println!("{:?}|{:?}", first, second);
    for c in first.chars() {
        if second.contains(c) {
            return Some(c);
        }
    }
    return None;
}

fn find_commons(first: &str, second: &str) -> Vec<char> {
    let mut result: Vec<char> = Vec::new();
    // println!("{:?}|{:?}", first, second);
    for c in first.chars() {
        if second.contains(c) {
            result.extend([c]);
        }
    }
    // println!("{:?}", result);
    return result;
}

fn calc_first(line: &str) -> i32 {
    let half = line.len() / 2;
    let common = find_common(&line[..half], &line[half..]).unwrap();
    return get_score(common);
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let today = "/3";
    if !current_dir.ends_with(today) {
        current_dir += today
    }
    let contents = fs::read_to_string("3/input.txt").expect("couldn't read file");
    let mut first: Vec<i32> = vec![];
    let mut second: Vec<i32> = vec![];
    let mut third: Vec<&str> = vec![];
    // let mut second: Vec<i32> = vec![];
    let mut lines = contents.lines();
    loop {
        let first_bag_option = lines.next();
        let first_bag = match first_bag_option {
            Some(bag) => bag,
            None => break,
        };
        let second_bag = lines.next().unwrap();
        let third_bag = lines.next().unwrap();
        first.extend([calc_first(&first_bag)]);
        first.extend([calc_first(&second_bag)]);
        first.extend([calc_first(&third_bag)]);
        let temp = find_commons(first_bag, second_bag);
        let temp_string: String = temp.into_iter().collect();
        let temp2 = find_commons(&temp_string, third_bag);
        let badge: String = temp2.clone().into_iter().collect();
        second.extend([get_score(badge.chars().next().unwrap())]);
        third.extend([first_bag]);
        third.extend([second_bag]);
        third.extend([third_bag]);
    }
    let one_liner: Vec<&str> = third.into_iter().map(|x| x.trim()).collect();
    // println!("{:?}", one_liner);
    let ol2 = one_liner
        .as_slice()
        .chunks(3)
        .collect_tuple()
        .map(move |it| -> i32 {
            let (a, b, c) = it;
            println!("{:?}", a);
            println!("{:?}", b);
            println!("{:?}", c);
            // let y = find_commons(find_commons(a.into_iter().collect(), b), c)
            //     .clone()
            //     .into_iter()
            //     .collect();
            1
            // .into_iter()
            // .collect()
        });
    println!("{:?}", ol2);

    let sum: i32 = first.iter().sum();
    let sum2: i32 = second.iter().sum();
    // println!("{:?}", first);
    // println!("{sum}");
    // println!("{:?}", second);
    // println!("{sum2}");
}
