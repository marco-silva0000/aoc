use std::env;
use std::fs;

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    if !current_dir.ends_with("/1") {
        current_dir += "/1"
    }
    let contents = fs::read_to_string(current_dir + "/input.txt").expect("couldn't read file");
    let lines = contents.lines();
    let mut elfs: Vec<Vec<u32>> = vec![vec![]];
    for l in lines.into_iter() {
        if l != "" {
            let value = l.parse::<u32>().unwrap();
            elfs.last_mut().unwrap().push(value);
        } else {
            let s = Vec::new();
            elfs.push(s);
        }
    }
    let len = elfs.len();
    println!("{len}");
    let mut summed_elfs: Vec<u32> = elfs.iter().map(|x| -> u32 { x.iter().sum() }).collect();
    summed_elfs.sort();
    let max = summed_elfs.last().unwrap();
    println!("{max}");
    let shitty_max_3 = summed_elfs.get(summed_elfs.len() - 1).unwrap()
        + summed_elfs.get(summed_elfs.len() - 2).unwrap()
        + summed_elfs.get(summed_elfs.len() - 3).unwrap();
    let max3 = &summed_elfs[summed_elfs.len() - 3..].iter().sum::<u32>();
    println!("{shitty_max_3}");
    println!("{max3}");
}
