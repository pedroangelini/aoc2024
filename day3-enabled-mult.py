import re
from utils.input_utils import get_input_from_args, str_seq_to_int_tup

input=get_input_from_args()
mult_matcher=re.compile(r"mul\((\d+),(\d+)\)")

disabled_pat=re.compile(r"don\'t\(\).*do\(\)")
clean_input = disabled_pat.sub('',input)

#print(disabled_pat.findall(input))
#print(input)
#print(clean_input)

acum =0

for match in mult_matcher.findall(clean_input):
  a,b=str_seq_to_int_tup(match)
  print(f"{a=}, {b=}, {(a*b)=}")
  acum += a*b

print(acum)
