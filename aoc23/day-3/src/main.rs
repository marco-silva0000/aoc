use itertools::Itertools;
use std::collections::HashMap;
use std::collections::HashSet;
use std::env;
use std::fs;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct Point {
    x: usize,
    y: usize,
    content: char,
    is_int: bool,
    is_symbol: bool,
    is_part: Option<bool>,
    is_gear: bool,
}
impl Point {
    pub fn new(x: usize, y: usize, content: char) -> Self {
        let is_int = content.is_digit(10);
        let is_symbol = !is_int && content != '.';
        let is_gear = !is_int && content != '*';
        Self {
            x,
            y,
            content,
            is_int,
            is_symbol,
            is_part: None,
            is_gear,
        }
    }
    pub fn get_neighbors(&self, mut map: &HashMap<(usize, usize), Point>) -> Vec<Point> {
        let mut neighbors: Vec<Point> = Vec::new();
        let x = self.x;
        let y = self.y;

        for (x, y) in vec![
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
            (x + 1, y + 1),
            (x - 1, y + 1),
            (x + 1, y - 1),
            (x - 1, y - 1),
        ] {
            if let Some(point) = map.get(&(x, y)) {
                neighbors.push(point.clone());
            }
        }
        neighbors
    }
    pub fn get_x_neighbors(&self, mut map: &HashMap<(usize, usize), Point>) -> Vec<Point> {
        let mut neighbors: Vec<Point> = Vec::new();
        let x = self.x;
        let y = self.y;

        for (x, y) in vec![(x + 1, y), (x - 1, y)] {
            if let Some(point) = map.get(&(x, y)) {
                neighbors.push(point.clone());
            }
        }
        neighbors
    }
}
fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    if !current_dir.ends_with("/3") {
        current_dir += "/3"
    }
    let contents = fs::read_to_string(current_dir + "/test.txt").expect("couldn't read file");
    let lines = contents.lines();

    let mut map: HashMap<(usize, usize), Point> = HashMap::new();
    let mut height = 0;
    let mut length = 0;
    for (y, mut l) in lines.into_iter().enumerate() {
        l = l.trim();
        height = y;
        println!("{:?}", l);
        for (x, c) in l.chars().enumerate() {
            length = x;
            map.insert(
                (x.try_into().unwrap(), y.try_into().unwrap()),
                Point::new(x.try_into().unwrap(), y.try_into().unwrap(), c),
            );
        }
    }
    height += 1;
    length += 1;
    //iterate map based on height and length and set is_part
    let mut count = 0;
    for y in 0..height {
        for x in 0..length {
            let cloned_map = map.clone();
            let point = map.get_mut(&(x, y)).unwrap();
            point.is_part = Some(
                point.is_int
                    && point
                        .get_neighbors(&cloned_map)
                        .iter_mut()
                        .any(|x| x.is_symbol),
            );
            if point.is_part.unwrap() {
                count += 1;
            }
        }
    }
    // set is_part on x neighbors
    fn set_x_neighbours_part(map: &mut HashMap<(usize, usize), Point>, x: usize, y: usize) {
        let mut cloned_map = map.clone();
        let point = map.get_mut(&(x, y)).unwrap();
        if point.is_int {
            point.is_part = Some(true);
            for neighbor in point.get_x_neighbors(&cloned_map) {
                if neighbor.is_int && !neighbor.is_part.unwrap() {
                    set_x_neighbours_part(map, neighbor.x, neighbor.y);
                }
            }
        }
    }
    for y in 0..height {
        for x in 0..length {
            let cloned_map = map.clone();
            let point = map.get_mut(&(x, y)).unwrap();
            if point.is_part.unwrap() {
                set_x_neighbours_part(&mut map, x, y);
            }
        }
    }

    let mut parts: HashMap<(usize, usize, usize), Vec<&Point>> = HashMap::new();
    let mut parts_to_int: HashMap<(usize, usize, usize), usize> = HashMap::new();
    let mut part_start: Option<usize> = None;
    let mut part_points: Vec<&Point> = vec![];
    for y in 0..height {
        if part_start.is_some() {
            let mut clone_parts = part_points.clone();
            clone_parts.push(&map.get(&(length - 1, y - 1)).unwrap());
            parts.insert((part_start.unwrap(), length - 1, y - 1), clone_parts);
            part_start = None;
        }
        part_start = None;
        for x in 0..length {
            let point = map.get(&(x, y)).unwrap();
            if point.is_part.unwrap() {
                if part_start.is_none() {
                    part_start = Some(x);
                    part_points.push(&point);
                } else {
                    part_points.push(&point);
                }
            } else {
                if part_start.is_some() {
                    let clone_parts = part_points.clone();
                    parts.insert((part_start.unwrap(), x - 1, y), clone_parts);
                    part_start = None;
                }
            }
        }
    }
    if part_start.is_some() {
        let mut clone_parts = part_points.clone();
        clone_parts.push(&map.get(&(length - 1, height - 1)).unwrap());
        parts.insert((part_start.unwrap(), length - 1, height - 1), clone_parts);
        part_start = None;
    }

    let part1 = parts
        .keys()
        .map(|k| {
            let (x0, xx, y) = k;
            let mut int_vec: Vec<String> = vec![];
            for x in *x0..=*xx {
                let point = map.get(&(x, *y)).unwrap();
                int_vec.push(point.content.to_string());
            }
            let result = int_vec.into_iter().join("").parse::<usize>().unwrap();
            println!("{:?}", result);
            parts_to_int.insert(*k, result);
            return result;
        })
        .sum::<usize>();

    println!("{:?}", parts.len());
    println!("{:?}", part1);

    let mut point_to_parts_map: HashMap<&Point, (usize, usize, usize)> = HashMap::new();
    for (k, v) in parts.iter() {
        for point in v {
            point_to_parts_map.insert(point, *k);
        }
    }

    let gear_pairs = map
        .values()
        .filter(|p| p.is_gear)
        .map(|p| {
            let mut gear_set = HashSet::new();
            let neighbors = p.get_neighbors(&map);
            for neighbor in neighbors.iter() {
                // if neighbour in point_to_parts_map
                if let Some((x0, xx, y)) = point_to_parts_map.get(&neighbor) {
                    gear_set.insert((*x0, *xx, *y));
                }
            }
            gear_set
        })
        .filter(|s| s.len() == 2)
        .map(|s| {
            s.into_iter().map(|p| {
                let (x0, xx, y) = p;
                parts_to_int.get(&(x0, xx, y)).unwrap()
            })
        })
        .collect::<Vec<_>>();
    println!("{:?}", gear_pairs);
}
