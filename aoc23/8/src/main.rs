#![feature(try_trait_v2)]
use itertools::Itertools;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;
use std::ops::ControlFlow;
use std::ops::FromResidual;
use std::ops::Try;

fn gcd_of_two_numbers(a: usize, b: usize) -> usize {
    if b == 0 {
        return a;
    }
    gcd_of_two_numbers(b, a % b)
}

pub fn lcm(nums: &[usize]) -> usize {
    if nums.len() == 1 {
        return nums[0];
    }
    let a = nums[0];
    let b = lcm(&nums[1..]);
    a * b / gcd_of_two_numbers(a, b)
}

#[derive(Debug, Clone)] //, Clone, Copy)
struct Node {
    name: String,
    l: String,
    r: String,
    finished_in: usize,
}

impl Node {
    fn new(name: String, l: String, r: String) -> Self {
        Self {
            name,
            l,
            r,
            finished_in: 0,
        }
    }
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    if !current_dir.ends_with("/8") {
        current_dir += "/8"
    }
    let contents = fs::read_to_string(current_dir + "/input.txt").expect("couldn't read file");
    let mut lines = contents.lines();
    let instructions = lines.next().unwrap().to_string();
    lines.next();
    // println!("{:?}", lines);
    let mut node_map: HashMap<String, Node> = HashMap::new();

    lines
        .into_iter()
        .map(|line| {
            let (name, neighbours) = line.split_once(" = ").unwrap();
            let (l, r) = neighbours
                .strip_prefix('(')
                .unwrap()
                .strip_suffix(')')
                .unwrap()
                .split_once(", ")
                .unwrap();
            Node::new(name.to_owned(), l.to_owned(), r.to_owned())
        })
        .for_each(|node| {
            node_map.insert(node.name.to_owned(), node);
        });

    let start = node_map.get("AAA").unwrap();
    let mut current = start;
    println!("{:?}", instructions);
    for (i, instruction) in instructions.clone().chars().cycle().enumerate() {
        // println!("{:?}", current);
        if current.name == "ZZZ" {
            println!("part1 {:?}", i);
            break;
        }
        match instruction {
            'R' => {
                current = node_map.get(&current.r).unwrap();
            }
            'L' => {
                current = node_map.get(&current.l).unwrap();
            }
            _ => unreachable!(),
        }
    }
    // part2
    let starting_node_names = node_map
        .keys()
        .filter(|k| k.ends_with('A'))
        .map(|k| (k, 0))
        .collect_vec();
    println!("starting_node_names{:?}", starting_node_names);

    let mut current_nodes: HashMap<&String, (Node, usize)> = HashMap::new();
    starting_node_names.iter().for_each(|(name, finished_in)| {
        current_nodes.insert(name, (node_map.get(*name).unwrap().clone(), *finished_in));
    });
    let mut part2_vec = vec![];

    for (i, instruction) in instructions.clone().chars().cycle().enumerate() {
        // println!("current_nodes: {:?}", current_nodes);
        if current_nodes.is_empty() {
            break;
        }
        let mut new_nodes: HashMap<&String, (Node, usize)> = HashMap::new();
        for (name, (node, finished_in)) in current_nodes.iter() {
            if *finished_in > 0 {
                part2_vec.push(*finished_in + 1);
                continue;
            }
            let node = match instruction {
                'R' => node_map.get(&node.r).unwrap().clone(),
                'L' => node_map.get(&node.l).unwrap().clone(),
                _ => unreachable!(),
            };
            let finished_in = if node.name.ends_with('Z') {
                i
            } else {
                *finished_in
            };
            new_nodes.insert(name, (node.clone(), finished_in));
        }
        current_nodes = new_nodes;
    }
    println!("part2_vec: {:?}", part2_vec);
    println!("part2as_slice: {:?}", lcm(part2_vec.as_slice()));
}
