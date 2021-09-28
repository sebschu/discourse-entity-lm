import sys
import csv
import argparse
import json


def clean_word_for_wuggy(w):
    if len(w) < 2:
        return f"{w}n"

    if "n't" in w:
        return w.replace("n't", "")

    w = w.replace("lucy", "anna")
    w = w.replace("self-driving", "driving")
    w = w.replace("susan", "anna")
    w = w.replace("carla", "anna")
    w = w.replace("sam", "john")
    w = w.replace("carolyn", "anna")
    w = w.replace("chris", "john")
    w = w.replace("sam", "john")
    w = w.replace("sarah", "anna")
    w = w.replace("colorful", "wonderful")
    w = w.replace("luke", "john")
    w = w.replace("david", "john")
    w = w.replace("lisa", "anna")
    w = w.replace("archeological", "archaeological")
    w = w.replace("dan", "john")
    w = w.replace("page-turner", "page")

    return w



def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument("input_file", type=str)
  argparser.add_argument("output_file", type=str)

  args = argparser.parse_args()

  with open(args.input_file) as f, open(args.output_file, "w") as out_f:
      for line in f:
          ex = json.loads(line)
          s1 = ex["i_sentence"].replace(".", "").lower().split()
          s2 = ex["s_sentence"].replace(".", "").lower().split()
          for w in s1:
              w = clean_word_for_wuggy(w)
              out_f.write(f"{w}\n")
          for w in s2:
              w = clean_word_for_wuggy(w)
              out_f.write(f"{w}\n")



if __name__ == '__main__':
    main()
