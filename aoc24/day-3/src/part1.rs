use regex::Regex;

pub fn process(_input: &str) -> miette::Result<String> {
    let re = Regex::new(r"mul\((?<left>\d+)\,(?<right>\d+)\)").unwrap();
    let data = _input
        .chars()
        .filter(|c| *c != '\n')
        .map(|c| c as char)
        .collect::<String>();
    let result: i32 = re
        .captures_iter(&data)
        .map(|capture| {
            (
                capture
                    .name("left")
                    .unwrap()
                    .as_str()
                    .parse::<i32>()
                    .unwrap(),
                capture
                    .name("right")
                    .unwrap()
                    .as_str()
                    .parse::<i32>()
                    .unwrap(),
            )
        })
        .map(|values| values.0 * values.1)
        .sum();
    Ok(result.to_string())
}
