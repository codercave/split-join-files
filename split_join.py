from pathlib import Path
import click


read_buffer_size = 1024


def _chunk_file(file, extension, destination, size):

    d = Path(destination)
    d.mkdir(parents=True, exist_ok=True)

    current_chunk_size = 0
    current_chunk = 1
    done_reading = False
    while not done_reading:
        with open(f'{destination}/{current_chunk}{extension}.chk', 'ab') as chunk:
            while True:
                bfr = file.read(read_buffer_size)
                if not bfr:
                    done_reading = True
                    break

                chunk.write(bfr)
                current_chunk_size += len(bfr)
                if current_chunk_size + read_buffer_size > size:
                    current_chunk += 1
                    current_chunk_size = 0
                    break


@click.command(name='split', help='split a file into chunks')
@click.option('--file', help='path to the file that has to be split')
@click.option('--destination', default='.', help='path of the directory that will contain the chunks')
@click.option('--size', default=100000000, help='max size of a chunk')
def _split(file, destination, size):
    f = Path(file)
    
    if f.exists():
        with open(f, 'rb') as file_stream:
            _chunk_file(file_stream, f.suffix, destination, size)


@click.command(name='join', help='join pieces so that you obtain your original file')
@click.option('--source-dir', default='.', help='directory of where the chunks are')
@click.option('--output', default='join', help='file name of the re-joined file')
def _join(source_dir, output):
    p = Path(source_dir)
    if not p.exists():
        print('source folder not valid')
        return

    chunks = list(p.rglob('*.chk'))
    chunks.sort()
    extension = chunks[0].suffixes[0]

    with open(f'{output}{extension}', 'ab') as file:
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
