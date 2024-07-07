import base64
from io import BytesIO
import numpy as np
import tensorflow
from PIL import Image

import json
from flask import Flask, abort, jsonify, make_response, request
from flask_cors import cross_origin, CORS
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/analizeMole', methods=['GET', 'POST'])
@cross_origin()
def analizeMole():
    img = request.files.get("imageInput")
    encoded_img = base64.b64encode(img.read()).decode("ascii")
    print(encoded_img)

    model = tensorflow.keras.models.load_model('./model_antrenat__.h5') # 53%

# Dicționar pentru a converti etichetele numerice în clase
    label_dict = {
        0: 'non-cancerigen',
        1: 'cancerigen'
    }

    def classify_image(image_path, model):
        try:
            # Încarcă imaginea
            img = Image.open(image_path)

            # Redimensionează imaginea la dimensiunea necesară (224x224)
            img = img.resize((224, 224))

            # Convertim imaginea la RGB
            img = img.convert('RGB')

            # Convertim imaginea într-un tablou numpy și scalăm valorile
            img_array = np.array(img) / 255.0

            # Adaugă o dimensiune suplimentară pentru lot (batch) pentru a corespunde așteptărilor modelului
            img_array = np.expand_dims(img_array, axis=0)

            # Efectuează predicția
            prediction = model.predict(img_array)

            # Obține indexul clasei cu cea mai mare probabilitate
            predicted_class = np.argmax(prediction, axis=1)[0]

            # Convertim eticheta numerică în clasa corespunzătoare
            predicted_label = label_dict[predicted_class]

            return predicted_label

        except Exception as e:
            print(f"Eroare la procesarea imaginii: {e}")
            return None


    # Clasifică imaginea și afișează rezultatul
    predicted_label = classify_image(BytesIO(base64.b64decode(encoded_img)), model)
    print(f'Clasa prezisă pentru imaginea selectată este: {predicted_label}')

    responseBody = jsonify({"response" : predicted_label})
    resp = make_response(responseBody, 201)
    return resp

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000)
# Încarcă modelul salvat