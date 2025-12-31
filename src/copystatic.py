from pathlib import Path
from loguru import logger
import shutil


def delete_dir_contents(target_dir: Path):
    # could have used shutil.rmtree - but wanted to train pathlib and recursion
    if not target_dir.exists():
        raise ValueError("path does not exist")
    if not target_dir.is_dir():
        raise ValueError("target not a directory")

    for item in target_dir.iterdir():
        if item.is_file():
            item.unlink()
            logger.debug(f"Removed {item} from {target_dir}")
        elif item.is_dir():
            delete_dir_contents(item)
            item.rmdir()
            logger.debug(f"Removed {item} directory")


def copy_directory(source: Path, target: Path):
    if not source.exists():
        raise ValueError("Source path does not exist")
    if not target.exists():
        target.mkdir()
        logger.debug(f"Created {target} directory")
    if not source.is_dir() or not target.is_dir():
        raise ValueError("not a directory")

    for item in source.iterdir():
        # TODO: for python 3.14 use copy or copy_into method from pathlib
        if item.is_file():
            shutil.copy(item, target)
            logger.debug(f"Copied {item} to {target}")
        elif item.is_dir():
            subdir_target = target.joinpath(item.name)
            copy_directory(item, subdir_target)


def replace_directory_tree(
    source: Path = Path("./static"), destination: Path = Path("./public")
):

    delete_dir_contents(destination)
    copy_directory(source, destination)
