import csv, sys, tqdm, json, openai, os, copy
import numpy


openai.api_key = os.getenv("OPENAI_API_KEY")


with open(sys.argv[1], "r") as config_f:
  config = json.load(config_f)

input_fname = config["input"]
output_fname = config["output"] + ".gen"

model_id = "GPT-3"

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
        examples.append(ex1)

            
BATCH_SIZE = 16
N_COMPLETIONS = 2

examples_out = []

for idx in tqdm.tqdm(range(int(len(examples)/16))):
#for idx in tqdm.tqdm([0,1]):
    
    sentences = []
    for i in range(BATCH_SIZE):
      j = idx*BATCH_SIZE + i
      prompt, continuation, _ = examples[j]["sentence"].split(".")
    
      full_sentence = f"{prompt}. The"
      examples[j]["prompt"] = full_sentence
      examples[j]["model"] = model_id
      for k in range(N_COMPLETIONS):
        examples_out.append(copy.deepcopy(examples[j]))
      sentences.append(full_sentence)

    response = openai.Completion.create(engine="davinci",
            prompt=sentences,
            max_tokens=100,
            temperature=0.7,
            n=N_COMPLETIONS,
            logprobs=0,
            echo=True,
            stop="."
        )
    for i in range(BATCH_SIZE * N_COMPLETIONS):
      j = idx*BATCH_SIZE * N_COMPLETIONS + i
      sample = i % N_COMPLETIONS + 1
      examples_out[j]["sample"] = sample
      examples_out[j]["tokens"] = "|".join(response["choices"][i]["logprobs"]["tokens"])
      examples_out[j]["log_probs"] = "|".join([str(p) for p in response["choices"][i]["logprobs"]["token_logprobs"][1:]])
      examples_out[j]["generation"] = response["choices"][i]["text"] + "."


with open(output_fname, "w") as csv_f:
  writer = csv.DictWriter(csv_f, fieldnames=["id", "type", "sample", "order", "model", "prompt", "generation", "tokens", "log_probs"], extrasaction="ignore")
  writer.writeheader()
  writer.writerows(examples_out)
