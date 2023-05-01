from pathlib import Path

RESIZE_STEP_SIZE = 0.2


def blocking_resize_one_image(image_data, image_name, out_dir: Path):
    for num in range(1, 6):
        old_x, old_y = image_data.size
        resize_factor = 1 + (RESIZE_STEP_SIZE * num)
        new_size = int(old_x * resize_factor), int(old_y * resize_factor)

        new_out_path = str(out_dir / f"{image_name} ({resize_factor * 100}%).png")
        new_image = image_data.resize(new_size)
        new_image.save(new_out_path)
