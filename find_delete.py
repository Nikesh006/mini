with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'delete' in line.lower() and 'route' in line.lower():
        print(f"--- MATCH AT LINE {i+1} ---")
        print(line.strip())
        for j in range(1, 25):
            if i+j < len(lines):
                print(lines[i+j].rstrip())
        print("-" * 40)
