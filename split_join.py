from pathlib import Path
import click


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


@click.command(name='split', help='split a file into chunks')
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


@click.command(name='join', help='join pieces so that you obtain your original file')
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


@click.group()
def main():
    print('split-join files')


main.add_command(_split)
main.add_command(_join)


if __name__ == '__main__':
    main()
