import face_recognition
from os import path
# import numpy as np

faces_to_compare = []
filenames_to_compare = []


class Face:
    def __init__(self, app):
        self.saves = app.config["saves"]
        self.db = app.db
        self.faces = []
        self.known_encoding_faces = []
        self.face_user_keys = {}
        self.load_all()

    def load_user_by_index_key(self, index_key=0):

        key_str = str(index_key)

        if key_str in self.face_user_keys:
            return self.face_user_keys[key_str]

        return None

    def load_known_file_by_name(self, name):
        saves_known = path.join(self.saves, 'known')
        return path.join(saves_known, name)

    def load_all(self):
        results = self.db.select('SELECT faces.id, faces.user_id, faces.filename, faces.created FROM faces')

        for row in results:
            print(row)
            user_id = row[1]
            filename = row[2]
            face = {
                "id": row[0],
                "user_id": user_id,
                "filename": filename,
                "created": row[3]
            }
            self.faces.append(face)
            face_image = face_recognition.load_image_file(self.load_known_file_by_name(filename))
            face_image_encoding = face_recognition.face_encodings(face_image)[0]

            index_key = len(self.known_encoding_faces)
            self.known_encoding_faces.append(face_image_encoding)
            index_key_string = str(index_key)
            self.face_user_keys['{0}'.format(index_key_string)] = user_id

    def recognize(self, file_stream):
        unknown_image = face_recognition.load_image_file(file_stream)
        unknown_encoding_images = face_recognition.face_encodings(unknown_image)[0]

        results = face_recognition.compare_faces(self.known_encoding_faces, unknown_encoding_images)

        print(results)

        if len(results) == 0:
            return

        face_index = [i for i, x in enumerate(results) if x]

        if len(face_index) == 0:
            return

        return face_index[0] + 1



    def encoding(self, file_stream):
        unknown_image = face_recognition.load_image_file(file_stream)
        unknown_encoding_images = face_recognition.face_encodings(unknown_image)[0]
        'mugshot'
        unknown_encoding_string="("

        for distance in  unknown_encoding_images:
            unknown_encoding_string+=str(distance)
            unknown_encoding_string+=str(",")

        unknown_encoding_string = unknown_encoding_string[:-1]
        unknown_encoding_string += str(")")

        return None

    def store_new(self, file_stream):
        unknown_image = face_recognition.load_image_file(file_stream)
        unknown_encoding_images = face_recognition.face_encodings(unknown_image)[0]
        self.known_encoding_faces.append(unknown_encoding_images)

