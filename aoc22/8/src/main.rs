use std::collections::HashMap;
use std::convert::TryInto;
use std::env;
use std::fs;

#[derive(Debug, Clone, PartialEq)]
struct Tree {
    x: i16,
    y: i16,
    height: i16,
    is_visible: bool,
    scenic_score: i32,
}
impl Tree {
    pub fn new(x: i16, y: i16, height: i16) -> Self {
        Self {
            x,
            y,
            height,
            is_visible: false,
            scenic_score: 0,
        }
    }
    pub fn check_views(&mut self, line: &Vec<(i16, i16)>, map: &HashMap<(i16, i16), Tree>) -> i32 {
        let mut result = 0;
        for position in line {
            let tree = map.get(position).unwrap();
            if tree.height < self.height {
                result += 1;
            } else {
                result += 1;
                return result;
            }
        }
        return result;
    }
    pub fn calc_scenic_score(
        &mut self,
        map: &HashMap<(i16, i16), Tree>,
        height: usize,
        length: usize,
    ) -> i32 {
        self.scenic_score = 0;
        let north_views: Vec<(i16, i16)> = (0..self.y).rev().map(|y| (self.x, y)).collect();
        let south_views: Vec<(i16, i16)> =
            (self.y + 1..height as i16).map(|y| (self.x, y)).collect();
        let right_views: Vec<(i16, i16)> =
            (self.x + 1..length as i16).map(|x| (x, self.y)).collect();
        let left_views: Vec<(i16, i16)> = (0..self.x).rev().map(|x| (x, self.y)).collect();
        self.scenic_score = self.check_views(&north_views, &map)
            * self.check_views(&south_views, &map)
            * self.check_views(&right_views, &map)
            * self.check_views(&left_views, &map);

        return self.scenic_score;
    }
}
fn tag_visible(map: &mut HashMap<(i16, i16), Tree>, line: &Vec<(i16, i16)>) {
    let mut current_height = -1;
    for tree in line.iter() {
        let candidate = map.get_mut(tree).unwrap();
        if candidate.height > current_height {
            current_height = candidate.height;
            candidate.is_visible = true;
        }
    }
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let today = "/8";
    let contents = fs::read_to_string("8/input.txt").expect("couldn't read file");
    let lines = contents.lines();
    let mut map: HashMap<(i16, i16), Tree> = HashMap::new();
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
                Tree::new(
                    x.try_into().unwrap(),
                    y.try_into().unwrap(),
                    c.to_digit(10).unwrap().try_into().unwrap(),
                ),
            );
        }
    }
    height += 1;
    length += 1;
    fn part1(mut map: &mut HashMap<(i16, i16), Tree>, height: usize, length: usize) {
        println!("{:?}", map);
        let mut top_views: Vec<Vec<(i16, i16)>> = vec![];
        let mut left_views: Vec<Vec<(i16, i16)>> = vec![];
        for i in 0..length {
            top_views.push(vec![]);
            let x: i16 = i.try_into().unwrap();
            for j in 0..height {
                let y: i16 = j.try_into().unwrap();
                top_views[i].push((x, y));
            }
        }
        for j in 0..height {
            left_views.push(vec![]);
            let y: i16 = j.try_into().unwrap();
            for i in 0..length {
                let x: i16 = i.try_into().unwrap();
                left_views[j].push((x, y));
            }
        }
        let mut right_views = left_views.clone();
        let mut down_views = top_views.clone();
        right_views.iter_mut().map(|l| l.reverse()).for_each(drop);
        down_views.iter_mut().map(|l| l.reverse()).for_each(drop);
        top_views
            .iter()
            .map(|line| tag_visible(&mut map, line))
            .for_each(drop);
        left_views
            .iter()
            .map(|line| tag_visible(&mut map, line))
            .for_each(drop);
        down_views
            .iter()
            .map(|line| tag_visible(&mut map, line))
            .for_each(drop);
        right_views
            .iter()
            .map(|line| tag_visible(&mut map, line))
            .for_each(drop);
    }
    part1(&mut map, height, length);
    let map_clone = map.clone();
    let part2 = map
        .values_mut()
        .map(|t| t.calc_scenic_score(&map_clone, height, length))
        .max()
        .unwrap();
    println!("{:?}", map);
    for j in 0..height {
        let y: i16 = j.try_into().unwrap();
        for i in 0..length {
            let x: i16 = i.try_into().unwrap();
            print!("{}", map.get(&(x, y)).unwrap().height.to_string());
        }
        println!("{}", "");
    }
    println!("{}", "");
    for j in 0..height {
        let y: i16 = j.try_into().unwrap();
        for i in 0..length {
            let x: i16 = i.try_into().unwrap();
            print!("{}", map.get(&(x, y)).unwrap().scenic_score.to_string());
        }
        println!("{}", "");
    }
    println!("{}", "");
    println!("{:?}", map.values().filter(|t| t.is_visible).count());
    println!("{:?}", part2);
}
