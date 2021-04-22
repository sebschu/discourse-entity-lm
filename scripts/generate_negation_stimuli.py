import random
import csv
import sys
import argparse


ANIMALS = [
  ["a dog", "dog"],
  ["an aardvark", "aardvark"],
  ["a hippotamus", "hippotamus"],
  ["a kangaroo", "kangaroo"],
  ["a bird", "bird"],
  ["a rat", "rat"],
  ["a cat", "cat"],
  ["a flamingo", "flamingo"],
  ["a giraffe", "giraffe"],
  ["a lion", "lion"]
]


ANIMAL_VERBS = [
  ["owned", "didn't own", "own"],
  ["saw", "didn't see", "see"],
  ["kicked", "didn't kick", "kick"],
  ["brought", "didn't bring", "bring"],
  ["got", "didn't get", "get"],
  ["bought", "didn't buy", "buy"],
  ["mentioned", "didn't mention", "mention"],
  ["visited", "didn't visit", "visit"],
  ["met", "didn't meet", "meet"],
  ["adopted", "didn't adopt", "adopt"]
]

ANIMAL_CONTINUATIONS = [
  "had a long tail",
  "had a red collar",
  "had a blind eye",
  "had a shrill voice",
  "had a colorful back",
  "enjoyed frolicking in the forest",
  "preferred fish over other food",
  "was called Fido",
  "liked to swim in lakes",
  "loved cheese"
]


DRINKS = [
  ["a manhattan", "manhattan"],
  ["a negroni", "negroni"],
  ["a pisco sour", "pisco sour"],
  ["a coke", "coke"],
  ["a soda", "soda"],
  ["a martini", "martini"],
  ["an old fashioned", "old fashioned"],
  ["a gimlet", "gimlet"],
  ["a mojito", "mojito"],
  ["a caipirinha", "caipirinha"]
]

DRINK_VERBS = [
  ["drunk", "didn't drink", "drink"],
  ["brought", "didn't bring", "bring"],
  ["got", "didn't get", "get"],
  ["bought", "didn't buy", "buy"],
  ["made", "didn't make", "make"],
  ["had", "didn't have", "have"],
  ["slurped", "didn't slurp", "slurp"],
  ["downed", "didn't down", "down"],
  ["poured", "didn't pour", "pour"],
  ["ordered", "didn't order", "order"]
]

DRINK_CONTINUATIONS = [
 "was bitter",
 "was warm",
 "was cold",
 "was sweet",
 "was sour",
 "tasted strange",
 "had to be served in a tall glass",
 "cost a lot of money",
 "came in a green bottle",
 "glowed in the dark" 
]


VEHICLES = [
  ["a car", "car"],
  ["a van", "van"],
  ["a bus", "bus"],
  ["a truck", "truck"],
  ["a bike", "bike"],
  ["a motorcycle", "motorcycle"],
  ["a convertible", "convertible"],
  ["an oldtimer", "oldtimer"],
  ["a limousine", "limousine"],
  ["a scooter", "scooter"]
]


VEHICLE_VERBS = [
  ["bought", "didn't buy", "buy"],
  ["rented", "didn't rent", "rent"],
  ["fixed", "didn't fix", "fix"],
  ["leased", "didn't lease", "lease"],
  ["acquired", "didn't acquire", "aquire"],
  ["destroyed", "didn't destroy", "destroy"],
  ["stole", "didn't steal", "steal"],
  ["donated", "didn't donate", "donate"],
  ["repaired", "didn't repair", "repair"],
  ["ruined", "didn't ruin", "ruin"]
]


VEHICLE_CONTINUATIONS = [
  "was blue",
  "was fast",
  "was slow",
  "was eco-friendly",
  "was expensive",
  "had a flat tire",
  "could seat multiple people",
  "required a special cable",
  "emitted lots of greenhouse gases",
  "made squeaky noises"
]

CLOTHES = [
  ["a sweater", "sweater"],
  ["a shirt", "shirt"],
  ["a bracelet", "bracelet"],
  ["a ring", "ring"],
  ["a hat", "hat"],
  ["a suit", "suit"],
  ["a jacket", "jacket"],
  ["a jumpsuit", "jumpsuit"],
  ["a bandana", "bandana"],
  ["a swimsuit", "swimsuit"]
]

CLOTHES_VERBS = [
  ["wore", "didn't wear", "wear"],
  ["bought", "didn't buy", "buy"],
  ["made", "didn't make", "make"],
  ["donated", "didn't donate", "donate"],
  ["found", "didn't find", "find"],
  ["ordered", "didn't order", "order"],
  ["tried", "didn't try", "try"],
  ["altered", "didn't alter", "alter"],
  ["lost", "didn't lose", "lose"],
  ["borrowed", "didn't borrow", "borrow"]
]

CLOTHES_CONTINUATIONS = [
  "was cheap",
  "was from Europe",
  "was handmade",
  "was appropriate for every occasion",
  "was comfortable",
  "could fit in the drawer",
  "attracted many compliments",
  "required a complicated cleaning procedure",
  "suited everyone",
  "left stains"
]

FURNITURE = [
  ["a chair", "chair"],
  ["a desk", "desk"],
  ["a bench", "bench"],
  ["a bed", "bed"],
  ["a shelf", "shelf"],
  ["a table", "table"],
  ["a dresser", "dresser"],
  ["a bookcase", "bookcase"],
  ["a nightstand", "nightstand"],
  ["a cabinet", "cabinet"]
]

FURNITURE_VERBS = [
  ["assembled", "didn't assemble", "assemble"],
  ["bought", "didn't buy", "buy"],
  ["built", "didn't build", "build"],
  ["refurbished", "didn't refurbish", "refurbish"],
  ["sold", "didn't sell", "sell"],
  ["painted", "didn't paint", "paint"],
  ["sanded", "didn't sand", "sand"],
  ["stained", "didn't stain", "stain"],
  ["scratched", "didn't scratch", "scratch"],
  ["burned", "didn't burn", "burn"]
]

