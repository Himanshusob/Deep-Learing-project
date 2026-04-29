from fastapi import FastAPI, UploadFile, File
import uvicorn
import shutil
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

app = FastAPI()

model = load_model("final_model.h5")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    with open("temp.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    img = Image.open("temp.jpg").resize((224,224))
    img = np.array(img)/255.0
    img = np.expand_dims(img, axis=0)

    pred = model.predict(img)[0][0]

    return {
        "label": "fake" if pred > 0.5 else "real",
        "prob": float(pred)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
