import csv, sys, argparse

FEMALE_NAMES = set(["Mary", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Nancy"])
MALE_NAMES = set(["James", "John", "Bob", "Michael", "Bill", "David", "Richard", "Joseph", "Thomas", "Chris"])


def main():
  argparser = argparse.ArgumentParser()
  argparser.add_argument("--input", type=str)
  
  args = argparser.parse_args()
  
  
  
  
  with open(args.input) as in_f:
    reader = csv.DictReader(in_f)
  
    field_names = reader.fieldnames
    new_stims = []
    for row in reader:
      if row["pronoun"] is not "1":
        continue
      
      pronoun = ""
      tokens = row["sentence"].split()
      if tokens[0] in FEMALE_NAMES or tokens[3] in FEMALE_NAMES:
        pronoun = "she"
      else:
        pronoun = "he"
      row["sentence"] = row["sentence"].replace(" it  ", f" {pronoun}  ")
      sentence_parts = row["sentence"].split(" ||| ")
      row["sentence"] = " ||| ".join(sentence_parts[0:2])
      
      new_stims.append(row)
  

  writer = csv.DictWriter(sys.stdout, fieldnames = field_names)
  writer.writerows(new_stims)


if __name__ == '__main__':
  main()
