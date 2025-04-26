import os
import uuid
import click
import const
import random
import logging

from PIL import Image
from tqdm import tqdm
from samila import GenerativeImage, GenerateMode, Projection, Marker
from samila.params import VALID_COLORS
from models.formula import Formula

LOG_FILE = "app.log"
COLORS = VALID_COLORS.copy()
COLORS.remove("black")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, mode="w"), logging.StreamHandler()],
)
logger = logging.getLogger("generative_art")


def log_metadata(metadata: dict) -> None:
    """
    Log metadata information about generated art.

    This function iterates through a dictionary of metadata, where each key is
    a UUID representing a generated image, and each value is the corresponding
    seed used for generation. It logs this information using the configured logger.

    Args:
        metadata (dict): A dictionary containing UUIDs as keys and seeds as values.

    Returns:
        None
    """
    for k, v in metadata.items():
        logger.info(f"UUID: {k} - Seed: {v}")


def generate_art(
    data_folder: str,
    images_folder: str,
    single_color: bool = False,
    total: int = 5,
    using_formula: bool = False,
) -> None:
    """
    Generate generative art images and save them along with their metadata.

    This function creates generative art images using the `samila` library.
    It generates a specified number of images, saves the image files and their
    corresponding data files, and logs metadata about the generated images.

    Args:
        data_folder (str): Path to the folder where generated data files will be saved.
        images_folder (str): Path to the folder where generated image files will be saved.
        single_color (bool, optional): If True, use a single color for the art. Defaults to False.
        total (int, optional): Total number of images to generate. Defaults to 5.
        using_formula (bool, optional): If True, use custom formulas for generating art. Defaults to False.

    Returns:
        None
    """
    formula = Formula()
    metadata = {}

    for _ in tqdm(
        range(total), desc=f"Generating {total} Art", colour="green", ascii=" #"
    ):
        image_uuid = uuid.uuid4()
        data_path = f"{data_folder}/{image_uuid}.json"
        image_path = f"{images_folder}/{image_uuid}.png"

        g = GenerativeImage(
            function1=formula.calc_formula2_value if using_formula else None,
            function2=formula.calc_formula1_value if using_formula else None,
        )
        g.generate(start=-5, step=0.01, stop=3, mode=random.choice(list(GenerateMode)))
        g.plot(
            projection=random.choice(list(Projection)),
            color=COLORS[random.randrange(0, len(COLORS))] if single_color else g.data2,
            cmap=[] if single_color else [random.choice(COLORS) for _ in range(10)],
            bgcolor="black",
            alpha=0.6,
            # marker=marker_mode,
            # spot_size=0.5,
        )
        g.save_data(file_adr=data_path)
        g.save_image(image_path, depth=5)  # more depth more higher resolution

        # convert to webp format
        image_webp_path = image_path.replace(".png", ".webp")
        image = Image.open(image_path)
        image = image.convert("RGB")
        image.save(image_webp_path, "webp")

        os.remove(image_path)  # remove original png file
        metadata[str(image_uuid)] = g.seed

    log_metadata(metadata)


@click.command()
@click.option(
    "--single-color",
    "-s",
    is_flag=False,
    help="Use a single color for the art.",
)
@click.option(
    "--total",
    "-t",
    default=1,
    help="Total number of images to generate.",
)
@click.option(
    "--using-formula",
    "-f",
    is_flag=False,
    help="Use custom formulas for generating art.",
)
def main(single_color: bool, total: int, using_formula: bool) -> None:
    """
    Main function to set up the output folder structure and generate art.

    This function ensures that the required folder structure is created:
    - 'output' folder
    - 'output/data' folder for storing generated data files
    - 'output/images' folder for storing generated image files

    After setting up the folders, it calls the `generate_art` function to create
    generative art and save the results in the appropriate folders.
    """
    output_folder = const.OUTPUT_FOLDER
    data_folder = const.DATA_FOLDER
    images_folder = const.IMAGES_FOLDER

    # create output folder
    if os.path.isdir(output_folder) is False:
        os.makedirs(output_folder)
    if not os.path.isdir(data_folder):
        os.makedirs(data_folder)
    if not os.path.isdir(images_folder):
        os.makedirs(images_folder)

    generate_art(data_folder, images_folder, single_color, total, using_formula)


if __name__ == "__main__":
    main()
