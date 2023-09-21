# Profile the simulation
python3 -m cProfile -o profile_v4.stats simulate.py v4

# Build the flamegraph
flameprof --font-size 16 --row-height 24 --width 1600  profile_v4.stats > profile_v4.svg