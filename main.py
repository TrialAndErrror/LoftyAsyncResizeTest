import asyncio
import json
import string
from datetime import datetime
from pathlib import Path
import random
from time import perf_counter
from typing import Callable

from PIL import Image

from src.async_resize import async_resize_images
from src.blocking import blocking_resize_one_image
from src.mp_resize import (
    advanced_mp_resize_image,
    multiprocessing_resize_image,
    joblib_mp_resize_image,
)
from src.paths import PathManager, get_images_from_folder


def do_joblib_multiprocessing(all_images: list[Path], out_dir: Path):
    print("Using multiprocessing from Joblib")
    for image_file in all_images:
        image_name = image_file.stem
        print(f"Multiprocessing: Resizing {image_name}")
        image_data = Image.open(image_file)
        joblib_mp_resize_image(image_data, image_name, out_dir)


def do_pool_multiprocessing(all_images: list[Path], out_dir: Path):
    print("Using multiprocessing with Pool")
    for image_file in all_images:
        image_name = image_file.stem
        print(f"Multiprocessing: Resizing {image_name}")
        image_data = Image.open(image_file)
        advanced_mp_resize_image(image_data, image_name, out_dir)


def do_multiprocessing(all_images: list[Path], out_dir: Path):
    print("Using multiprocessing")
    for image_file in all_images:
        image_name = image_file.stem
        print(f"Multiprocessing: Resizing {image_name}")
        image_data = Image.open(image_file)
        multiprocessing_resize_image(image_data, image_name, out_dir)


def do_blocking(all_images: list[Path], out_dir: Path):
    for image_file in all_images:
        image_name = image_file.stem
        print(f"Sync: Resizing {image_name}")
        image_data = Image.open(image_file)
        blocking_resize_one_image(image_data, image_name, out_dir)


def do_async(all_images, out_dir):
    asyncio.run(async_resize_images(all_images, out_dir))


def save_results(file_path, overall_summary, all_results):
    output_data = {"summary": overall_summary, "results": all_results}
    with open(file_path, "w+") as file:
        json.dump(output_data, file)

    for category, result in overall_summary.items():
        print(
            f"Running in {category} mode took {result:.2f} seconds (~{result / 60:.2f} minutes)"
        )


def run_with_timer(func: Callable, all_images: list, out_dir: Path):
    start = perf_counter()
    func(all_images, out_dir)
    stop = perf_counter()

    return stop - start


def main():
    new_folder_path = "".join(random.choices(string.ascii_uppercase, k=5))
    path_manager = PathManager(Path.cwd(), folder_name=new_folder_path)
    all_images = get_images_from_folder(path_manager.resize_inputs)
    if all_images:
        test_categories = [
            ("blocking", do_blocking, path_manager.resize_outputs_sync),
            ("async", do_async, path_manager.resize_outputs_multi_standard),
            (
                "multiprocessing",
                do_multiprocessing,
                path_manager.resize_outputs_multi_pool,
            ),
            (
                "multiprocessing-pool",
                do_pool_multiprocessing,
                path_manager.resize_outputs_multi_joblib,
            ),
            (
                "multiprocessing-joblib",
                do_joblib_multiprocessing,
                path_manager.resize_outputs_async,
            ),
        ]

        results = {
            name: run_with_timer(test_func, all_images, out_dir)
            for name, test_func, out_dir in test_categories
        }

        return results
    else:
        print(
            f"No images found! Please place input images in '{path_manager.resize_inputs.absolute()}'"
        )


if __name__ == "__main__":
    num_rounds = 3
    categories = [
        "blocking",
        "async",
        "multiprocessing",
        "multiprocessing-pool",
        "multiprocessing-joblib",
    ]

    new_folder_path = "".join(random.choices(string.ascii_uppercase, k=5))
    path_manager = PathManager(Path.cwd(), folder_name=new_folder_path)

    results_path = (
        path_manager.root
        / f"results [{new_folder_path}] ({datetime.now().strftime('%Y-%m-%d_%h-%m-%s')}).json"
    )

    all_results = {key: list() for key in categories}

    for num in range(num_rounds):
        results = main()

        for category, time in results.items():
            all_results[category].append(time)

    overall_summary = {
        key: sum(value) / num_rounds for key, value in all_results.items()
    }

    save_results(results_path, overall_summary, all_results)
