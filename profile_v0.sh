# Profile the simulation
python3 -m cProfile -o profile_v0.stats simulate.py v0

# Build the flamegraph
flameprof --font-size 16 --row-height 24 --width 1600  profile_v0.stats > profile_v0.svg