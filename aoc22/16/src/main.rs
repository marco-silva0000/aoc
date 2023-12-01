use pathfinding::prelude::bfs;
use pathfinding::prelude::dijkstra_partial;
use std::collections::HashMap;
use std::env;
use std::fs;

#[derive(Debug, Clone, Hash, PartialEq, Eq, Default)]
struct Node {
    position: String,
    open: Vec<String>,
    time_til_here: i32,
    flow_til_here: i32,
}
impl Node {
    fn successors(&self, grid: &HashMap<&str, Vec<String>>) -> Vec<Node> {
        return grid
            .get(&self.position as &str)
            .unwrap()
            .into_iter()
            .map(|st| Node {
                position: st.to_string(),
                open: vec![],
                time_til_here: self.time_til_here + 1,
                ..Default::default()
            })
            .collect();
    }
    fn successors_cost(
        &self,
        grid: &HashMap<&str, Vec<String>>,
        distances: &HashMap<(&str, &str), i32>,
        flow_rates: &HashMap<&str, i32>,
        max_flow_rate: i32,
        max_time: i32,
    ) -> Vec<(Node, i32)> {
        let time_til_here = self.time_til_here + 1;
        return grid
            .keys()
            .filter(|key| key.to_string() != self.position)
            .filter(|key| !self.open.contains(&key.to_string()))
            .filter(|key| flow_rates.get(&key.to_string() as &str).unwrap() > &0)
            .filter(|key| {
                time_til_here + distances.get(&(&self.position as &str, &key)).unwrap() < max_time
            })
            .map(|st| {
                let mut new_open = self.open.clone();
                let temp: Vec<String> = vec![st.to_string()];
                new_open.extend(temp);
                let distance = distances
                    .get(&(&self.position as &str, &st))
                    .unwrap()
                    .to_owned();
                let time_left = max_time - time_til_here - distance;
                let flow_rate = flow_rates.get(&st.to_string() as &str).unwrap();
                let added_flow_rate = time_left * flow_rate;
                let flow_til_here = self.flow_til_here + added_flow_rate;
                let cost = max_flow_rate - flow_til_here + distance;
                return (
                    Node {
                        position: st.to_string(),
                        open: new_open,
                        time_til_here: time_til_here + distance,
                        flow_til_here,
                    },
                    cost,
                );
            })
            .collect();
    }
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let today = "/16";
    if !current_dir.ends_with(today) {
        current_dir += today
    }
    let contents = fs::read_to_string("16/input.txt").expect("couldn't read file");
    let lines = contents.lines();
    let mut graph: HashMap<&str, Vec<String>> = HashMap::new();
    let mut flow_rates: HashMap<&str, i32> = HashMap::new();
    let max_time = 30;
    for mut l in lines.into_iter() {
        l = l.trim();
        l = Box::leak(
            l.replace("tunnel leads to valve", "tunnels lead to valves")
                .into_boxed_str(),
        );
        let (mut valve_str, tunnels_str) = l.split_once("; ").unwrap();
        valve_str = valve_str.strip_prefix("Valve ").unwrap();
        let valve_id = valve_str.split(" ").next().unwrap();
        let flow_rate = valve_str
            .split(" ")
            .last()
            .unwrap()
            .strip_prefix("rate=")
            .unwrap()
            .parse::<i32>()
            .unwrap();

        let tunnels: Vec<String> = tunnels_str
            .strip_prefix("tunnels lead to valves ")
            .unwrap()
            .split(", ")
            .map(|s| s.to_string())
            .collect();
        graph.insert(valve_id, tunnels);
        flow_rates.insert(valve_id, flow_rate);
    }
    let mut distances: HashMap<(&str, &str), i32> = HashMap::new();
    for this in graph.keys() {
        for that in graph.keys() {
            let start = Node {
                position: this.to_string(),
                ..Default::default()
            };
            let goal = Node {
                position: that.to_string(),
                ..Default::default()
            };
            let result = bfs(
                &start,
                |n| n.successors(&graph),
                |n| *n.position == goal.position,
            )
            .unwrap();
            distances.insert((this, that), result.len() as i32 - 1);
        }
    }
    // Part 1
    let mut max_iters = 1000000;
    let start = Node {
        position: "AA".to_string(),
        ..Default::default()
    };
    let mut flow_rate_values = flow_rates.values().collect::<Vec<&i32>>();
    flow_rate_values.sort();
    let max_valves = (max_iters / 2).min(flow_rate_values.len());
    let max_flow_rate: i32 = flow_rate_values[0..max_valves]
        .to_vec()
        .into_iter()
        .enumerate()
        .map(|(i, value)| (max_time - i as i32 - 1) * value)
        .sum();

    let result = dijkstra_partial(
        &start,
        |n| n.successors_cost(&graph, &distances, &flow_rates, max_flow_rate, max_time),
        |_| {
            max_iters -= 1;
            return max_iters.lt(&0);
        },
    );
    let (nodes, _) = result;
    let best = nodes
        .iter()
        .max_by(|a, b| a.0.flow_til_here.cmp(&b.0.flow_til_here))
        .unwrap();
    println!("part1 {:?}", best.0.flow_til_here);

    // Part 2
    let max_time = 26;
    let mut max_iters = 1000000;
    let start = Node {
        position: "AA".to_string(),
        ..Default::default()
    };
    let mut flow_rate_values = flow_rates.values().collect::<Vec<&i32>>();
    flow_rate_values.sort();
    let max_valves = (max_iters / 2).min(flow_rate_values.len());
    let max_flow_rate: i32 = flow_rate_values[0..max_valves]
        .to_vec()
        .into_iter()
        .enumerate()
        .map(|(i, value)| (max_time - i as i32 - 1) * value)
        .sum();

    let result = dijkstra_partial(
        &start,
        |n| n.successors_cost(&graph, &distances, &flow_rates, max_flow_rate, max_time),
        |_| {
            max_iters -= 1;
            return max_iters.lt(&0);
        },
    );
    let (nodes, _) = result;
    let first = nodes.iter().nth(0).unwrap().0;
    let second = nodes.iter().nth(1).unwrap().0;
    let mut best = (first, second, first.flow_til_here + second.flow_til_here);
    for outer in nodes.iter().map(|n| n.0) {
        for inner in nodes.iter().map(|n| n.0) {
            if !outer.open.iter().any(|val| inner.open.contains(val)) {
                if inner.flow_til_here + outer.flow_til_here > best.2 {
                    best = (inner, outer, inner.flow_til_here + outer.flow_til_here);
                    println!("found best {:?}", best);
                }
            }
        }
    }

    println!("best {:?}", best);
    println!("part2 {:?}", best.2);
}
