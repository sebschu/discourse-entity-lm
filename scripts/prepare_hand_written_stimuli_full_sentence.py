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

  REF_CONTINUATIONS = {
    "affirmative": "affirmative_continuation_referential",
    "negated": "affirmative_continuation_referential",
    "know": "factive_continuation_referential",
    "doubt": "factive_continuation_referential",
    "modal": "modal_continuation_referential",
    "managed": "implicative_continuation_referential",
    "failed": "implicative_continuation_referential"
  }

  NONREF_CONTINUATIONS = {
    "affirmative": "affirmative_continuation_nonreferential",
    "negated": "affirmative_continuation_nonreferential",
    "know": "factive_continuation_nonreferential",
    "doubt": "factive_continuation_nonreferential",
    "modal": "modal_continuation_nonreferential",
    "managed": "implicative_continuation_nonreferential",
    "failed": "implicative_continuation_nonreferential"
  }

  examples = []
  with open(args.input_file) as f:
      reader = csv.DictReader(f)
      for row in reader:
          for ex_type in TYPES:
              c_field = f"context_{ex_type}"
              i_field = REF_CONTINUATIONS[ex_type]
              s_field = NONREF_CONTINUATIONS[ex_type]
              ex_id = f"{row['id']}_{ex_type}"
              ex = {
                "id": ex_id,
                "i_sentence": f"{row[c_field]} {row[i_field]}",
                "s_sentence": f"{row[c_field]} {row[s_field]}",
                "prompt": f"{row[c_field]}",
                "i_continuation": f"{row[i_field]}",
                "s_continuation": f"{row[s_field]}",
                "type": ex_type
              }
              examples.append(ex)


  with open(args.output_file, "w") as f:
      for ex in examples:
          f.write(json.dumps(ex))
          f.write("\n")





if __name__ == '__main__':
  main()
