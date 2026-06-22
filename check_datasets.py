import os

def main():
    root = os.path.join(os.getcwd(), "dataset", "raw")
    subfolders = ["posture", "eye", "lighting", "behaviour"]
    for sub in subfolders:
        path = os.path.join(root, sub)
        if not os.path.isdir(path):
            print(f"{sub}: MISSING folder")
            continue
        file_list = []
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                file_list.append(os.path.join(dirpath, f))
        print(f"{sub}: {len(file_list)} files")
        if file_list:
            # Show a few sample files relative to raw folder
            rel_samples = [os.path.relpath(p, root) for p in file_list[:3]]
            print("  Sample files:", ", ".join(rel_samples))

if __name__ == "__main__":
    main()
