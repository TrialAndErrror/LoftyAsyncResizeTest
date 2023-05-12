import asyncio
import json
import string
from datetime import datetime
from pathlib import Path
import random
from time import perf_counter

from PIL import Image

from src.async_resize import async_resize_images
from src.blocking import blocking_resize_one_image
from src.mp_resize import advanced_mp_resize_image, multiprocessing_resize_image
from src.paths import PathManager, get_images_from_folder


def do_multiprocessing(all_images: list[Path], out_dir: Path):
    print("Using multiprocessing")
    for image_file in all_images:
        image_name = image_file.stem
        print(f"Multiprocessing: Resizing {image_name}")
        image_data = Image.open(image_file)
        # multiprocessing_resize_image(image_data, image_name, out_dir)
        advanced_mp_resize_image(image_data, image_name, out_dir)


def do_blocking(all_images: list[Path], out_dir: Path):
    for image_file in all_images:
        image_name = image_file.stem
        print(f"Sync: Resizing {image_name}")
        image_data = Image.open(image_file)
        blocking_resize_one_image(image_data, image_name, out_dir)


def save_results(file_path, data):
    with open(file_path, 'w+') as file:
        json.dump(data, file)

    for category, result in data.items():
        print(f"Running in {category} mode took {result:.2f} seconds (~{result / 60:.2f} minutes)")


def main():
    new_folder_path = ''.join(random.choices(string.ascii_uppercase, k=5))
    path_manager = PathManager(Path.cwd(), folder_name=new_folder_path)
    all_images = get_images_from_folder(path_manager.resize_inputs)
    if all_images:

        async_start = perf_counter()
        asyncio.run(async_resize_images(all_images, path_manager.resize_outputs_async))
        async_stop = perf_counter()

        sync_start = perf_counter()
        do_blocking(all_images, path_manager.resize_outputs_sync)
        sync_stop = perf_counter()

        mp_start = perf_counter()
        do_multiprocessing(all_images, path_manager.resize_outputs_multi)
        mp_stop = perf_counter()

        async_duration = async_stop - async_start
        blocking_duration = sync_stop - sync_start
        mp_duration = mp_stop - mp_start

        results = {
            "blocking": blocking_duration,
            "async": async_duration,
            "multiprocessing": mp_duration
        }

        results_path = path_manager.root / f"results [{new_folder_path}] ({datetime.now().strftime('%Y-%m-%d_%h-%m-%s')}).json"
        save_results(results_path, results)
    else:
        print(f"No images found! Please place input images in '{path_manager.resize_inputs.absolute()}'")


if __name__ == "__main__":
    main()
