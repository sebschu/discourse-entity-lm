import argparse, csv

def main():

  argparser = argparse.ArgumentParser()
  argparser.add_argument("input_file", type=str)
  argparser.add_argument("output_file", type=str)


  args = argparser.parse_args()

  examples = []

  with open(args.input_file, "r") as res_f:
      reader = csv.DictReader(res_f)
      for line in reader:
          tokens = [t.replace(" ", "##") for t in line["tokens"].split("|||")]
          log_probs = line["log_probs"].split("|||")
          critical_token_idx = -1
          if "pronoun" not in line: # 2 noun results
            for i, token in enumerate(tokens):
              if token == ".":
                critical_token_idx = i
                break
          else:
            for i, token in enumerate(tokens):
                if (token == "##it" or token == "##It" or token == "##they" or token == "##They") and i > 0 and ("and" in tokens[i-1] or tokens[i-1] == "."):
                    critical_token_idx = i
                    break

          

          if critical_token_idx < 0:
              print("ERROR: critical token idx is 0!!!")
              print(line)
          line["continuation_log_prob"] = sum([float(x) for x in log_probs[critical_token_idx:-1]])
          line["critical_token_idx"] = critical_token_idx
          examples.append(line)


  with open(args.output_file, "w") as out_f:
      writer = csv.DictWriter(out_f, examples[0].keys())
      writer.writeheader()
      writer.writerows(examples)



if __name__ == '__main__':
    main()
