use aoc23_{{day}}::part1::process;
use miette::Context;

fn main() -> miette::Result<()> {
    let file = include_str!("../../input.txt");
    let result = process(file).context("process part 1")?;
    println!("{}", result);
    Ok(())
}
