from sys import argv
from pathlib import Path


read_buffer_size = 1024
chunk_size = 1024 * 100000


def _chunk_file(file, extension):
    current_chunk_size = 0
    current_chunk = 1
    done_reading = False
    while not done_reading:
        with open(f'{current_chunk}{extension}.chk', 'ab') as chunk:
            while True:
                bfr = file.read(read_buffer_size)
                if not bfr:
                    done_reading = True
                    break

                chunk.write(bfr)
                current_chunk_size += len(bfr)
                if current_chunk_size + read_buffer_size > chunk_size:
                    current_chunk += 1
                    current_chunk_size = 0
                    break


def _split():
    p = Path.cwd()
    file_to_split = None
    for f in p.iterdir():
        if f.is_file() and f.name[0] != '.':
            file_to_split = f
            break

    if file_to_split:
        with open(file_to_split, 'rb') as file:
            _chunk_file(file, file_to_split.suffix)


def _join():
    p = Path.cwd()

    chunks = list(p.rglob('*.chk'))
    chunks.sort()
    extension = chunks[0].suffixes[0]

    with open(f'join{extension}', 'ab') as file:
        for chunk in chunks:   
            with open(chunk, 'rb') as piece:
                while True:
                    bfr = piece.read(read_buffer_size)
                    if not bfr:
                        break
                    file.write(bfr)


def main():
    
    command = argv[1]

    if command.lower() == 'split':
        _split()
    elif command.lower() == 'join':
        _join()
    else:
        print('use either split or join')


if __name__ == '__main__':
    main()
