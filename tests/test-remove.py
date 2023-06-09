from amtools.filesystem import fsutil

with open('f1.txt', 'r') as f:
    text = f.read()

print(fsutil.remove_metadata(text))
