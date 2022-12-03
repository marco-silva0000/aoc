use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Debug)]
#[derive(PartialEq)]
#[derive(Eq)]
#[derive(Hash)]
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
}
fn tool_score(tool: &Tool) -> i32{
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


fn battle(p1: &Tool, p2: &Tool) -> i32 {
    let nemesis_map = HashMap::from([
        (Tool::Rock, Tool::Paper),
        (Tool::Paper, Tool::Scissors),
        (Tool::Scissors, Tool::Rock),
    ]);
    if p1 == p2 {
        return 0;
    } 
    else if *p1 == nemesis_map[&p2] {
        return -1; 
    }
    else{
        return 1;
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
}

fn find_tool(opponent: &Tool, outcome: &Outcome) -> Tool {
  return match outcome  {
      Outcome::Draw => match opponent {
        Tool::Paper => Tool::Paper,
        Tool::Rock => Tool::Rock,
        Tool::Scissors => Tool::Scissors,
      },
      Outcome::Lose => nemesis_map(&nemesis_map(opponent)),
      Outcome::Win => nemesis_map(opponent),
  }

}

fn play(opponent: &Tool, me: &Tool) -> i32 {
    let score = tool_score(me) + (battle(opponent, me) + 1)*3;
    return score;
}

fn play2(opponent: &Tool, outcome: &Outcome) -> i32 {
    let my_tool = find_tool(opponent, outcome);
    let score = tool_score(&my_tool) + (battle(opponent, &my_tool) + 1)*3;
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

        println!("{:?}", tool);
        println!("{:?}", second_tool);
        println!("{:?}", outcome);
    }
    println!("{:?}", first);
    let sum: i32 = first.iter().sum();
    let sum2: i32 = second.iter().sum();
    println!("{sum}");
    println!("{sum2}");
}
