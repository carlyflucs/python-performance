# Profile the simulation
python3 -m cProfile -o profile_v5.stats simulate.py v5

# Build the flamegraph
flameprof --font-size 16 --row-height 24 --width 1600  profile_v5.stats > profile_v5.svg