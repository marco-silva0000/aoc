use regex::Regex;
// cargo run -r -p aoc24_ --bin part2
pub fn process(_input: &str) -> miette::Result<String> {
    let re = Regex::new(r"mul\((?<left>\d+)\,(?<right>\d+)\)").unwrap();
    let dont_do = Regex::new(r"don't\(\).*?do\(\)").unwrap();
    let data = _input
        .chars()
        .filter(|c| *c != '\n')
        .map(|c| c as char)
        .collect::<String>();
    let dontdodata = dont_do.replace_all(&data, "");
    let result: i32 = re
        .captures_iter(&dontdodata)
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
        // .inspect(|values| println!("sum({:?},{:?})", values.0, values.1))
        .map(|values| values.0 * values.1)
        .sum();
    Ok(result.to_string())
}
