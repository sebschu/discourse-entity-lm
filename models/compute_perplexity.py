import torch, csv, sys, tqdm, json
import numpy

with open(sys.argv[1], "r") as config_f:
  config = json.load(config_f)

input_fname = config["input"]
output_fname = config["output"]
model_id = config["model"]

from transformers import GPT2LMHeadModel, GPT2TokenizerFast
device = 'cpu' if len(sys.argv) < 3 else sys.argv[2]
print("Loading model...")
model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
print("Loaded model...")
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
print("Loading tokenizer...")

compute_rank = config["compute_rank"] if "compute_rank" in config else False
compute_ll = config["compute_ll"] if "compute_ll" in config else False


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
                "sentence": ex["i_sentence"],
                "type": ex["type"],
                "pronoun": "it"
            }
            ex2 = {
                "id": ex["id"],
                "sentence": ex["s_sentence"],
                "type": ex["type"],
                "pronoun": "subj"
            }
            examples.append(ex1)
            examples.append(ex2)


sm = torch.nn.LogSoftmax()

for example in tqdm.tqdm(examples):

    full_sentence = example["sentence"].replace(" ||| ", "").strip() + "<|endoftext|>"


    encoding = tokenizer(full_sentence, return_tensors='pt')


    input_ids = encoding.input_ids.to(device)
    attention_mask = encoding.attention_mask.to(device)




    with torch.no_grad():
        if compute_ll:
          outputs = model(input_ids, attention_mask=attention_mask)
          logits = outputs.logits[0]
          scores = logits.gather(1, input_ids[0].unsqueeze(1)).squeeze(1)
          log_probs = scores - logits.logsumexp(1)
          example["tokens"] = "|".join([tokenizer._convert_id_to_token(t).replace("Ġ", "##") for t in input_ids[0]])
          example["log_probs"] = "|".join([str(x) for x in log_probs.cpu().numpy()])


        if compute_rank:
          outputs = model(input_ids)
          logits = sm(outputs.logits[0, np_start_idx-1, :])
          sorted_logits = logits.sort(descending=True)
          k = numpy.where(sorted_logits[1].numpy() == np_token_idx)[0][0]
          example["k"] = k



with open(output_fname, "w") as csv_f:
  writer = csv.DictWriter(csv_f, fieldnames=examples[0].keys())
  writer.writeheader()
  writer.writerows(examples)
