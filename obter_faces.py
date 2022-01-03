import lib_dir
import lib_image
from tqdm import tqdm


def get_faces_from_dir(dir_path):
    subs = lib_dir.get_sub_directories(dir_path)
    pbar = tqdm(subs)
    for sub in pbar:
        pbar.set_description(sub)
        get_faces_from_dir(sub)

    files = lib_dir.get_files(dir_path)
    pbar1 = tqdm(files)
    for file in pbar1:
        image_url = lib_image.check_image_for_faces(file)
        image_unknown, image_unknown_location, image_unknown_faces_encoding = lib_image.get_image_attributes(image_url)
        lib_image.check_if_face_is_valid(image_unknown, image_unknown_location, image_unknown_faces_encoding)

        # novas = lib_image.check_image(image_unknown, image_unknown_location, image_unknown_faces_encoding,
        # encodings, names, 0)


if __name__ == '__main__':
    lib_dir.create_default_dir()
    dirs = lib_dir.ask_open_directory()
    get_faces_from_dir(dirs)

