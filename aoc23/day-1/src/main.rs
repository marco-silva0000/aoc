use std::env;
use std::fs;

fn match_str_to_int(s: &str) -> Option<u32> {
    match s {
        "one" => Some(1),
        "two" => Some(2),
        "three" => Some(3),
        "four" => Some(4),
        "five" => Some(5),
        "six" => Some(6),
        "seven" => Some(7),
        "eight" => Some(8),
        "nine" => Some(9),
        "1" => Some(1),
        "2" => Some(2),
        "3" => Some(3),
        "4" => Some(4),
        "5" => Some(5),
        "6" => Some(6),
        "7" => Some(7),
        "8" => Some(8),
        "9" => Some(9),
        _ => None,
    }
}

fn reversed_match_str_to_int(s: &str) -> Option<u32> {
    match s {
        "eno" => Some(1),
        "owt" => Some(2),
        "eerht" => Some(3),
        "ruof" => Some(4),
        "evif" => Some(5),
        "xis" => Some(6),
        "neves" => Some(7),
        "thgie" => Some(8),
        "enin" => Some(9),
        "1" => Some(1),
        "2" => Some(2),
        "3" => Some(3),
        "4" => Some(4),
        "5" => Some(5),
        "6" => Some(6),
        "7" => Some(7),
        "8" => Some(8),
        "9" => Some(9),
        _ => None,
    }
}

fn process_line(l_slice: &[u8], matcher_function: &dyn Fn(&str) -> Option<u32>) -> u32 {
    let mut left_digit: u32 = 0;
    let mut last_5_chars: Vec<u8> = vec![0; 5];
    for c in l_slice.iter() {
        // println!("{:?}", *c as char);
        // println!(
        //     "{:?}",
        //     last_5_chars.iter().map(|x| *x as char).collect::<String>()
        // );
        if let Some(num) = matcher_function(
            &last_5_chars[0..5]
                .iter()
                .map(|x| *x as char)
                .collect::<String>(),
        ) {
            left_digit = num;
            break;
        } else if let Some(num) = matcher_function(
            &last_5_chars[1..5]
                .iter()
                .map(|x| *x as char)
                .collect::<String>(),
        ) {
            left_digit = num;
            break;
        } else if let Some(num) = matcher_function(
            &last_5_chars[2..5]
                .iter()
                .map(|x| *x as char)
                .collect::<String>(),
        ) {
            left_digit = num;
            break;
        } else if let Some(num) = matcher_function(&(*c as char).to_string()) {
            left_digit = num;
            break;
        } else {
            last_5_chars.push(*c);
            if last_5_chars.len() > 5 {
                last_5_chars.remove(0);
            }
        }
    }
    left_digit
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let module_path = module_path!();
    let (_, day) = module_path.split_once('_').unwrap();
    let dir_str = "/day-".to_string() + day;
    if !current_dir.ends_with(&dir_str) {
        current_dir += &dir_str;
    }
    println!("{:?}", current_dir);
    let contents = fs::read_to_string(current_dir + "/input.txt").expect("couldn't read file");
    let lines = contents.lines();

    // println!("{:?}", lines);

    let mut numbers: Vec<u32> = Vec::new();
    for l in lines.into_iter() {
        println!("{:?}", l);
        // converst l into slice
        let l_slice = l.trim().as_bytes();
        let left_digit = process_line(l_slice, &match_str_to_int);
        let mut slice_copy = l_slice.to_vec();
        slice_copy.reverse();
        let right_digit = process_line(slice_copy.as_slice(), &reversed_match_str_to_int);
        println!("{:?}{:?}", left_digit, right_digit);
        numbers.push(left_digit * 10 + right_digit);
    }
    // println!("{:?}", numbers);
    println!("{:?}", numbers.iter().sum::<u32>());
}
