import os

bad_files = []

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "rb") as f:
                data = f.read()
                if b"\x00" in data:
                    bad_files.append(path)

if bad_files:
    print("Archivos con NULL bytes encontrados:")
    for bf in bad_files:
        print("  ->", bf)
else:
    print("✅ No hay archivos con NULL bytes")
