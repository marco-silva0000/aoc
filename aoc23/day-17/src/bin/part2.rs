use aoc23_17::part2::process;
use miette::Context;

fn main() -> miette::Result<()> {
    let file = include_str!("../../input.txt");
    let result = process(file).context("process part 2")?;
    println!("{}", result);
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_process() -> miette::Result<()> {
        let input = "2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533";
        assert_eq!("94", process(input)?);
        Ok(())
    }
}
