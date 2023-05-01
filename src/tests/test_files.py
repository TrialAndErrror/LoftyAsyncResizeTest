import asyncio
import datetime
from pathlib import Path
from time import perf_counter

from main import do_blocking, do_multiprocessing, save_results
from src.async_resize import async_resize_images


def get_images_path(filename: str = None) -> Path:
    path = Path.cwd() / "src" / "tests" / "sample_data"
    path.mkdir(exist_ok=True)

    if filename:
        return path / filename
    return path


def get_results_path():
    path = Path.cwd() / "src" / "tests" / "results"
    path.mkdir(exist_ok=True)
    return path


def test_tiny_file(tmp_path):
    num_iters = 1000
    resize_images("1KB.jpg", num_iters, tmp_path)


def test_small_file(tmp_path):
    num_iters = 100
    resize_images("1MB.jpg", num_iters, tmp_path)


def test_medium_file(tmp_path):
    num_iters = 10
    resize_images("10MB", num_iters, tmp_path)


def resize_images(image_file: str, num_iters: int, tmp_path: Path):
    input_file = get_images_path(image_file)

    results_path = get_results_path()
    tmp_path.mkdir(exist_ok=True, parents=True)

    print("Running Async...")
    async_start = perf_counter()
    for num in range(num_iters):
        asyncio.run(async_resize_images(input_file, tmp_path))
    async_stop = perf_counter()

    print("Running Sync...")
    sync_start = perf_counter()
    for num in range(num_iters):
        do_blocking(input_file, tmp_path)
    sync_stop = perf_counter()

    print("Running Multiprocessing...")
    mp_start = perf_counter()
    for num in range(num_iters):
        do_multiprocessing(input_file, tmp_path)
    mp_stop = perf_counter()

    results = {
        "blocking": sync_stop - sync_start,
        "async": async_stop - async_start,
        "multiprocessing": mp_stop - mp_start
    }

    results_filename = datetime.datetime.now().isoformat() + " results"
    save_results(results_path / results_filename, results)

