import torch, csv, sys, tqdm, json
import numpy
from lm_scorer.models.auto import AutoLMScorer as LMScorer


with open(sys.argv[1], "r") as config_f:
  config = json.load(config_f)

input_fname = config["input"]
output_fname = config["output"]
model_id = config["model"]

batch_size = 1
device = "cuda:0" if torch.cuda.is_available() else "cpu"
scorer = LMScorer.from_pretrained(model_id, device=device, batch_size=batch_size)





examples = []


if ".csv" in input_fname:
    with open(input_fname, "r") as csv_f:
      reader = csv.DictReader(csv_f)
      for line in reader:
        examples.append(line)
else:
    with open(input_fname, "r") as jsonl_f:
        for line in jsonl_f:
            ex = json.loads(line)
            ex1 = {
                "id": ex["id"],
                "sentence": ex["exp_sentence"],
                "type": ex["type"],
                "expected": 1,
                "order": ex["order"]
            }
            ex2 = {
                "id": ex["id"],
                "sentence": ex["unexp_sentence"],
                "type": ex["type"],
                "expected": 0,
                "order": ex["order"]
            }
            examples.append(ex1)
            examples.append(ex2)



for example in tqdm.tqdm(examples):
    scores, ids, tokens = scorer.tokens_score(example["sentence"], log=True)
    example["tokens"] = "|||".join([t.replace("Ġ", "##") for t in tokens])
    example["log_probs"] = "|||".join([str(x) for x in scores])




with open(output_fname, "w") as csv_f:
  writer = csv.DictWriter(csv_f, fieldnames=examples[0].keys())
  writer.writeheader()
  writer.writerows(examples)
