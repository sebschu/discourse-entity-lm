import sys
import csv
import argparse
import json
import random





def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument("input_file_main", type=str)
  argparser.add_argument("input_file_fillers", type=str)
  argparser.add_argument("output_file", type=str)

  args = argparser.parse_args()

  positions = set()

  with open(args.input_file_main) as main_f, open(args.input_file_fillers) as filler_f:
      stimuli = json.load(main_f)
      fillers = json.load(filler_f)
      lists = [[],[],[],[],[],[],[],[]]
      for j in range(7):
          for i in range(8):
              z = j % 7 + i*2*7
              z2 = z + 7
              lists[(i+j) % 8].append((stimuli[z]))
              lists[(i+j) % 8].append((stimuli[z2]))
              positions.add(z)
              positions.add(z2)

  print(positions)


  with open(args.output_file, "w") as out_f:
      practice_str = json.dumps([f for f in fillers if "practice" in f["trial_id"]])

      out_f.write(f"var practice_items = {practice_str};\n")


      filler_str = json.dumps([f for f in fillers if "filler" in f["trial_id"]])

      out_f.write(f"var fillers = {filler_str};\n")

      out_f.write(f"var stims = [];\n")

      for i, stim_list in enumerate(lists):
          stim_list_str = json.dumps(stim_list)
          out_f.write(f"stims[{i}] = {stim_list_str};\n")



if __name__ == '__main__':
    main()
