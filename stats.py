import pstats

p = pstats.Stats("original_profile.txt")

p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats(pstats.SortKey.CUMULATIVE).print_stats(10)
