use itertools::Itertools;
use std::env;
use std::fs;

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    if !current_dir.ends_with("/2") {
        current_dir += "/2"
    }
    let contents = fs::read_to_string(current_dir + "/input.txt").expect("couldn't read file");
    let lines = contents.lines();

    // println!("{:?}", lines);
    let result = lines
        .into_iter()
        .map(|l| {
            println!("{:?}", l);
            // l contains: Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
            // add max of each color to numbers
            l.split_once(':')
                .unwrap()
                .1
                .split(';')
                .map(|part| {
                    part.split(',').fold([0, 0, 0], |mut set, c| {
                        match c.trim().split_once(' ') {
                            Some((num, "red")) => set[0] += num.parse::<usize>().unwrap(),
                            Some((num, "blue")) => set[1] += num.parse::<usize>().unwrap(),
                            Some((num, "green")) => set[2] += num.parse::<usize>().unwrap(),
                            _ => {
                                println!("{:?}", c);
                                unreachable!("bad input")
                            }
                        }
                        set
                    })
                })
                .collect_vec()
        })
        .map(|game| {
            println!("{:?}", game);
            game.iter()
                .fold([0, 0, 0], |set, part| {
                    [
                        set[0].max(part[0]),
                        set[1].max(part[1]),
                        set[2].max(part[2]),
                    ]
                })
                .iter()
                .product::<usize>()
        })
        .collect_vec();

    println!("{:?}", result);
    println!("{:?}", result.iter().sum::<usize>());
}