FURNITURE_CONTINUATIONS = [
  "was valuable",
  "was an antique",
  "was made to order",
  "was stable",
  "was attached to the floor",
  "fit into the room",
  "stood out",
  "made the apartment homely",
  "required special care",
  "came from Asia"
]



ALL_STIMS = {
  "ANIMALS": {
    "nouns": ANIMALS,
    "verbs": ANIMAL_VERBS,
    "continuations": ANIMAL_CONTINUATIONS
  },
  "DRINKS": {
    "nouns": DRINKS,
    "verbs": DRINK_VERBS,
    "continuations": DRINK_CONTINUATIONS
  },
  "VEHICLES": {
    "nouns": VEHICLES,
    "verbs": VEHICLE_VERBS,
    "continuations": VEHICLE_CONTINUATIONS
  },
  "CLOTHES" : {
    "nouns": CLOTHES,
    "verbs": CLOTHES_VERBS,
    "continuations": CLOTHES_CONTINUATIONS
  }, 
  "FURNITURE" : {
    "nouns": FURNITURE,
    "verbs": FURNITURE_VERBS,
    "continuations": FURNITURE_CONTINUATIONS
  }
}


PERSON_NAMES = ["James", "John", "Bob", "Michael", "Bill", "David", "Richard", "Joseph", "Thomas", "Chris", "Mary", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Nancy"]


def main():
  
  argparser = argparse.ArgumentParser()
  argparser.add_argument("--join_det", type=str, default=" and  ||| the")
  argparser.add_argument("--join_pron", type=str, default=" and  ||| it")
  
  args = argparser.parse_args()

  JOINING_MATERIAL_DET = args.join_det
  JOINING_MATERIAL_PRON = args.join_pron
  
  sentences = []
  
  #NEGATION
  
  pair_id = 0
  for key in ALL_STIMS:
    for noun in ALL_STIMS[key]["nouns"]:
      for verb in ALL_STIMS[key]["verbs"]:
        for continuation in ALL_STIMS[key]["continuations"]:
          person = random.choice(PERSON_NAMES)
          pos_sent = person + " " + verb[0] + " " + noun[0] + JOINING_MATERIAL_DET + " " + noun[1] + "  ||| " + continuation + "."
          neg_sent = person + " " + verb[1] + " " + noun[0] + JOINING_MATERIAL_DET + " " + noun[1] + "  ||| " +  continuation + "."
          sentences.append({"pair_id": pair_id, "sentence": pos_sent, "type": "negation", "pronoun": 0, "preferred": 1, "noun": noun[1], "verb": verb[2]})
          sentences.append({"pair_id": pair_id, "sentence": neg_sent, "type": "negation", "pronoun": 0, "preferred": 0, "noun": noun[1], "verb": verb[2]})
          
          pair_id += 1
          # with pronouns
          pos_sent = person + " " + verb[0] + " " + noun[0] + JOINING_MATERIAL_PRON + "  ||| " + continuation + "."
          neg_sent = person + " " + verb[1] + " " + noun[0] + JOINING_MATERIAL_PRON + "  ||| " + continuation + "."
          sentences.append({"pair_id": pair_id, "sentence": pos_sent, "type": "negation", "pronoun": 1, "preferred": 1, "noun": noun[1], "verb": verb[2]})
          sentences.append({"pair_id": pair_id, "sentence": neg_sent, "type": "negation", "pronoun": 1, "preferred": 0, "noun": noun[1], "verb": verb[2]})
          pair_id += 1
  
  # FACTIVES
  
  for key in ALL_STIMS:
    for noun in ALL_STIMS[key]["nouns"]:
      for verb in ALL_STIMS[key]["verbs"]:
        for continuation in ALL_STIMS[key]["continuations"]:
          person = random.choice(PERSON_NAMES)
          pos_sent = "I know that " + person + " " + verb[0] + " " + noun[0] + JOINING_MATERIAL_DET + " " + noun[1] + "  ||| " + continuation + "."
          neg_sent = "I doubt that " + person + " " + verb[0] + " " + noun[0] + JOINING_MATERIAL_DET + " " + noun[1] + "  ||| " +  continuation + "."
          sentences.append({"pair_id": pair_id, "sentence": pos_sent, "type": "factive", "pronoun": 0, "preferred": 1, "noun": noun[1], "verb": verb[2]})
          sentences.append({"pair_id": pair_id, "sentence": neg_sent, "type": "factive", "pronoun": 0, "preferred": 0, "noun": noun[1], "verb": verb[2]})
          
          pair_id += 1
          # with pronouns
          pos_sent = "I know that " + person + " " + verb[0] + " " + noun[0] + JOINING_MATERIAL_PRON + "  ||| " + continuation + "."
          neg_sent = "I doubt that " + person + " " + verb[0] + " " + noun[0] + JOINING_MATERIAL_PRON + "  ||| " + continuation + "."
          sentences.append({"pair_id": pair_id, "sentence": pos_sent, "type": "factive", "pronoun": 1, "preferred": 1, "noun": noun[1], "verb": verb[2]})
          sentences.append({"pair_id": pair_id, "sentence": neg_sent, "type": "factive", "pronoun": 1, "preferred": 0, "noun": noun[1], "verb": verb[2]})
          pair_id += 1
          
  
  
  
  
  
  
  writer = csv.DictWriter(sys.stdout, fieldnames=sentences[0].keys())
  writer.writeheader()
  writer.writerows(sentences)

        
        
if __name__ == '__main__':
  main()   
        
        
      
      