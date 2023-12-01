use pathfinding::prelude::build_path;
use pathfinding::prelude::dijkstra_partial;
use std::collections::HashMap;
use std::env;
use std::fs;
use std::slice::Iter;

#[derive(Debug, Clone, Hash, PartialEq, Eq, Copy)]
enum RobotType {
    Ore,
    Clay,
    Obsidian,
    Geode,
}

impl RobotType {
    pub fn iterator() -> Iter<'static, RobotType> {
        static DIRECTIONS: [RobotType; 4] = [
            RobotType::Ore,
            RobotType::Clay,
            RobotType::Obsidian,
            RobotType::Geode,
        ];
        DIRECTIONS.iter()
    }
}
#[derive(Debug, Clone, Hash, PartialEq, Eq, Default, Copy)]
struct Blueprint {
    id: i32,
    ore_cost: i32,
    clay_cost: i32,
    obsidian_ore_cost: i32,
    obsidian_clay_cost: i32,
    geode_ore_cost: i32,
    geode_obsidian_cost: i32,
}
impl Blueprint {
    fn update_inventory(
        &self,
        robot: &RobotType,
        ore: i32,

        clay: i32,
        obsidian: i32,
        geode: i32,
    ) -> (i32, i32, i32, i32) {
        match robot {
            RobotType::Ore => (ore - self.ore_cost, clay, obsidian, geode),
            RobotType::Clay => (ore - self.clay_cost, clay, obsidian, geode),
            RobotType::Obsidian => (
                ore - self.obsidian_ore_cost,
                clay - self.obsidian_clay_cost,
                obsidian,
                geode,
            ),
            RobotType::Geode => (
                ore - self.geode_ore_cost,
                clay,
                obsidian - self.geode_obsidian_cost,
                geode,
            ),
        }
    }
    fn can_build(&self, robot: &RobotType, ore: i32, clay: i32, obsidian: i32) -> bool {
        match robot {
            RobotType::Ore => ore >= self.ore_cost,
            RobotType::Clay => ore >= self.clay_cost,
            RobotType::Obsidian => ore >= self.obsidian_ore_cost && clay >= self.obsidian_clay_cost,
            RobotType::Geode => ore >= self.geode_ore_cost && obsidian >= self.geode_obsidian_cost,
        }
    }
}

#[derive(Debug, Clone, Hash, PartialEq, Eq, Default, Copy)]
struct Game {
    ore: i32,
    clay: i32,
    obsidian: i32,
    geode: i32,
    time_left: i32,
    ore_robots: i32,
    clay_robots: i32,
    obsidian_robots: i32,
    geode_robots: i32,
    last_action: Option<RobotType>,
    blueprint: Blueprint,
}

impl Game {
    fn can_build(&self, robot: &RobotType) -> bool {
        self.blueprint
            .can_build(robot, self.ore, self.clay, self.obsidian)
    }
    fn should_build(&self, robot: &RobotType) -> bool {
        match robot {
            RobotType::Ore => self.time_left > 10,
            RobotType::Clay => self.clay_robots < 5,
            RobotType::Obsidian => self.obsidian < 5,
            RobotType::Geode => true,
        }
    }

    fn build(&self, robot: &RobotType) -> Game {
        let (mut ore, mut clay, mut obsidian, mut geode) =
            self.blueprint
                .update_inventory(robot, self.ore, self.clay, self.obsidian, self.geode);

        let mut ore_robots = self.ore_robots;
        let mut clay_robots = self.clay_robots;
        let mut obsidian_robots = self.obsidian_robots;
        let mut geode_robots = self.geode_robots;

        match robot {
            RobotType::Ore => {
                ore_robots += 1;
                ore -= 1;
            }
            RobotType::Clay => {
                clay_robots += 1;
                clay -= 1;
            }
            RobotType::Obsidian => {
                obsidian_robots += 1;
                obsidian -= 1;
            }
            RobotType::Geode => {
                geode_robots += 1;
                geode -= 1;
            }
        };

        Game {
            ore: ore + ore_robots,
            clay: clay + clay_robots,
            obsidian: obsidian + obsidian_robots,
            geode: geode + geode_robots,
            time_left: self.time_left - 1,
            blueprint: self.blueprint.to_owned(),
            ore_robots,
            clay_robots,
            obsidian_robots,
            geode_robots,
            last_action: Some(robot.to_owned()),
        }
    }
    fn cost(&self) -> i32 {
        let geode_points = self.geode + self.geode_robots * self.time_left;
        let inventory_points = self.ore
            + self.blueprint.clay_cost * self.clay
            + self.blueprint.obsidian_ore_cost * self.obsidian
            + self.blueprint.obsidian_clay_cost * self.blueprint.clay_cost * self.obsidian
            + self.blueprint.geode_ore_cost * self.geode
            + self.blueprint.geode_obsidian_cost
                * (self.blueprint.obsidian_clay_cost * self.blueprint.clay_cost
                    + self.blueprint.obsidian_ore_cost)
                * self.geode;
        10000 - geode_points * 4 - inventory_points * 2
    }

