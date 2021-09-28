import sys
import csv
import argparse
import json
import random





def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument("input_file_amaze", type=str)
  argparser.add_argument("input_file_wuggy", type=str)
  argparser.add_argument("output_file", type=str)
  argparser.add_argument("--fillers", action="store_true")

  args = argparser.parse_args()

  stims = []

  names = ["john", "lucy", "carol", "susan", "mary", "carla", "sam", "michael", "carolyn", "chris", "sarah", "thomas", "luke", "dan", "david", "lisa"]

  with open(args.input_file_amaze) as amaze_f, open(args.input_file_wuggy) as wuggy_f:
      reader = csv.reader(amaze_f, delimiter=";")
      for row in reader:
          row_i = row
          if not args.fillers:
              row_s = reader.__next__()
          else:
              row_s = row
          stim_id = row_i[1]
          assert(stim_id == row_s[1])
          s1 = row_i[2][0].upper() + row_i[2][1:]
          s2 = row_s[2][0].upper() + row_s[2][1:]
          s1 = s1.replace(". he", ". He").replace(". she", ". She").replace(". it", ". It")
          s2 = s2.replace(". he", ". He").replace(". she", ". She").replace(". it", ". It")

          a1 = row_i[3]
          a2 = row_s[3]

          for name in names:
              s1 = s1.replace(name, name[0].upper() + name[1:])
              s2 = s2.replace(name, name[0].upper() + name[1:])

          # s1_words = s1.split()
          # a1_words = a1.split()
          # s1_wuggy_words = []
          # for i in range(len(s1_words)):
          #     w_word = wuggy_f.readline().strip().split()[1]
          #     s1_wuggy_words.append(w_word)
          #
          # s2_words = s2.split()
          # a2_words = a2.split()
          # s2_wuggy_words = []
          # for i in range(len(s2_words)):
          #     w_word = wuggy_f.readline().strip().split()[1]
          #     s2_wuggy_words.append(w_word)
          #
          #
          # for i, w in enumerate(s1_words):
          #     if i > 0 and w not in ["He", "She", "It", "he", "she", "it"] and i < len(s2_words):
          #         if random.random() < 0.3:
          #             a1_words[i] = s1_wuggy_words[i]
          #             a2_words[i] = s1_wuggy_words[i]


          stim = {
            "trial_id": stim_id,
            "s1": s1,
            "s2": s2,
            "a1": a1,
            "a2": a2
          }
          stims.append(stim)

  with open(args.output_file, "w") as out_f:
      json.dump(stims, out_f)



if __name__ == '__main__':
    main()
