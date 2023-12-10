fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let module_path = module_path!();
    let (_, day) = module_path.split_once('_').unwrap();
    let dir_str = "/day-".to_string() + day;
    if !current_dir.ends_with(&dir_str) {
        current_dir += &dir_str;
    }
    let file = include_str!(current_dir + "/input.txt");
    let result = process(file).context("process part 1")?;
    println!("{}", result);
    Ok(())
}
