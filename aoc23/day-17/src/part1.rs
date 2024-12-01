use core::cmp::Eq;
use core::cmp::PartialEq;
use core::hash::Hash;
use core::hash::Hasher;
use glam::IVec2;
use pathfinding::prelude::astar;
use std::collections::HashMap;
use std::ops::Mul;

#[derive(Debug, Clone, Default, Hash, PartialEq, Eq)]
struct State {
    position: IVec2,
    direction: IVec2,
    chain_length: usize,
}

// impl Hash for State {
//     fn hash<H: Hasher>(&self, state: &mut H) {
//         self.position.x.hash(state);
//         self.position.y.hash(state);
//         self.direction.x.hash(state);
//         self.direction.y.hash(state);
//         self.chain_length.hash(state);
//     }
// }
// impl PartialEq for State {
//     fn eq(&self, other: &Self) -> bool {
//         self.position.x == other.position.x
//             && self.position.y == other.position.y
//             && self.direction.x == other.direction.x
//             && self.direction.y == other.direction.y
//             && self.chain_length == other.chain_length
//     }
// }
// impl Eq for State {}

impl State {
    fn successors(
        &self,
        grid: &HashMap<IVec2, usize>,
        max_chain: usize,
        min_chain_before_turn: usize,
    ) -> Vec<(State, usize)> {
        let r = vec![IVec2::X, IVec2::Y, IVec2::NEG_X, IVec2::NEG_Y]
            .iter()
            .inspect(|d| {
                println!("***iterating {:?}", d);
                println!("self.direction {:?}", self.direction);
                println!("self.chain_length {:?}", self.chain_length);
                println!("max_chain {:?}", max_chain);
                println!("new_position {:?}", self.position + **d);
                println!("in grid? {:?}", grid.contains_key(&(self.position + **d)));
                println!("is not back? {:?}", **d != -self.direction);
            })
            .filter(|d| grid.contains_key(&(self.position + **d)))
            .filter(|d| **d != -self.direction)
            // .filter(|d| {
            //     println!(
            //         "after second filter d {:?} self.direction {:?}",
            //         d, self.direction
            //     );
            //     print!("*d{:?} != &self.direction{:?}={:?} || (*d != &self.direction && self.chain_length >= max_chain)", *d, &self.direction, *d != &self.direction);
            //     *d != &self.direction || (*d != &self.direction && self.chain_length >= max_chain)
            // })
            // .filter(|d| *d != &self.direction && self.chain_length < min_chain_before_turn)
            .inspect(|d| {
                println!("before map d {:?}", d);
            })
            .map(|d| {
                let mut new_chain_length = self.chain_length + 1;
                let mut new_position = self.position + *d;
                if d != &self.direction {
                    new_chain_length = 1;
                }
                (
                    State {
                        position: new_position,
                        direction: *d,
                        chain_length: new_chain_length,
                    },
                    *grid.get(&new_position).unwrap(),
                )
            })
            .collect();
        println!("---------------------r {:?}", r);
        return r;
    }
}

pub fn process(_input: &str) -> miette::Result<String> {
    let mut grid = HashMap::new();
    for (i, line) in _input.lines().enumerate() {
        for (j, c) in line.chars().enumerate() {
            grid.insert(
                IVec2::new(i as i32, j as i32),
                c.to_string().parse::<usize>().unwrap(),
            );
        }
    }
    let max_x = grid.keys().map(|v| v.x).max().unwrap();
    let max_y = grid.keys().map(|v| v.y).max().unwrap();
    let end = IVec2::new(max_x, max_y);
    let max_chain = 3;
    let min_chain_before_turn = 0;
    let start = State {
        position: IVec2::new(0, 0),
        direction: IVec2::X,
        chain_length: 0,
    };
    let result = astar(
        &start,
        |n| n.successors(&grid, max_chain, min_chain_before_turn),
        |n| n.position.distance_squared(end).try_into().unwrap(),
        |n| n.position == end,
    )
    .unwrap()
    .1;
    return Ok(result.to_string());
}
