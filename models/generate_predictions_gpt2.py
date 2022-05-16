import torch, csv, sys, tqdm, json
import numpy

with open(sys.argv[1], "r") as config_f:
  config = json.load(config_f)

input_fname = config["input"]
output_fname = config["output"] + ".gen"
model_id = config["model"]

from transformers import GPT2LMHeadModel, GPT2TokenizerFast
device = 'cpu' if len(sys.argv) < 3 else sys.argv[2]
print("Loading model...")
model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
print("Loaded model...")
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
print("Loading tokenizer...")


examples = []


with open(input_fname, "r") as jsonl_f:
    for line in jsonl_f:
        ex = json.loads(line)
        
        if "nonref" in ex["id"]:
          continue
        
        ex1 = {
            "id": ex["id"],
            "sentence": ex["exp_sentence"],
            "type": ex["type"],
            "sample": 1,
            "order": ex["order"]
        }
        ex2 = {
            "id": ex["id"],
            "sentence": ex["unexp_sentence"],
            "type": ex["type"],
            "sample": 2,
            "order": ex["order"]
        }
        examples.append(ex1)
        examples.append(ex2)




for example in tqdm.tqdm(examples):

    prompt, continuation, _ = example["sentence"].split(".")
    
    full_sentence = f"{prompt}. The"
    example["prompt"] = full_sentence
    example["model"] = model_id

    encoding = tokenizer(full_sentence, return_tensors='pt')


    input_ids = encoding.input_ids.to(device)
    attention_mask = encoding.attention_mask.to(device)




    with torch.no_grad():
      #follow generation approach in Radford et al. (2019)
      outputs = model.generate(**encoding, max_length=100, return_dict_in_generate=True, do_sample=True, top_k=40)
      example["tokens"] = "|".join([tokenizer._convert_id_to_token(t).replace("Ġ", "##") for t in outputs.sequences[0]])
      example["continuation"] = tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
      example["generation"] = ".".join(example["continuation"].split(".")[0:2]) + "."
      print(example["generation"])




with open(output_fname, "w") as csv_f:
  writer = csv.DictWriter(csv_f, fieldnames=["id", "type", "sample", "order", "model", "prompt", "generation"], extrasaction="ignore")
  writer.writeheader()
  writer.writerows(examples)
