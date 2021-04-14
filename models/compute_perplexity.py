import torch, csv, sys, tqdm, json


with open(sys.argv[1], "r") as config_f:
  config = json.load(config_f)
  
input_fname = config["input"]
output_fname = config["output"]
model_id = config["model"]

from transformers import GPT2LMHeadModel, GPT2TokenizerFast
device = 'cpu'
print("Loading model...")
model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
print("Loaded model...")
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
print("Loading tokenizer...")




examples = []



with open(input_fname, "r") as csv_f:
  reader = csv.DictReader(csv_f)
  for line in reader:
    examples.append(line)



for example in tqdm.tqdm(examples):
    
    full_sentence = example["sentence"].replace(" ||| ", "")
    first_part = example["sentence"].split(" ||| ")[0]
    np = example["sentence"].split(" ||| ")[1]
    
    
  
    encoding = tokenizer(full_sentence, return_tensors='pt')
    encoding_first_part = tokenizer(first_part, return_tensors='pt')
    encoding_np = tokenizer(np, return_tensors='pt')
    
    full_sentence_list = list(encoding.input_ids[0].numpy())
    first_part_list = list(encoding_first_part.input_ids[0].numpy())
    np_list = list(encoding_np.input_ids[0].numpy())
    
    trg_len = len(full_sentence_list) - len(first_part_list)
    np_len = len(np_list)
    
    
    input_ids = encoding.input_ids.to(device)
    target_ids = input_ids.clone()
    target_ids[:,:-trg_len] = -100
    
    # TODO: compute accuracy on It / the NP
    


    with torch.no_grad():
        outputs = model(input_ids, labels=target_ids)
        log_likelihood = outputs.loss * trg_len
        example["ll"] = log_likelihood.numpy()
        target_ids[:,-trg_len:-trg_len+np_len] = -100
        outputs = model(input_ids, labels=target_ids)
        log_likelihood = outputs.loss * np_len
        example["np_ll"] = log_likelihood.numpy()
        
        
        
with open(output_fname, "w") as csv_f:
  writer = csv.DictWriter(csv_f, fieldnames=examples[0].keys())
  writer.writeheader()
  writer.writerows(examples)
  

