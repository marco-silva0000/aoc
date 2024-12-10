// cargo run -r -p aoc24_ --bin part1

use std::cmp::Ordering;
use std::collections::HashSet;
use std::collections::HashMap;
use std::hash::{Hash, Hasher};

#[derive(Debug, Clone, Copy, Eq)]
struct Point {
    x: i32,
    y: i32,
}

impl Hash for Point {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.x.hash(state);
        self.y.hash(state);
    }
}

impl PartialEq for Point {
    fn eq(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y
    }
}

impl Ord for Point {
    fn cmp(&self, other: &Self) -> Ordering {
        (self.x, self.y).cmp(&(other.x, other.y))
    }
}

impl PartialOrd for Point {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl std::ops::Add for Point {
    type Output = Point;

    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

impl std::ops::Sub for Point {
    type Output = Point;

    fn sub(self, other: Point) -> Point {
        Point {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

impl std::ops::Neg for Point {
    type Output = Point;

    fn neg(self) -> Point {
        Point {
            x: -self.x,
            y: -self.y,
        }
    }
}

impl Point {
    fn dist(&self, other: &Point) -> i32 {
        (self.x - other.x).abs() + (self.y - other.y).abs()
    }

    fn move_point(&self, direction: Direction) -> Point {
        match direction {
            Direction::North => Point { x: self.x, y: self.y - 1 },
            Direction::South => Point { x: self.x, y: self.y + 1 },
            Direction::East => Point { x: self.x + 1, y: self.y },
            Direction::West => Point { x: self.x - 1, y: self.y },
            Direction::NorthWest => Point { x: self.x - 1, y: self.y - 1 },
            Direction::NorthEast => Point { x: self.x + 1, y: self.y - 1 },
            Direction::SouthEast => Point { x: self.x + 1, y: self.y + 1 },
            Direction::SouthWest => Point { x: self.x - 1, y: self.y + 1 },
        }
    }

    fn get_neighbours(
        &self,
        directions: Option<&[Direction]>,
        max_x: Option<i32>,
        max_y: Option<i32>,
        min_x: Option<i32>,
        min_y: Option<i32>,
    ) -> Vec<(Point, Direction)> {
        let mut neighbours = self.get_all_neighbours();
        if let Some(directions) = directions {
            neighbours.retain(|(_, dir)| directions.contains(dir));
        }
        if let Some(max_x) = max_x {
            neighbours.retain(|(point, _)| point.x < max_x);
        }
        if let Some(max_y) = max_y {
            neighbours.retain(|(point, _)| point.y < max_y);
        }
        if let Some(min_x) = min_x {
            neighbours.retain(|(point, _)| point.x >= min_x);
        }
        if let Some(min_y) = min_y {
            neighbours.retain(|(point, _)| point.y >= min_y);
        }
        neighbours
    }

    fn get_all_neighbours(&self) -> Vec<(Point, Direction)> {
        vec![
            (self.move_point(Direction::North), Direction::North),
            (self.move_point(Direction::South), Direction::South),
            (self.move_point(Direction::East), Direction::East),
            (self.move_point(Direction::West), Direction::West),
        ]
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum Direction {
    North,
    South,
    East,
    West,
    NorthWest,
    NorthEast,
    SouthEast,
    SouthWest,
}
 impl Direction {
    fn opposite(&self) -> Self {
        match self {
            Direction::North => Direction::South,
            Direction::South => Direction::North,
            Direction::East => Direction::West,
            Direction::West => Direction::East,
            Direction::NorthWest => Direction::SouthEast,
            Direction::NorthEast => Direction::SouthWest,
            Direction::SouthEast => Direction::NorthWest,
            Direction::SouthWest => Direction::NorthEast,
        }
    }
    fn new(s: &str) -> Self {
        match s {
            "N" => Direction::North,
            "S" => Direction::South,
            "E" => Direction::East,
            "W" => Direction::West,
            "2" => Direction::NorthWest,
            "1" => Direction::NorthEast,
            "4" => Direction::SouthEast,
            "3" => Direction::SouthWest,
            _ => panic!("Invalid direction"),
        }
    }
}


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum Tile {
    X,
    M,
    A,
    S,
    Other(char),
}

impl Tile {
    fn new(c: char) -> Self {
        match c {
            'X' => Tile::X,
            'M' => Tile::M,
            'A' => Tile::A,
            'S' => Tile::S,
            _ => Tile::Other(c),
        }
    }
}

fn part1(values_list: Vec<&str>) -> String {
    let mut result = Vec::new();
    let mut grid = HashMap::new();

    for (y, line) in values_list.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let tile = Tile::new(c);
            grid.insert(Point { x: x as i32, y: y as i32 }, tile);
        }
    }

    let max_x = values_list[0].len() as i32;
    let max_y = values_list.len() as i32;
    let min_x = 0;
    let min_y = 0;

    print_grid(&grid, max_x + 1, max_y + 1, None);

    for y in 0..max_y {
        for x in 0..max_x {
            let x_point = Point { x, y };
            if let Some(Tile::X) = grid.get(&x_point) {
                let x_neighbours = x_point.get_neighbours(None, Some(max_x), Some(max_y), Some(min_x), Some(min_y));
                for (m_point, direction) in x_neighbours {
                    if let Some(Tile::M) = grid.get(&m_point) {
                        let m_neighbours = m_point.get_neighbours(Some(&[direction]), Some(max_x), Some(max_y), Some(min_x), Some(min_y));
                        for (a_point, _) in m_neighbours {
                            if let Some(Tile::A) = grid.get(&a_point) {
                                let a_neighbours = a_point.get_neighbours(Some(&[direction]), Some(max_x), Some(max_y), Some(min_x), Some(min_y));
                                for (s_point, _) in a_neighbours {
                                    if let Some(Tile::S) = grid.get(&s_point) {
                                        result.push((x_point, m_point, a_point, s_point));
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    let mut all_points = Vec::new();
    for r in &result {
        all_points.extend_from_slice(&[r.0, r.1, r.2, r.3]);
    }

    print_grid(&grid, max_x, max_y, Some(&all_points));
    println!("{}", result.len());
    println!("{}", result.len());
    println!("{}", result.len());
    println!("{}", result.len());

    format!("{}", result.len())
}

fn print_grid(grid: &HashMap<Point, Tile>, max_x: i32, max_y: i32, points: Option<&Vec<Point>>) {
    let points_set: HashSet<Point> = points.map_or(HashSet::new(), |p| p.iter().cloned().collect());

    for y in 0..max_y {
        for x in 0..max_x {
            let point = Point { x, y };
            if let Some(tile) = grid.get(&point) {
                if points_set.contains(&point) {
                    print!("{}", match tile {
                        Tile::X => 'X',
                        Tile::M => 'M',
                        Tile::A => 'A',
                        Tile::S => 'S',
                        Tile::Other(c) => *c,
                    });
                } else {
                    print!(".");
                }
            } else {
                print!("@");
            }
        }
        println!();
    }
}


pub fn process(input: &str) -> miette::Result<String> {
    let values_list: Vec<&str> = input.lines().collect();

    // Call the part1 function with the parsed input
    let result = part1(values_list);

    // Return the result
    Ok(result)
}
