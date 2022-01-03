import cv2 as cv
import settings
import lib_dir
from PIL import Image
import face_recognition
import uuid
from tqdm import tqdm
import os


def new_guid():
    return f'{uuid.uuid4().hex}'


def open_image(image_url):
    img = Image.open(image_url)


def create_frame(image, location, label):
    top, right, bottom, left = location
    cv.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 1)
    if label != "":
        cv.putText(image, label, (left + 3, bottom + 14), cv.FONT_HERSHEY_DUPLEX, 0.4, (255, 255, 255), 1)


def render_image(image_obj):
    rgb_img = cv.cvtColor(image_obj, cv.COLOR_BGR2RGB)
    cv.imshow('Face ', rgb_img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def get_count_faces(image_url):
    img = face_recognition.load_image_file(image_url)
    return len(face_recognition.face_locations(img))


def get_faces_and_bounding_boxes(filepath):
    face = face_recognition.load_image_file(filepath)
    face_bounding_boxes = face_recognition.face_locations(face)
    return face, face_bounding_boxes


def get_image_attributes(img_url):
    # print(f'image:: {img_url}')
    image_unknown = face_recognition.load_image_file(img_url)
    image_unknown_location = face_recognition.face_locations(image_unknown)
    image_unknown_faces_encoding = face_recognition.face_encodings(image_unknown, image_unknown_location)
    return image_unknown, image_unknown_location, image_unknown_faces_encoding


def check_image_for_faces(image_url):
    image_url = resize_image(image_url)
    faces_found = get_count_faces(image_url)
    # print(f'asdf: {image_url} - {faces_found}')
    if faces_found > 0:
        return image_url
    # print(f'#1 nenhum rosto encontrado na imagem {image_url}')
    image_name_split = image_url.split('/')
    image_path_resized = settings.get_resized_dir()
    new_image_name = f'{image_path_resized}/{image_name_split[len(image_name_split) - 1]}'
    img = Image.open(image_url)
    img = img.rotate(180)
    # img.show()
    img.save(new_image_name)
    faces_found = get_count_faces(new_image_name)
    if faces_found > 1:
        return new_image_name

    # print(f'#2 nenhum rosto encontrado na imagem {new_image_name}')
    img = img.rotate(180)
    img = img.rotate(90)
    img.save(new_image_name)
    # img.show()
    faces_found = get_count_faces(new_image_name)
    if faces_found > 1:
        return new_image_name

    # print(f'#3 nenhum rosto encontrado na imagem {new_image_name}')
    return image_url


def resize_image(image_url):
    basewidth = settings.get_resized_basewidth()
    image_name_split = image_url.split('/')
    image_path = settings.get_unknown_dir()
    new_image_name = f'{image_path}/resized/1_{image_name_split[len(image_name_split) - 1]}'
    # print(f'resize_image{image_url} \n {new_image_name}')
    img = Image.open(image_url)
    if img.size[0] > 1920 or img.size[1] > 800:
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        # img.show()
        img.save(new_image_name)
        return new_image_name
    return image_url


def append_known_people(encodings, names, filenames):
    pbar = tqdm(filenames)
    for person in pbar:
        pbar.set_description(person)
        face, face_bounding_boxes = get_faces_and_bounding_boxes(f'{person}')
        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)
            encodings.append(face_enc)
            names.append(person)
        else:
            os.remove(f"{person}")
    return encodings, names


def get_known_people(enc, nams):
    encodings = []
    names = []
    known_dir = settings.get_known_dir()
    known_people = lib_dir.get_files(known_dir)

    # print(f'reconhecidos: {known_people}')

    if len(known_people) == 0:
        # print('Nenhuma pessoa conhecida')
        return encodings, names

    pbar = tqdm(known_people)
    for person in pbar:
        pbar.set_description(person)
        face, face_bounding_boxes = get_faces_and_bounding_boxes(f'{person}')
        if len(face_bounding_boxes) == 1:
            face_enc = face_recognition.face_encodings(face)
            encodings.append(face_enc)
            names.append(person)
        else:
            os.remove(f"{person}")
    return encodings, names


def check_if_face_is_valid(image_obj, image_locations, image_encodings):
    for image_location, image_encoding in zip(image_locations, image_encodings):
        top, right, bottom, left = image_location
        face_image = image_obj[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        image_id = new_guid()
        temp_name = f"{settings.get_unknown_dir()}/{image_id}.png"
        pil_image.save(temp_name)
        if get_count_faces(temp_name) == 0:
            os.remove(temp_name)
        # else:
        #     pil_image.show()
        #     pessoa = input("\nQuem é esse ? ")
        #     if pessoa != "":
        #         fullfilename = f"{settings.get_known_dir()}/{lib_dir.check_name_in_known_dir(pessoa)}.png"
        #         pil_image.save(fullfilename)


def check_image(image_unknown, image_unknown_location, image_unknown_faces_encoding, encodings, names,
                nomear_desconhecido=0):
    novas = []
    image_unknown2 = image_unknown.copy()
    found = 0
    for location, face_encoding in zip(image_unknown_location, image_unknown_faces_encoding):
        foundThis = 0
        for known_image, known_name in zip(encodings, names):
            is_target_face = face_recognition.compare_faces(face_encoding, known_image, tolerance=0.4)
            if is_target_face[0]:
                # print(lib_dir.get_name(known_name))
                # print(known_name)
                create_frame(image_unknown, location, lib_dir.get_name(known_name))
                found = 1
                foundThis = 1
                break

        if nomear_desconhecido == 1:
            if foundThis == 0:
                top, right, bottom, left = location
                face_image = image_unknown2[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                temp_name = f"{settings.get_known_dir()}/semnometa.png"
                pil_image.save(temp_name)
                if get_count_faces(temp_name) == 0:
                    os.remove(temp_name)
                else:
                    pil_image.show()
                    pessoa = input("Quem é esse ? ")
                    if pessoa != "":
                        fullfilename = f"{settings.get_known_dir()}/{lib_dir.check_name_in_known_dir(pessoa)}.png"
                        pil_image.save(fullfilename)
                        novas.append(fullfilename)
    render_image(image_unknown)
    return novas


if __name__ == '__main__':
    # lib_dir.create_default_dir()
    image_url = lib_dir.ask_open_file()
    resize_image(image_url)
    # image_url = check_image_for_faces(image_url)
    # image_url = resize_image(image_url)
