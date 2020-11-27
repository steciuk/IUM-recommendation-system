from IUM.services.reader import read_sessions
from IUM.correlation import count_correlation
from IUM.randomizer import random_sessions

sessions = read_sessions()

production_correlation = count_correlation(sessions)

print("production_correlation", production_correlation)

for count in range(0, 10):
    shuffled_sessions = random_sessions(sessions)
    shuffled_correlation = count_correlation(shuffled_sessions)

    print("shuffled_correlation", shuffled_correlation)
