import os
import const


def delete_file(filename: str) -> None:
    """
    Delete a file from the data and images folders if the name matches.

    Args:
        filename (str): The name of the file to delete (without folder path).

    Returns:
        None
    """
    data_file_path = os.path.join(const.DATA_FOLDER, f"{filename}.json")
    image_file_path = os.path.join(const.IMAGES_FOLDER, f"{filename}.png")

    # Delete from data folder
    if os.path.exists(data_file_path):
        os.remove(data_file_path)

    # Delete from images folder
    if os.path.exists(image_file_path):
        os.remove(image_file_path)


if __name__ == "__main__":
    while True:
        filename_to_delete = input("Enter the filename to delete: ").strip()

        if filename_to_delete.lower() == "exit":
            break
        delete_file(filename_to_delete)
