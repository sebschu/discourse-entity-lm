import csv, sys

f = open(sys.argv[1], "r")

reader = csv.DictReader(f, delimiter="\t")

items = []
for line in reader:
  items.append(line)
  
  
pair_id = 0
new_items = []
for item in items:
  new_item = {}
  new_item["pair_id"] = pair_id
  new_item["sentence"] = item["context_aff"] + " ||| " + item["target_aff"] + " ||| ."
  new_item["type"] = "negation-natural"
  new_item["preferred"] = 1
  new_items.append(new_item)
  
  new_item = {}
  new_item["pair_id"] = pair_id
  new_item["sentence"] = item["context_neg"] + " ||| " + item["target_aff"] + " ||| ."
  new_item["type"] = "negation-natural"
  new_item["preferred"] = 0
  new_items.append(new_item)
  
  pair_id += 1
  
  new_item = {}
  new_item["pair_id"] = pair_id
  new_item["sentence"] = item["context_neg"] + " ||| " + item["target_neg"] + " ||| ."
  new_item["type"] = "negation-natural"
  new_item["preferred"] = 1
  new_items.append(new_item)
  
  new_item = {}
  new_item["pair_id"] = pair_id
  new_item["sentence"] = item["context_aff"] + " ||| " + item["target_neg"] + " ||| ."
  new_item["type"] = "negation-natural"
  new_item["preferred"] = 0
  new_items.append(new_item)
  


writer = csv.DictWriter(sys.stdout, fieldnames=["pair_id", "sentence", "type", "preferred"])
writer.writeheader()
writer.writerows(new_items)