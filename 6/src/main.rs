use std::collections::HashMap;
use std::env;
use std::fs;

fn print_crates(crates: &HashMap<u32, Vec<char>>) {
    for i in 1..crates.keys().len() + 1 {
        print!("{i}: ");
        let row = crates.get(&(i as u32)).unwrap();
        for j in 0..row.len() {
            let item = row.get(j).unwrap();
            print!("{item}");
        }
        print!("\n");
    }
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let today = "/5";
    if !current_dir.ends_with(today) {
        current_dir += today
    }
    let contents = fs::read_to_string("5/input.txt").expect("couldn't read file");
    let lines = contents.lines();
    let mut crates: HashMap<u32, Vec<char>> = HashMap::new();
    let mut crates2: HashMap<u32, Vec<char>> = HashMap::new();
    for l in lines.into_iter() {
        if l.contains("[") {
            for c in (0..l.len()).step_by(4) {
                println!("{:?}", c);
                if !l.chars().nth(c + 1).unwrap().is_whitespace() {
                    let index = (c / 4 + 1) as u32;
                    let item = l.chars().nth(c + 1).unwrap();
                    println!("{:?}", index);
                    println!("{:?}", item);
                    if !crates.contains_key(&index) {
                        crates.insert(index, vec![item]);
                        crates2.insert(index, vec![item]);
                    } else {
                        crates.get_mut(&index).unwrap().extend(vec![item]);
                        crates2.get_mut(&index).unwrap().extend(vec![item]);
                    }
                }
            }
        } else if l.starts_with("move") {
            print_crates(&crates2);
            println!("{:?}", l);
            let (ammount, from_to) = l
                .strip_prefix("move ")
                .unwrap()
                .split_once(" from ")
                .unwrap();
            let (origin, destiny) = from_to.split_once(" to ").unwrap();
            let ammount = ammount.parse::<u32>().unwrap();
            let origin = origin.parse::<u32>().unwrap();
            let destiny = destiny.parse::<u32>().unwrap();

            // Part1
            for _ in 0..ammount {
                let item = crates.get_mut(&origin).unwrap().remove(0);
                crates.get_mut(&destiny).unwrap().insert(0, item);
            }
            // Part2
            let (chunk, remainder) = crates2.get_mut(&origin).unwrap().split_at(ammount as usize);
            let mut chunk_vec: Vec<char> = chunk.to_vec();
            let remainder_vec: Vec<char> = remainder.to_vec();
            // println!("chunk {:?}", chunk_vec);
            let destiny_item = crates2.get_mut(&destiny).unwrap();
            // println!("destiny_item {:?}", destiny_item);
            chunk_vec.extend_from_slice(destiny_item);
            crates2.remove(&destiny);
            crates2.insert(destiny, chunk_vec);
            crates2.remove(&origin);
            crates2.insert(origin, remainder_vec);
        }
    }
    for i in 1..crates.keys().len() + 1 {
        let item = crates.get(&(i as u32)).unwrap().get(0).unwrap();
        print!("{item}");
    }
    print!("\n");
    for i in 1..crates2.keys().len() + 1 {
        let item = crates2.get(&(i as u32)).unwrap().get(0).unwrap();
        print!("{item}");
    }
    print!("\n");
}
