use std::env;
use std::fs;
use std::result;

#[derive(Debug, Clone, PartialEq)]
enum Kind {
    Dir,
    File,
}
#[derive(Debug, Clone)]
struct FSItem {
    path: String,
    size: i32,
    kind: Kind,
    files: Vec<Box<FSItem>>,
}

impl FSItem {
    fn add_dir(&mut self, path: &str, name: &str) {
        let (_, rest) = path.split_once("/").unwrap();
        println!("{:?}", rest);
        if rest.len() > 0 {
            let (next, _) = rest.split_once("/").unwrap();
            let file = self
                .files
                .iter()
                .filter(|f| f.path == next)
                .map(|fs| fs)
                .last()
                .unwrap();
            println!("{:?}", file);
            let index = self.files.iter().position(|f| f.path == file.path).unwrap();
            let mut cloned_file = file.clone();
            cloned_file.add_dir(rest, name);
            self.files.remove(index);
            self.files.extend([cloned_file]);
        } else {
            self.files.extend([Box::new(FSItem {
                path: name.to_string(),
                kind: Kind::Dir,
                files: vec![],
                size: 0,
            })])
        }
    }
    fn add_file(&mut self, path: &str, name: &str, size: i32) {
        let (_, rest) = path.split_once("/").unwrap();
        if rest.len() > 0 {
            let (next, _) = rest.split_once("/").unwrap();
            let file = self
                .files
                .iter()
                .filter(|f| f.path == next)
                .map(|fs| fs)
                .last()
                .unwrap();
            println!("{:?}", file);
            let index = self.files.iter().position(|f| f.path == file.path).unwrap();
            let mut cloned_file = file.clone();
            cloned_file.add_file(rest, name, size);
            self.files.remove(index);
            self.files.extend([cloned_file]);
        } else {
            self.files.extend([Box::new(FSItem {
                path: name.to_string(),
                kind: Kind::File,
                files: vec![],
                size: size,
            })])
        }
    }
    fn update_size(&mut self) -> i32 {
        let mut result = 0;
        for file in &mut self.files {
            if file.size != 0 {
                result += file.size;
            } else {
                file.update_size();
                result += file.size;
            }
        }
        self.size = result;
        return result;
    }
    fn children(self) -> Vec<FSItem> {
        let clone = self.clone();
        let mut result = vec![self];
        let files = clone.files.clone();
        for file in files {
            result.extend(file.children())
        }
        return result;
    }
}

fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let today = "/7";
    if !current_dir.ends_with(today) {
        current_dir += today
    }
    let contents = fs::read_to_string("7/input.txt").expect("couldn't read file");
    let lines = contents.lines();
    let mut fs = FSItem {
        path: "/".to_string(),
        kind: Kind::Dir,
        files: vec![],
        size: 0,
    };

    let comand_prefix = "$ ";
    let mut current_dir = "/".to_owned();
    for mut l in lines.into_iter() {
        println!("{:?}", l);
        l = l.trim();
        if l.starts_with(comand_prefix) {
            let comand = l.strip_prefix(comand_prefix).unwrap();
            if comand.starts_with("cd") {
                let (_, args) = comand.split_once(" ").unwrap();
                if args == ".." {
                    let current_dir_size = current_dir.matches("/").count();
                    current_dir = current_dir
                        .split_inclusive("/")
                        .into_iter()
                        .enumerate()
                        .filter(|&(i, _)| i != current_dir_size - 1)
                        .map(|(_, e)| e)
                        .collect();
                } else if args == "/" {
                    current_dir = args.to_string();
                } else {
                    current_dir = current_dir + args + "/";
                }
            } else if comand.starts_with("ls") {
            }
        } else {
            if l.starts_with("dir ") {
                let (_, name) = l.split_once("dir ").unwrap();
                fs.add_dir(&current_dir, name);
            } else {
                let (size, name) = l.split_once(" ").unwrap();
                fs.add_file(&current_dir, name, size.parse::<i32>().unwrap());
            }
        }
    }

    println!("{:?}", fs);
    fs.update_size();
    println!("{:?}", fs);
    let max = fs.size;
    let part2fs = fs.clone();
    let part1: i32 = fs
        .children()
        .into_iter()
        .filter(|f| f.size < 100000 && f.kind == Kind::Dir)
        .map(|f| f.size)
        .sum();
    println!("Part1: {:?}", part1);
    // part2
    let unused = 70000000 - max;
    let needed_to_free_up = 30000000 - unused;
    let part2 = part2fs
        .children()
        .into_iter()
        .filter(|f| f.size > needed_to_free_up && f.kind == Kind::Dir)
        .map(|f| f.size)
        .min()
        .unwrap();
    println!("Part2: {:?}", part2);
}
