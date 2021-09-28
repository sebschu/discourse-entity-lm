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
          tokens = [t.replace(" ", "##") for t in line["tokens"].split("|")]
          log_probs = line["log_probs"].split("|")
          critical_token_idx = -1
          if line["pronoun"] == "it":
              for i, token in enumerate(tokens):
                  if (token == "##it" or token == "##It") and i > 0 and ("and" in tokens[i-1] or tokens[i-1] == "."):
                      critical_token_idx = i
                      break

          else:
              for i, token in enumerate(tokens):
                  if (token == "##she" or token == "##She" or token == "##he" or token == "##He") and i > 0 and ("and" in tokens[i-1] or tokens[i-1] == "."):
                      critical_token_idx = i
                      break

          if critical_token_idx < 0:
              print("ERROR: critical token idx is 0!!!")
              print(line)
          line["pronoun_log_prob"] = log_probs[critical_token_idx]
          line["critical_token_idx"] = critical_token_idx
          examples.append(line)


  with open(args.output_file, "w") as out_f:
      writer = csv.DictWriter(out_f, examples[0].keys())
      writer.writeheader()
      writer.writerows(examples)



if __name__ == '__main__':
    main()
