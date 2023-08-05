import sys

# check if filenames are given as command line arguments
if len(sys.argv) < 4:
    print("Error: Please provide filenames as command line arguments.")
    print("Usage: python script.py [hashes_file] [all_files_file] [duplicates_file]")
    sys.exit(1)

# get filenames from command line arguments
hashes_file = sys.argv[1]
all_files_file = sys.argv[2]
duplicates_file = sys.argv[3]

# load the duplicate hashes into a set for efficient lookup
with open(hashes_file, 'r') as f:
    duplicate_hashes = set(line.strip() for line in f)

excessive_space = 0
seen_duplicates = set()

# iterate over the sorted hashes file and write matches to the output file
with open(all_files_file, 'r') as f, open(duplicates_file, 'w') as out:
    for line in f:
        parts = line.split(',')
        hash = parts[0]
        size = int(parts[1])
        if hash in duplicate_hashes:
            out.write(line)
            if hash in seen_duplicates:
                excessive_space += size
            else:
                seen_duplicates.add(hash)

# convert excessive space from bytes to gigabytes
excessive_space_gb = excessive_space / (1024 ** 3)

print(f'Total excessive space: {excessive_space_gb:.2f} GB')

