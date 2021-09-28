import sys
import csv
import argparse
import json






def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument("input_file", type=str)
  argparser.add_argument("output_file", type=str)

  args = argparser.parse_args()

  with open(args.input_file) as f, open(args.output_file, "w") as out_f:
      for line in f:
          ex = json.loads(line)
          ex_type = ex["type"]
          ex_id = ex["id"]
          s1 = ex["i_sentence"].lower()
          s2 = ex["s_sentence"].lower()
          out_f.write(f"{ex_type}_i;{ex_id};{s1}\n")
          out_f.write(f"{ex_type}_s;{ex_id};{s2}\n")




if __name__ == '__main__':
    main()
