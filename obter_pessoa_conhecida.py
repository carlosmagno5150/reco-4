import lib_dir
import lib_image
from tqdm import tqdm


encodings = []
names = []
encodings, names = lib_image.get_known_people(encodings, names)
dirs = lib_dir.ask_open_directory()
files = lib_dir.get_files(dirs)
pbar = tqdm(files)
sb = []
for file in pbar:
    image_url_original = file
    image_url = lib_image.check_image_for_faces(file)
    image_unknown, image_unknown_location, image_unknown_faces_encoding = lib_image.get_image_attributes(image_url)
    msgs = lib_image.check_image_for_known_face(image_url_original, image_unknown, image_unknown_location, image_unknown_faces_encoding, encodings, names)
    for m in msgs:
        sb.append(m)
lib_image.write_to_file(sb)    
