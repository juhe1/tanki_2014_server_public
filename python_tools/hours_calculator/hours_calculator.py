from datetime import datetime

# Using readlines()
file1 = open("hours.txt", 'r')
lines = file1.readlines()

# Strips the newline character
line = lines[0]

hours = 0

for line in lines:
    line = line[:-1]

    splited = line.split(" - ")
    clock_times = []

    for t in splited:
        clock_times += t.split(" ")

    clock_times = clock_times[1:]
    print(clock_times)
    i = 0
    while i < len(clock_times):
        _format = "%H.%M"
        hours += (datetime.strptime(clock_times[i+1], _format) - datetime.strptime(clock_times[i], _format)).seconds / (60*60)
        i += 2

print("hours", hours)
