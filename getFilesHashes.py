import os
import hashlib
import datetime
import argparse
import signal

class TimeoutException(Exception):
    pass

def handler(signum, frame):
    raise TimeoutException()

def calculate_hash(file_path, block_size=1024):
    hasher = hashlib.sha256()
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(5)  # Set the alarm to 5 seconds
    try:
        with open(file_path, 'rb') as file:
            buf = file.read(block_size)
            hasher.update(buf)
    except TimeoutException:
        print(f"Operation timed out on file: {file_path}")
        return None
    finally:
        signal.alarm(0)  # Disable the alarm
    return hasher.hexdigest()



def main(directory, output_file):
    with open(output_file, 'w') as f:
        counter = 0
        for root, dirs, files in os.walk(directory):
            if root.startswith(('/System', '/private', '/usr', '/Library/Caches/', '/Library/Containers', '/Users/giz/Library/Containers', '/Users/giz/.cache', '/dev')):
                print(f'skipping {root}')
                continue

            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # counter += 1
                    # if counter % 100 == 0:
                    print(f'Processing file: {file_path}')
                    hash_value = calculate_hash(file_path)
                    size = os.path.getsize(file_path)
                    mtime = os.path.getmtime(file_path)
                    date = datetime.datetime.fromtimestamp(mtime)
                    f.write(f'{hash_value},{size},{date},{file_path}\n')
                except Exception as e:
                    print(f"Couldn't process file {file_path}: {e}")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate file hashes.')
    parser.add_argument('directory', type=str, help='The directory to scan.')
    parser.add_argument('output_file', type=str, help='The file to output to.')
    args = parser.parse_args()
    main(args.directory, args.output_file)
    print(f'finished....')
