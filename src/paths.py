from pathlib import Path


class PathManager:
    root: Path
    logs: Path

    def __init__(self, root, folder_name: str = None):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.folder_name = folder_name
        self._setup_folders()

    def _setup_folders(self):
        output_folder = self.root / "Outputs"
        if self.folder_name:
            output_folder = output_folder / self.folder_name

        self.resize_inputs = self._make_directory("Inputs")
        self.resize_outputs_multi = self._make_directory("multiprocessing", root=output_folder)
        self.resize_outputs_async = self._make_directory("async", root=output_folder)
        self.resize_outputs_sync = self._make_directory("sync", root=output_folder)

    def _make_directory(self, directory, root: Path = None):
        directory_path = root / directory if root else self.root / directory
        directory_path.mkdir(parents=True, exist_ok=True)
        return directory_path


IMAGE_TYPES = (
    '*.jpg',
    '*.png',
    '*.jpeg'
)


def get_images_from_folder(folder_path: Path):
    files_grabbed = []
    for files in IMAGE_TYPES:
        files_grabbed.extend(list(folder_path.glob(files)))

    return files_grabbed
