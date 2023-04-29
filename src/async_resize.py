import asyncio
from pathlib import Path

from PIL import Image
from aioEasyPillow import Editor

RESIZE_STEP_SIZE = 0.2


async def async_resize_images(all_images: list[Path], out_dir: Path):
    for image_file in all_images:
        image_name = image_file.stem
        print(f"Async Resizing {image_name}")

        image_data = Image.open(image_file)
        image = Editor(image_data)
        await make_sizes(image, out_dir, image_name)


async def make_sizes(image, image_dir, image_name):
    print(f"Starting {image_name}")
    async with asyncio.TaskGroup() as tg:
        for num in range(1, 6):
            task = tg.create_task(async_make_resized_outputs(image, image_dir, image_name, num))

    print(f"{image_name} is now complete.")


async def async_make_resized_outputs(image: Editor, output_dir: Path, image_name: str, magnification_factor: int):
    old_x, old_y = image.image.size
    resize_factor = 1 + (RESIZE_STEP_SIZE * magnification_factor)
    new_size = int(old_x * resize_factor), int(old_y * resize_factor)
    print(f"Resize factor: {resize_factor}")

    new_out_path = str(output_dir / f"{image_name} ({resize_factor * 100}%).png")

    new_image = await image.resize(new_size)
    return await new_image.save(new_out_path)
