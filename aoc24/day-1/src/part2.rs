pub fn process(_input: &str) -> miette::Result<String> {
    let mut v1 = vec![];
    let mut v2 = vec![];
    for line in _input.lines() {
        let mut values = line.split_whitespace();
        v1.push(values.next().unwrap().parse::<usize>().unwrap());
        v2.push(values.next().unwrap().parse::<usize>().unwrap());
    }
    let result: usize = v1
        .iter()
        .map(|index| index * v2.iter().filter(|x| *x == index).count())
        .sum();
    println!("{:?}", result);
    Ok(stringify!(result).to_owned())
}
