use std::env;
use std::fs;

#[derive(PartialEq)]
enum Tool {
    Rock,
    Paper,
    Scissors,
}
impl Tool {
    fn from_str(char: &str) -> Self{
        return match char {
                "A"|"X" => Tool::Rock,
                "B"|"Y" => Tool::Paper,
                _ => Tool::Scissors,
        };
    }

    fn score(tool: &Tool) -> i32{
        return match tool {
            Tool::Rock => 1,
            Tool::Paper => 2,
            Tool::Scissors => 3,
        };
    }
    fn nemesis_map(tool: &Tool) -> Tool {
        return match tool {
            Tool::Rock => Tool::Paper,
            Tool::Paper => Tool::Scissors,
            Tool::Scissors => Tool::Rock,
        }
    }
    fn battle(&self, p2: &Tool) -> i32 {
        if self == p2 {
            return 0;
        } 
        else if self == &Tool::nemesis_map(p2) {
            return -1; 
        }
        else{
            return 1;
        }
    }
}


#[derive(Debug)]
enum Outcome {
    Win,
    Draw,
    Lose,
}
impl Outcome {
    fn from_str(char: &str) -> Self{
        return match char {
                "X" => Outcome::Lose,
                "Y" => Outcome::Draw,
                _ => Outcome::Win,
        }
    }
    fn find_tool(&self, opponent: &Tool) -> Tool {
        return match self  {
            Outcome::Draw => match opponent {
                Tool::Paper => Tool::Paper,
                Tool::Rock => Tool::Rock,
                Tool::Scissors => Tool::Scissors,
            },
            Outcome::Lose => Tool::nemesis_map(&Tool::nemesis_map(opponent)),
            Outcome::Win => Tool::nemesis_map(opponent),
        }
    }
}


fn play(opponent: &Tool, me: &Tool) -> i32 {
    let score = Tool::score(me) + (opponent.battle(me) + 1)*3;
    return score;
}

fn play2(opponent: &Tool, outcome: &Outcome) -> i32 {
    let my_tool = outcome.find_tool(opponent);
    let score = Tool::score(&my_tool) + (opponent.battle(&my_tool) + 1)*3;
    return score;
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let today = "/2";
    if !current_dir.ends_with(today) {
        current_dir += today
    }
    let contents = fs::read_to_string("input.txt").expect("couldn't read file");
    let lines = contents.lines();
    let mut first: Vec<i32> = vec![];
    let mut second: Vec<i32> = vec![];

    for l in lines.into_iter() {
        let tool = Tool::from_str(l.chars().nth(0).unwrap().to_string().as_str());
        let second_tool = Tool::from_str(l.chars().nth(2).unwrap().to_string().as_str());
        let outcome = Outcome::from_str(l.chars().nth(2).unwrap().to_string().as_str());
        first.extend([play(&tool, &second_tool)]);
        second.extend([play2(&tool, &outcome)]);
    }
    let sum: i32 = first.iter().sum();
    let sum2: i32 = second.iter().sum();
    println!("{sum}");
    println!("{sum2}");
}
