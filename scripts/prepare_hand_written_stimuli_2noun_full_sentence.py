import sys
import csv
import argparse
import json


def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument("input_file", type=str)
  argparser.add_argument("output_file", type=str)


  args = argparser.parse_args()

  TYPES = ["affirmative_negation", "negation_affirmative", "know_doubt", "doubt_know", "affirmative_modal", "modal_affirmative", "managed_failed", "failed_managed"]

  EXPECTED_CONTINUATIONS = []
  
  EXPECTED_CONTINUATIONS.append({
    "affirmative_negation1": ["continuation_ref_1", "continuation_nonref_2"],
    "negation_affirmative1": ["continuation_ref_2", "continuation_nonref_1"],
    "know_doubt1": ["continuation_ref_1", "continuation_nonref_2"],
    "doubt_know1": ["continuation_ref_2", "continuation_nonref_1"],
    "affirmative_modal1": ["continuation_ref_1", "continuation_nonref_2"],
    "modal_affirmative1": ["continuation_ref_2", "continuation_nonref_1"],
    "managed_failed1": ["continuation_ref_1", "continuation_nonref_2"],
    "failed_managed1": ["continuation_ref_2", "continuation_nonref_1"]
  })
  
  EXPECTED_CONTINUATIONS.append({
    "affirmative_negation2": ["continuation_ref_2", "continuation_nonref_1"],
    "negation_affirmative2": ["continuation_ref_1", "continuation_nonref_2"],
    "know_doubt2": ["continuation_ref_2", "continuation_nonref_1"],
    "doubt_know2": ["continuation_ref_1", "continuation_nonref_2"],
    "affirmative_modal2": ["continuation_ref_2", "continuation_nonref_1"],
    "modal_affirmative2": ["continuation_ref_1", "continuation_nonref_2"],
    "managed_failed2": ["continuation_ref_2", "continuation_nonref_1"],
    "failed_managed2": ["continuation_ref_1", "continuation_nonref_2"]
  })
  
  UNEXPECTED_CONTINUATIONS = []

  UNEXPECTED_CONTINUATIONS.append({
    "affirmative_negation1": ["continuation_ref_2", "continuation_nonref_1"],
    "negation_affirmative1": ["continuation_ref_1", "continuation_nonref_2"],
    "know_doubt1": ["continuation_ref_2", "continuation_nonref_1"],
    "doubt_know1": ["continuation_ref_1", "continuation_nonref_2"],
    "affirmative_modal1": ["continuation_ref_2", "continuation_nonref_1"],
    "modal_affirmative1": ["continuation_ref_1", "continuation_nonref_2"],
    "managed_failed1": ["continuation_ref_2", "continuation_nonref_1"],
    "failed_managed1": ["continuation_ref_1", "continuation_nonref_2"]
  })

  UNEXPECTED_CONTINUATIONS.append({
    "affirmative_negation2": ["continuation_ref_1", "continuation_nonref_2"],
    "negation_affirmative2": ["continuation_ref_2", "continuation_nonref_1"],
    "know_doubt2": ["continuation_ref_1", "continuation_nonref_2"],
    "doubt_know2": ["continuation_ref_2", "continuation_nonref_1"],
    "affirmative_modal2":["continuation_ref_1", "continuation_nonref_2"],
    "modal_affirmative2": ["continuation_ref_2", "continuation_nonref_1"],
    "managed_failed2": ["continuation_ref_1", "continuation_nonref_2"],
    "failed_managed2": ["continuation_ref_2", "continuation_nonref_1"]
  })
  

  examples = []
  with open(args.input_file) as f:
      reader = csv.DictReader(f)
      for row in reader:
          for ex_type in TYPES:
            for i in range(2):
              for j in range(2):
                c_field = f"{ex_type}{i+1}"
                ref = "ref" if j == 0 else "nonref"
                expected_field = EXPECTED_CONTINUATIONS[i][c_field][j]
                unexpected_field = UNEXPECTED_CONTINUATIONS[i][c_field][j]
                ex_id = f"{row['id']}_{ex_type}_{ref}"
                ex = {
                  "id": ex_id,
                  "exp_sentence": f"{row[c_field]} {row[expected_field]}",
                  "unexp_sentence": f"{row[c_field]} {row[unexpected_field]}",
                  "prompt": f"{row[c_field]}",
                  "exp_continuation": f"{row[expected_field]}",
                  "unexp_continuation": f"{row[unexpected_field]}",
                  "type": ex_type,
                  "order": i + 1
                }
                
                # change possesive det to definite det for one stimulus to make it more natural
                if row["id"] == "2_car" and "managed" in ex_type and ref == "ref":
                  ex["exp_sentence"] = ex["exp_sentence"].replace("Her ", "The ")
                  ex["unexp_sentence"] = ex["unexp_sentence"].replace("Her ", "The ")
                  ex["exp_continuation"] = ex["exp_continuation"].replace("Her ", "The ")
                  ex["unexp_continuation"] = ex["unexp_continuation"].replace("Her ", "The ")
                examples.append(ex)



  with open(args.output_file, "w") as f:
      for ex in examples:
          f.write(json.dumps(ex))
          f.write("\n")


if __name__ == '__main__':
  main()
