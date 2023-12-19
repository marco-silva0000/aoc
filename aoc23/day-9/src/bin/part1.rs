use aoc23_9::part1::process;
use miette::Context;

fn main() -> miette::Result<()> {
    println!("Hello, world!");
    let file = include_str!("../../input.txt");
    println!("{:?}", file);
    let result = process(file).context("process part 1")?;
    println!("{}", result);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_process() -> miette::Result<()> {
        let input = "0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45";
        assert_eq!("114", process(input)?);
        Ok(())
    }
}