    fn successors_cost(&self) -> Vec<(Game, i32)> {
        if self.time_left <= 0 {}
        let mut next_states: Vec<(Game, i32)> = RobotType::iterator()
            .filter(|robot| self.can_build(robot))
            .filter(|robot| self.should_build(robot))
            .map(|robot| {
                let new_state = self.build(robot);
                let cost = new_state.cost();
                (new_state, cost)
            })
            .collect();
        let idle_state = Game {
            ore: self.ore + self.ore_robots,
            clay: self.clay + self.clay_robots,
            obsidian: self.obsidian + self.obsidian_robots,
            geode: self.geode + self.geode_robots,
            ore_robots: self.ore_robots,
            clay_robots: self.clay_robots,
            obsidian_robots: self.obsidian_robots,
            geode_robots: self.geode_robots,
            time_left: self.time_left - 1,
            blueprint: self.blueprint.to_owned(),
            last_action: None,
        };
        next_states.extend([(idle_state, idle_state.cost() - 1000)]);
        next_states
    }
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let today = "/16";
    if !current_dir.ends_with(today) {
        current_dir += today
    }
    let contents = fs::read_to_string("19/test.txt").expect("couldn't read file");
    let lines = contents.lines();
    let mut blueprints: HashMap<i32, Blueprint> = HashMap::new();
    let game_time = 24;
    for mut l in lines {
        l = l.trim();
        let (blueprint_str, robots_str) = l.split_once(": ").unwrap();
        let blueprint_id: i32 = blueprint_str
            .strip_prefix("Blueprint ")
            .unwrap()
            .parse::<i32>()
            .unwrap();
        let mut robots_iter = robots_str.split('.');
        let ore_cost = robots_iter
            .next()
            .unwrap()
            .trim()
            .strip_prefix("Each ore robot costs ")
            .unwrap()
            .strip_suffix(" ore")
            .unwrap()
            .parse::<i32>()
            .unwrap();
        let clay_cost = robots_iter
            .next()
            .unwrap()
            .trim()
            .strip_prefix("Each clay robot costs ")
            .unwrap()
            .strip_suffix(" ore")
            .unwrap()
            .parse::<i32>()
            .unwrap();
        let mut obsidian_iter = robots_iter
            .next()
            .unwrap()
            .trim()
            .strip_prefix("Each obsidian robot costs ")
            .unwrap()
            .strip_suffix(" clay")
            .unwrap()
            .split(" ore and ");
        let obsidian_ore_cost = obsidian_iter.next().unwrap().parse::<i32>().unwrap();
        let obsidian_clay_cost = obsidian_iter.next().unwrap().parse::<i32>().unwrap();
        let mut geode_iter = robots_iter
            .next()
            .unwrap()
            .trim()
            .strip_prefix("Each geode robot costs ")
            .unwrap()
            .strip_suffix(" obsidian")
            .unwrap()
            .split(" ore and ");
        let geode_ore_cost = geode_iter.next().unwrap().parse::<i32>().unwrap();
        let geode_obsidian_cost = geode_iter.next().unwrap().parse::<i32>().unwrap();

        println!("ore_str {:?}", ore_cost);
        println!("clay_str {:?}", clay_cost);
        println!("obsidian_ore_cost {:?}", obsidian_ore_cost);
        println!("obsidian_clay_cost {:?}", obsidian_clay_cost);
        println!("geode_ore_cost {:?}", geode_ore_cost);
        println!("geode_obsidian_cost {:?}", geode_obsidian_cost);

        blueprints.insert(
            blueprint_id,
            Blueprint {
                id: blueprint_id,
                ore_cost,
                clay_cost,
                obsidian_ore_cost,
                obsidian_clay_cost,
                geode_ore_cost,
                geode_obsidian_cost,
            },
        );
    }
    for blueprint in blueprints.values() {
        let start = Game {
            ore_robots: 1,
            time_left: game_time,
            blueprint: blueprint.to_owned(),
            ..Default::default()
        };
        // // Part 1
        let mut max_iters = 1000000;
        let result = dijkstra_partial(
            &start,
            |n| n.successors_cost(),
            |_| {
                max_iters -= 1;
                max_iters.lt(&0)
            },
        );
        let (nodes, _) = result;
        let best = nodes
            .iter()
            .max_by(|a, b| a.0.geode.cmp(&b.0.geode))
            .unwrap();

        println!("path");
        for node in build_path(best.0, &nodes) {
            println!("  {:?}", node);
        }
        println!("best {:?}", best.0);
        println!("best.geodes {:?}", best.0.geode);
        println!("best.geode*id {:?}", best.0.geode * blueprint.id);
    }

    // // Part 2
    // let max_time = 26;
    // let mut max_iters = 1000000;
    // let start = Node {
    //     position: "AA".to_string(),
    //     ..Default::default()
    // };
    // let mut flow_rate_values = flow_rates.values().collect::<Vec<&i32>>();
    // flow_rate_values.sort();
    // let max_valves = (max_iters / 2).min(flow_rate_values.len());
    // let max_flow_rate: i32 = flow_rate_values[0..max_valves]
    //     .to_vec()
    //     .into_iter()
    //     .enumerate()
    //     .map(|(i, value)| (max_time - i as i32 - 1) * value)
    //     .sum();

    // let result = dijkstra_partial(
    //     &start,
    //     |n| n.successors_cost(&graph, &distances, &flow_rates, max_flow_rate, max_time),
    //     |_| {
    //         max_iters -= 1;
    //         return max_iters.lt(&0);
    //     },
    // );
    // let (nodes, _) = result;
    // let first = nodes.iter().nth(0).unwrap().0;
    // let second = nodes.iter().nth(1).unwrap().0;
    // let mut best = (first, second, first.flow_til_here + second.flow_til_here);
    // for outer in nodes.iter().map(|n| n.0) {
    //     for inner in nodes.iter().map(|n| n.0) {
    //         if !outer.open.iter().any(|val| inner.open.contains(val)) {
    //             if inner.flow_til_here + outer.flow_til_here > best.2 {
    //                 best = (inner, outer, inner.flow_til_here + outer.flow_til_here);
    //                 println!("found best {:?}", best);
    //             }
    //         }
    //     }
    // }

    // println!("best {:?}", best);
    // println!("part2 {:?}", best.2);
}
