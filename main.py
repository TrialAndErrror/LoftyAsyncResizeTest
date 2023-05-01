import asyncio
import json
import tempfile
import datetime
from pathlib import Path
from time import perf_counter

from PIL import Image

from src.async_resize import async_resize_images
from src.blocking import blocking_resize_one_image
from src.mp_resize import multiprocessing_resize_image


def do_multiprocessing(image_file: Path, out_dir: Path):
    image_name = image_file.stem
    image_data = Image.open(image_file)
    multiprocessing_resize_image(image_data, image_name, out_dir)


def do_blocking(image_file: Path, out_dir: Path):
    image_name = image_file.stem
    image_data = Image.open(image_file)
    blocking_resize_one_image(image_data, image_name, out_dir)


def save_results(file_path, data):
    with open(file_path, 'w+') as file:
        json.dump(data, file)

    for category, result in data.items():
        print(f"Running in {category} mode took {result:.2f} seconds (~{result / 60:.2f} minutes)")


def run_test(image_filename: str, num_iterations: int):
    input_file = Path.cwd() / "src" / "tests" / "sample_data" / image_filename
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir)

        async_start = perf_counter()
        for num in range(num_iterations):
            asyncio.run(async_resize_images(input_file, output_dir))
        async_stop = perf_counter()

        sync_start = perf_counter()
        for num in range(num_iterations):
            do_blocking(input_file, output_dir)
        sync_stop = perf_counter()

        mp_start = perf_counter()
        for num in range(num_iterations):
            do_multiprocessing(input_file, output_dir)
        mp_stop = perf_counter()

    async_duration = async_stop - async_start
    blocking_duration = sync_stop - sync_start
    mp_duration = mp_stop - mp_start

    results = {
        "blocking": blocking_duration,
        "async": async_duration,
        "multiprocessing": mp_duration
    }

    return results


def run_tiny(results_dir):
    print("Running Tiny...")
    results = run_test("1KB.jpg", 1_000)
    save_results(results_dir / f"Tiny Results: {datetime.datetime.now().isoformat()}", results)


def run_small(results_dir):
    print("Running Small...")
    results = run_test("1MB.jpg", 100)
    save_results(results_dir / f"Small Results: {datetime.datetime.now().isoformat()}", results)


def run_medium(results_dir):
    print("Running Medium...")
    results = run_test("10MB.jpg", 10)
    save_results(results_dir / f"Medium Results: {datetime.datetime.now().isoformat()}", results)


def run_all():
    results_dir = Path.cwd() / "Results"
    results_dir.mkdir(exist_ok=True)

    run_tiny(results_dir)
    run_small(results_dir)
    run_medium(results_dir)

if __name__ == "__main__":
    run_all()