from pathlib import Path

from PIL import Image
import multiprocessing as mp
from joblib import Parallel, delayed


RESIZE_STEP_SIZE = 0.2


def make_one_thread(image: Image, output_dir, image_name, magnification_factor):
    old_x, old_y = image.size
    resize_factor = 1 + (RESIZE_STEP_SIZE * magnification_factor)
    new_size = int(old_x * resize_factor), int(old_y * resize_factor)
    new_out_path = str(output_dir / f"{image_name} ({resize_factor * 100}%).png")

    new_image = image.resize(new_size)
    new_image.save(new_out_path)


def multiprocessing_resize_image(image_data: Image, image_name: str, out_dir: Path):
    for num in range(1, 6):
        task = mp.Process(target=make_one_thread, args=(image_data.copy(), out_dir, image_name, num))
        task.start()
        task.join()


def advanced_mp_resize_image(image_data: Image, image_name: str, out_dir: Path):
    pool = mp.Pool()
    processes = [pool.apply_async(make_one_thread, args=(image_data.copy(), out_dir, image_name, num)) for num in range(6)]
    result = [p.get() for p in processes]


def joblib_mp_resize_image(image_data: Image, image_name: str, out_dir: Path):
    Parallel(n_jobs=3)(delayed(make_one_thread)(image_data.copy(), out_dir, image_name, i) for i in range(1, 6))