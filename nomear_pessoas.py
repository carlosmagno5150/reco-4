import lib_dir
import lib_image


lib_dir.create_default_dir()

encodings = []
names = []

encodings, names = lib_image.get_known_people(encodings, names)

continuar = 1

while continuar == 1:
    image_url = lib_dir.ask_open_file()
    if image_url == "":
        break

    image_url = lib_image.check_image_for_faces(image_url)
    print(image_url)
    image_unknown, image_unknown_location, image_unknown_faces_encoding = lib_image.get_image_attributes(image_url)
    novas = lib_image.check_image(image_unknown, image_unknown_location, image_unknown_faces_encoding, encodings, names, 1)
    if len(novas) > 0:
        # encodings, names = lib_image.get_known_people(encodings, names)
        lib_image.append_known_people(encodings, names, novas)
    # for nova in novas:
        # photo.obter_novo_reconhecido(nova, encodings, names)
    # encodings, names = photo.obter_reconhecidos(encodings, names)