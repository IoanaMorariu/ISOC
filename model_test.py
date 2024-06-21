import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# Încarcă modelul salvat
model = load_model('model_antrenat__.h5') # 53%

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

# Calea către imaginea pe care dorești să o clasifici
image_path = './a.png'

# Clasifică imaginea și afișează rezultatul
predicted_label = classify_image(image_path, model)
print(f'Clasa prezisă pentru imaginea selectată este: {predicted_label}')
