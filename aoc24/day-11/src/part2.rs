use std::collections::HashMap;
use std::sync::Mutex;
use lazy_static::lazy_static;

lazy_static! {
    static ref CACHE_RULE1: Mutex<HashMap<u64, Vec<u64>>> = Mutex::new(HashMap::new());
    static ref CACHE_BETTER_RULE2: Mutex<HashMap<(u64, usize), Vec<u64>>> = Mutex::new(HashMap::new());
    static ref CACHE_RULE2: Mutex<HashMap<String, Vec<u64>>> = Mutex::new(HashMap::new());
    static ref CACHE_RULE3: Mutex<HashMap<u64, Vec<u64>>> = Mutex::new(HashMap::new());
}

fn rule1(stone: u64) -> Vec<u64> {
    let mut cache = CACHE_RULE1.lock().unwrap();
    if let Some(result) = cache.get(&stone) {
        return result.clone();
    }
    let result = vec![1];
    cache.insert(stone, result.clone());
    result
}

fn better_rule2(stone: u64, n: usize) -> Vec<u64> {
    let mut cache = CACHE_BETTER_RULE2.lock().unwrap();
    if let Some(result) = cache.get(&(stone, n)) {
        return result.clone();
    }
    let half = n / 2;
    let result = vec![stone / 10_u64.pow(half as u32), stone % 10_u64.pow(half as u32)];
    cache.insert((stone, n), result.clone());
    result
}

fn rule2(stone_str: &str) -> Vec<u64> {
    let mut cache = CACHE_RULE2.lock().unwrap();
    if let Some(result) = cache.get(stone_str) {
        return result.clone();
    }
    let half = stone_str.len() / 2;
    let result = vec![
        stone_str[..half].parse::<u64>().unwrap(),
        stone_str[half..].parse::<u64>().unwrap(),
    ];
    cache.insert(stone_str.to_string(), result.clone());
    result
}

fn rule3(stone: u64) -> Vec<u64> {
    let mut cache = CACHE_RULE3.lock().unwrap();
    if let Some(result) = cache.get(&stone) {
        return result.clone();
    }
    let result = vec![stone * 2024];
    cache.insert(stone, result.clone());
    result
}


pub fn process(_input: &str) -> miette::Result<String> {
    let mut numbers: Vec<u64> = _input
        .split_whitespace()
        .map(|s| s.parse::<u64>().unwrap())
        .collect();


    let n_blinks = 75;
    for blink in 0..n_blinks {
        println!("Blink: {}", blink);
        let mut new_numbers = Vec::new();
        for number in &numbers {
            if *number == 0 {
                new_numbers.extend(rule1(*number));
            } else if number.to_string().len() % 2 == 0 {
                new_numbers.extend(better_rule2(*number, number.to_string().len()));
            } else {
                new_numbers.extend(rule3(*number));
            }
        }
        numbers = new_numbers;
    }

    Ok(numbers.len().to_string())

}