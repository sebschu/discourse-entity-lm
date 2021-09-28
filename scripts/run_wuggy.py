from wuggy import WuggyGenerator
from fractions import Fraction


g = WuggyGenerator()
g.load("orthographic_english")
f = open("/Users/sebschu/Dropbox/Uni/RA/common-ground/discourse-entity-tracking/stimuli/hand_written_stimuli.wuggy.txt")
for line in f:
  line = line.strip()
  printed = False
  try:
      for w in g.generate_classic([line], ncandidates_per_sequence=1, subsyllabic_segment_overlap_ratio=None, max_search_time_per_sequence=30):
          print (w["word"], w["pseudoword"])
          printed = True
  except Exception as e:
      pass
  if not printed:
      print(line, "asdf")
