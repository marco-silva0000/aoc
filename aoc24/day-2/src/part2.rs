use nom::multi::count;

// cargo run -r -p aoc24_ --bin part2
fn analyse(line: &Vec<i32>) -> bool {
    println!("{:?}", line);
    let diff = line.windows(2).map(|window| window[1] - window[0]);
    let count = diff.clone().count();
    let no_greater_than_3 = diff.clone().filter(|num| num.abs() <= 3).count() == count;
    let all_negative = diff.clone().filter(|num| num < &0).count() == count;
    let all_positive = diff.clone().filter(|num| num > &0).count() == count;
    let any_constant = diff.filter(|num| *num == 0).count() > 0;
    let is_monotonic = all_negative || all_positive;
    println!("count {:?}", count);
    println!("no_greater_than_3 {:?}", no_greater_than_3);
    println!("all_positive {:?}", all_positive);
    println!("all_negative {:?}", all_negative);
    println!("any_constant {:?}", any_constant);
    println!("is_monotonic {:?}", is_monotonic);
    no_greater_than_3 && is_monotonic && !any_constant
}

pub fn process(_input: &str) -> miette::Result<String> {
    let mut result = 0;
    for line in _input.lines() {
        let values = line
            .split_whitespace()
            .map(|value| value.parse::<i32>().unwrap().clone())
            .into_iter()
            .collect();
        if analyse(&values) {
            result += 1;
        } else {
            for i in 0..values.len() {
                let mut new_values = values.clone();
                _ = new_values.remove(i);
                if analyse(&new_values) {
                    result += 1;
                    break;
                }
            }
        }
    }
    println!("result {:?}", result);
    Ok(result.to_string())
}
