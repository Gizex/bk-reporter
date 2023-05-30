with open('data.txt', 'r') as file:
    lines = file.read().split("\n")

trimmed_lines = []
for line in lines:
    parts = line.split("-")
    if len(parts) >= 3:
        line = "-".join(parts[1:3])
    trimmed_lines.append(line.upper())

with open('trimmed_data.txt', 'w') as file:
    file.write("\n".join(trimmed_lines))
