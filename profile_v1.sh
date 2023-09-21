# Profile the simulation
python3 -m cProfile -o profile_v1.stats simulate.py v1

# Build the flamegraph
flameprof --font-size 16 --row-height 24 --width 1600  profile_v1.stats > profile_v1.svg