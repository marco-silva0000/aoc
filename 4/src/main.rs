use std::env;
use std::fs;


fn bitshift(section: &str) -> u128 {
    // println!("{section}");
    let (start, finish) = section.split_once('-').unwrap();
    let start_bin = start.parse::<u128>().unwrap();
    let finish_bin = finish.parse::<u128>().unwrap();
    let size = finish_bin - start_bin;
    let mask: u128 = 2u128.pow(u32::try_from(size + 1).unwrap()) -1;
    let result = mask << start_bin;
    // println!("{:0>128b}", start_bin);
    // println!("{:0>128b}", finish_bin);
    // println!("{:0>128b}", mask);
    // println!("{:0>128b}", result);
    return result;
}


fn main() {
    let mut current_dir = env::current_dir().unwrap().to_str().unwrap().to_owned();
    let today = "/4";
    if !current_dir.ends_with(today) {
        current_dir += today
    }
    let contents = fs::read_to_string("4/input.txt").expect("couldn't read file");
    let mut result = 0;
    let mut result2 = 0;
    let lines = contents.lines();
    for l in lines.into_iter() {
        // println!("{l}");
        let (elf1, elf2) = l.split_once(',').unwrap();
        let elf1_bit = bitshift(elf1);
        let elf2_bit = bitshift(elf2);
        let or_result = elf1_bit | elf2_bit;
        if (elf1_bit == or_result) || (elf2_bit == or_result) {
            result += 1;
        }
        if (elf1_bit & elf2_bit) != 0u128 {
            result2 += 1;
        }
    }
    println!("{result}");
    println!("{result2}");
}
