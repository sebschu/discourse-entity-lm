import torch, csv, sys, tqdm

from transformers import GPT2LMHeadModel, GPT2TokenizerFast
device = 'cpu'
#model_id = 'gpt2-large'
model_id = 'gpt2'
print("Loading model...")
model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
print("Loaded model...")
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
print("Loading tokenizer...")

GPT2_PERIOD_TOKEN_ID = 13
GPT2_QUESTION_MARK_TOKEN_ID = 30
GPT2_EXCLAMATION_MARK_TOKEN_ID = 0
GPT2_AND_TOKEN = 290

examples = []

fname = sys.argv[1]
with open(fname, "r") as csv_f:
  reader = csv.DictReader(csv_f)
  for line in reader:
    examples.append(line)



for example in tqdm.tqdm(examples):
    encoding = tokenizer(example["sentence"], return_tensors='pt')
    token_id_list = list(encoding.input_ids[0].numpy())
    if GPT2_QUESTION_MARK_TOKEN_ID in token_id_list:
      trg_len = len(token_id_list) - token_id_list.index(GPT2_QUESTION_MARK_TOKEN_ID) - 1
    elif GPT2_EXCLAMATION_MARK_TOKEN_ID in token_id_list:
      trg_len = len(token_id_list) - token_id_list.index(GPT2_EXCLAMATION_MARK_TOKEN_ID) - 1
    elif GPT2_AND_TOKEN in token_id_list:
      trg_len = len(token_id_list) - token_id_list.index(GPT2_AND_TOKEN) - 1
    else:
      trg_len = len(token_id_list) - token_id_list.index(GPT2_PERIOD_TOKEN_ID) - 1
    input_ids = encoding.input_ids.to(device)
    target_ids = input_ids.clone()
    target_ids[:,:-trg_len] = -100
    
    # TODO: compute accuracy on It / the NP
    


    with torch.no_grad():
        outputs = model(input_ids, labels=target_ids)
        log_likelihood = outputs.loss * trg_len
        example["ll"] = log_likelihood.numpy()
        
fname = sys.argv[2]
with open(fname, "w") as csv_f:
  writer = csv.DictWriter(csv_f, fieldnames=examples[0].keys())
  writer.writeheader()
  writer.writerows(examples)
  

