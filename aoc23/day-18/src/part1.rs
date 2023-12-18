use geo::prelude::*;
use geo::EuclideanLength;
use geo::{coord, Area, Coord, LineString, Polygon};
use raqote::*;

enum Direction {
    North,
    South,
    East,
    West,
}

impl Direction {
    fn as_point(&self) -> Coord {
        match self {
            Direction::North => coord! {x: 0.0, y: -1.0},
            Direction::South => coord! {x: 0.0, y: 1.0},
            Direction::East => coord! {x: 1.0, y: 0.0},
            Direction::West => coord! {x: -1.0, y: 0.0},
        }
    }
}

struct Instruction {
    direction: Direction,
    distance: i32,
}

impl Instruction {
    fn walk(&self, start_point: Coord) -> Coord {
        let direction = self.direction.as_point();
        let distance = self.distance as f64;
        start_point + (direction * distance)
    }
}

pub fn process(input: &str) -> miette::Result<String> {
    let mut points = vec![];
    let mut current_point = coord! {x: 0.0, y: 0.0};
    points.push(current_point);
    for line in input.lines() {
        let instruction = parse_instruction(line);
        current_point = instruction.walk(current_point);
        points.push(current_point);
    }
    let line_string = LineString::new(points);
    let min_x = line_string
        .points()
        .min_by(|a, b| a.x().partial_cmp(&b.x()).unwrap())
        .unwrap();
    let min_y = line_string
        .points()
        .min_by(|a, b| a.y().partial_cmp(&b.y()).unwrap())
        .unwrap();
    let max_x = line_string
        .points()
        .max_by(|a, b| a.x().partial_cmp(&b.x()).unwrap())
        .unwrap();
    let max_y = line_string
        .points()
        .max_by(|a, b| a.y().partial_cmp(&b.y()).unwrap())
        .unwrap();

    println!("min_x: {:?}", min_x);
    println!("min_y: {:?}", min_y);
    println!("max_x: {:?}", max_x);
    println!("max_y: {:?}", max_y);

    let mut polygon = Polygon::new(line_string, vec![]);
    polygon = polygon.translate(min_x.x().abs(), min_y.y().abs());

    let perimeter = polygon.exterior().euclidean_length();
    let area = polygon.unsigned_area();
    let result = area + perimeter / 2.0 + 1.0;

    let height = max_y.euclidean_distance(&min_y);
    let width = max_x.euclidean_distance(&min_x);
    println!("height: {:?}", height);
    println!("width: {:?}", width);

    let mut dt = DrawTarget::new(
        (height as i32).try_into().unwrap(),
        (width as i32).try_into().unwrap(),
    );
    let mut pb = PathBuilder::new();
    for point in polygon.exterior().points() {
        pb.line_to(point.x() as f32, point.y() as f32);
    }
    let path = pb.finish();
    let source = Source::Solid(SolidSource {
        r: 0x00,
        g: 0x00,
        b: 0x00,
        a: 0xff,
    });
    dt.fill(&path, &source, &DrawOptions::new());
    let _ = dt.write_png("example.png");

    println!("Perimeter: {}", perimeter);
    println!("Area: {}", area);
    println!("Result: {}", result);
    Ok(format!("{}", result))
}

fn parse_instruction(line: &str) -> Instruction {
    // let mut (_, _, distance_hex) = line.split(' ');
    let mut split = line.splitn(3, ' ');
    let direction_str = split.next().unwrap();
    let distance_hex = split.next().unwrap();
    let _color = split.next().unwrap();
    let direction = match direction_str {
        "U" => Direction::North,
        "D" => Direction::South,
        "R" => Direction::East,
        "L" => Direction::West,
        _ => panic!("Invalid direction"),
    };
    let distance = i32::from_str_radix(distance_hex, 10).unwrap();
    Instruction {
        direction,
        distance,
    }
}
