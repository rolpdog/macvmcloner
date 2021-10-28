from pathlib import Path

import os
import subprocess
import uuid

def main():
    source_image_path = '/Users/mdavis/Parallels/1201_gharunner.macvm'
    ephemeral_image_dir = '/Users/mdavis/Parallels/_ephemeral'
    prl_macvm_app_path = '/Applications/Parallels Desktop.app/Contents/MacOS/Parallels Mac VM.app/Contents/MacOS/prl_macvm_app'

    if not Path(source_image_path).is_dir():
        raise FileNotFoundError(f'source image dir {source_image_path} does not exist')

    Path(ephemeral_image_dir).mkdir(parents=True, exist_ok=True)

    if not Path(prl_macvm_app_path).is_file():
        raise FileNotFoundError(f'prl_macvm_app not found at {prl_macvm_app_path}')

    while True:
        image_dir = Path(ephemeral_image_dir).joinpath(f'_ephemeral_{uuid.uuid4()}')

        print(f'cloning to {image_dir}')
        subprocess.run(f'cp -c -r "{source_image_path}" "{image_dir}"', shell=True)

        try:
            print(f'starting ephemeral VM at {image_dir}')
            args = [prl_macvm_app_path, '--openvm', image_dir]
            subprocess.run(args)
            print(f'ephemeral VM at {image_dir} has exited')
        finally:
            subprocess.run(f'rm -rf {image_dir}', shell=True)


if __name__ == '__main__':
    main()
