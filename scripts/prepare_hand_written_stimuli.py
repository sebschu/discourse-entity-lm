import sys
import csv
import argparse
import json


def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument("input_file", type=str)
  argparser.add_argument("output_file", type=str)


  args = argparser.parse_args()

  TYPES = ["affirmative", "negated", "know", "doubt", "modal", "managed", "failed"]

  IT_CONTINUATIONS = {
    "affirmative": "it_continuation_negation",
    "negated": "it_continuation_negation",
    "know": "it_continuation_factive",
    "doubt": "it_continuation_factive",
    "modal": "it_continutation_modal",
    "managed": "it_continuation_implicative",
    "failed": "it_continuation_implicative"
  }

  SUBJ_CONTINUATIONS = {
    "affirmative": "subj_continuation_affirmative",
    "negated": "subj_continuation_negated",
    "know": "subj_continutation_know",
    "doubt": "subj_continutation_doubt",
    "modal": "subj_continuation_modal",
    "managed": "subj_continuation_managed",
    "failed": "subj_continuation_failed"
  }

  examples = []
  with open(args.input_file) as f:
      reader = csv.DictReader(f)
      for row in reader:
          for ex_type in TYPES:
              c_field = f"context_{ex_type}"
              i_field = IT_CONTINUATIONS[ex_type]
              s_field = SUBJ_CONTINUATIONS[ex_type]
              ex_id = f"{row['id']}_{ex_type}"
              ex = {
                "id": ex_id,
                "i_sentence": f"{row[c_field]} {row[i_field]}",
                "s_sentence": f"{row[c_field]} {row[s_field]}",
                "type": ex_type
              }
              examples.append(ex)


  with open(args.output_file, "w") as f:
      for ex in examples:
          f.write(json.dumps(ex))
          f.write("\n")





if __name__ == '__main__':
  main()
