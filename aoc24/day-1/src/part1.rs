use itertools::Itertools;
use std::convert::TryFrom;

pub fn process(_input: &str) -> miette::Result<String> {
    let mut v1 = vec![];
    let mut v2 = vec![];
    for line in _input.lines() {
        let mut values = line.split_whitespace();
        v1.push(values.next().unwrap().parse::<i32>().unwrap());
        v2.push(values.next().unwrap().parse::<i32>().unwrap());
    }
    v1.sort();
    v2.sort();
    let result: i32 = v1.iter().zip(v2.iter()).map(|(l, r)| (l - r).abs()).sum();
    println!("{:?}", result);
    Ok(result.to_string())
}
