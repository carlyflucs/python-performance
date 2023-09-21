# Profile the simulation
python3 -m cProfile -o profile_v3.stats simulate.py v3

# Build the flamegraph
flameprof --font-size 16 --row-height 24 --width 1600  profile_v3.stats > profile_v3.svg