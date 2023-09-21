# Profile the simulation
python3 -m cProfile -o profile_v2.stats simulate.py v2

# Build the flamegraph
flameprof --font-size 16 --row-height 24 --width 1600  profile_v2.stats > profile_v2.svg