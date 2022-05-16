import sys
import csv
import argparse
import json
import random
from collections import Counter


NEG_TYPES = ["failed", "doubt", "negated", "modal"]

pratice_trials = [
  {
    "prompt": "Peter had a coffee with milk",
    "exp_continuation": "and sugar for breakfast.",
    "unexp_continuation": "and socks in the drawer.",
    "id": "practice_1"
  },
  {
    "prompt": "Pam saw a show on Broadway.",
    "exp_continuation": "She enjoyed the songs in the final act the most.",
    "unexp_continuation": "She watered the plants with rainwater.",
    "id": "practice_2"
  }
]

filler_trials = [
  {
    "prompt": "Andrew bought a scooter",
    "exp_continuation": "and a helmet online.",
    "unexp_continuation": "and a horror movie at the the movie theater.",
    "id": "filler_1"
  },
  {
    "prompt": "Jane bet on her favorite basketball team",
    "exp_continuation": "to win the game.",
    "unexp_continuation": "to give birth to four kittens.",
    "id": "filler_2",
  },
  {
    "prompt": "Lisa assigned a lot of homework",
    "exp_continuation": "to the students in her class.",
    "unexp_continuation": "to the blue car in front of the courthouse.",
    "id": "filler_3"
  }
]

def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument("input_file_single_noun", type=str)
  argparser.add_argument("input_file_two_noun", type=str)
  argparser.add_argument("output_file", type=str)

  args = argparser.parse_args()

  examples_single_noun = []
  examples_two_noun = []
  
  lists = []
  
  with open(args.input_file_single_noun) as single_noun_f, open(args.input_file_two_noun) as two_noun_f:
      for line in single_noun_f:
        ex = json.loads(line)
        ex["exp_continuation"] =   ex["i_continuation"] if ex["type"] not in NEG_TYPES else ex["s_continuation"]
        ex["unexp_continuation"] = ex["s_continuation"] if ex["type"] not in NEG_TYPES else ex["i_continuation"]
        del ex["s_continuation"]
        del ex["i_continuation"]
        examples_single_noun.append(ex)
        if ex["type"] == "modal":
          examples_single_noun.append(ex)
      for line in two_noun_f:
        ex = json.loads(line)
        examples_two_noun.append(ex)

  len_single = len(examples_single_noun)
  for i in range(int(len_single / 2)):
    ex_1_idx = i
    ex_2_idx = int((len_single / 2) + ((i + 3) % (len_single / 2)))
    if examples_single_noun[ex_1_idx]["type"] == "modal" and examples_single_noun[ex_2_idx]["type"] in NEG_TYPES:
      lists.append([examples_single_noun[ex_2_idx]])
    elif examples_single_noun[ex_2_idx]["type"] == "modal" and examples_single_noun[ex_1_idx]["type"] in NEG_TYPES:
      lists.append([examples_single_noun[ex_1_idx]])
    else:
      lists.append([examples_single_noun[ex_1_idx], examples_single_noun[ex_2_idx]])
  
  # perform a couple of checks
  for l in lists:
    if len(l) > 1 and l[0]["type"] ==  l[1]["type"]:
      print("PROBLEM: Two identical types of stimuli in one list.")
    elif len(l) > 1 and l[0]["type"] in NEG_TYPES and l[1]["type"] in NEG_TYPES:
      print("PROBLEM: Two negated stimuli in one list.") 
  print(len(lists))  
  
  len_double = len(examples_two_noun)
  indices = set()
  j = 0
  for i in range(int(len_double / 4), int(len_double / 2)):
    if i % 4 == 2 or i % 4 == 3:
      continue
    ex_1_idx = int((len_double / 4) + ((i + 32) % (len_double / 4))) 
    ex_2_idx = int((len_double / 2) + ((i + 105) % (len_double / 4)))
    ex_3_idx = int((len_double / 4) * 3 + ((i + 49) % (len_double / 4)))
    ex_4_idx = int(((i + 88 - (len_double / 4)) % (len_double / 4)))
    
    indices.add(ex_1_idx)
    indices.add(ex_2_idx)
    indices.add(ex_3_idx)
    indices.add(ex_4_idx)
    #print(ex_1_idx, ex_2_idx, ex_3_idx, ex_4_idx)
    lists[j].extend([examples_two_noun[ex_1_idx], examples_two_noun[ex_2_idx], examples_two_noun[ex_3_idx], examples_two_noun[ex_4_idx]])
    j += 1
  
  id_counter = Counter()
  type_counter = Counter()
  
  for l in lists:
    print(", ".join([j["id"] for j in l]))
    ids = [int(j["id"][0:2].replace("_", "")) for j in l]
    types = [j["type"] for j in l]
    for i in ids:
      id_counter[i] += 1
    for t in types:
      type_counter[t] +=1  
    if len(set(ids)) != len(ids):
      print("PROBLEM: ", ids)
    ref_non_ref = [j["id"].split("_")[-1] for j in l[-4:]]
    if Counter(ref_non_ref)["ref"] != 2 or Counter(ref_non_ref)["nonref"] != 2:
      print("PROBLEM:", Counter(ref_non_ref))
    types = [j["id"].split("_")[-2] for j in l[-4:]]
    types = types + [j["id"].split("_")[-3] for j in l[-4:]]
    if len(set(types)) != 7:
      print("PROBLEM:", types)
    
  print(type_counter)
  print(id_counter)
  
  print(len(lists))  
  
  print(len(indices))
  print(len(examples_single_noun))
  print(len(examples_two_noun))


  split_lists = []
  for l in lists:
    l1 = l[0:-2]
    l2 = l[0:-4] + l[-2:]
    split_lists.append(l1)
    split_lists.append(l2)
  
  for l in split_lists:
    print(", ".join([j["id"] for j in l]))
    

  with open(args.output_file, "w") as out_f:
      practice_str = json.dumps(pratice_trials)
  
      out_f.write(f"var practice_items = {practice_str};\n")


      filler_str = json.dumps(filler_trials)

      out_f.write(f"var fillers = {filler_str};\n")

      out_f.write(f"var stims = [];\n")

      for i, stim_list in enumerate(split_lists):
          stim_list_str = json.dumps(stim_list)
          out_f.write(f"stims[{i}] = {stim_list_str};\n")



if __name__ == '__main__':
    main()
