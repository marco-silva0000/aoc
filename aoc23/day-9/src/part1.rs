fn differ(values: Vec<i32>) -> Vec<i32> {
    let mut iter = values.iter();
    let mut last = iter.next().unwrap();
    let mut result = vec![];
    for value in iter {
        result.push(value - last);
        last = value;
    }
    if result.is_empty() {
        result.push(0);
    }
    return result.to_vec();
}

fn spread(values: Vec<i32>) -> Vec<i32> {
    let mut cloned = values.clone();
    if !values.iter().all(|value| *value == 0) {
        let mut next_list = differ(values.clone());
        next_list = spread(next_list);
        let to_prepend = cloned.last().unwrap() + next_list.last().unwrap();
        cloned.push(to_prepend);
    }
    return cloned;
}

pub fn process(input: &str) -> miette::Result<String> {
    let result = input
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|number| number.parse::<i32>().unwrap())
                .collect::<Vec<i32>>()
        })
        .into_iter()
        .map(|values| spread(values).last().unwrap().to_owned())
        .sum::<i32>();
    return Ok(result.to_string());
}
