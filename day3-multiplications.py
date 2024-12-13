import re
from utils.input_utils import get_input_from_args, str_seq_to_int_tup


input=get_input_from_args()
mult_matcher=re.compile(r"mul\((\d+),(\d+)\)")

acum =0

for match in mult_matcher.findall(input):
  a,b=str_seq_to_int_tup(match)
  print(f"{a=}, {b=}, {(a*b)=}")
  acum += a*b

print(acum)
