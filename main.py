from src.SafeBiteAPI.utils import regex, info
from fastapi import FastAPI, File, UploadFile,Form, HTTPException
import uuid
from paddleocr import PaddleOCR
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

# Database Name
db = client["FoodAdditives"]

# Collection Name
col = db["Additives"]

app = FastAPI(debug=True)
ING_IMGDIR = "images/ingredients/"
NUTRI_IMGDIR = "images/nutritiontable/"

ocr_model = PaddleOCR(lang='en', use_gpu=True)


def convert_table_to_dict(table):
    labels = ['Energy', 'Saturated Fat', 'Protein', 'Carbohydrate', 'Total Sugars'
        , 'Added Sugars', 'Total Fat', 'Trans Fat', 'Sodium']
    table_dict = {}
    index = 0
    for text in table[0]:
        for label in labels:
            if label in text:
                table_dict[text] = table[0][index + 1]
        index += 1
    return table_dict


def get_results_of_ocr(img_path: str):
    result = ocr_model.ocr(img_path)
    boxes = []
    texts = []
    scores = []
    boxes.append([result[0][i][0] for i in range(len(result[0]))])  #
    texts.append([result[0][j][1][0] for j in range(len(result[0]))])
    scores.append([result[0][k][1][1] for k in range(len(result[0]))])
    return texts


# def check_percentage(text):
#     lst = ['Total Fat','Saturated Fat','Sugars','Salt']
#     for


@app.get("/")
async def home():
    return "Welcome to OCR API"


@app.post("/upload/ingredients")
async def get_image_by_upload(file: UploadFile = File(...), user_preference: dict = Form(...)):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    path = f"{ING_IMGDIR}{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)
    text = get_results_of_ocr(path)
    additive = regex.get_additives_from_ingredients(text)
    if additive is not None:
        additive_information = info.get_ingredients_info(additive, col)
    else:
        additive_information = "No additives detected "
    return {"ingredients": text, 'additives': additive_information}


@app.post("/upload/nutritiontable")
async def get_image_by_upload(file: UploadFile = File(...), user_preference: dict = Form(...)):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    path = f"{NUTRI_IMGDIR}{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)
    texts = get_results_of_ocr(path)
    print(texts)
    table_dict = convert_table_to_dict(texts)
    if table_dict != {}:
        nutri_score = info.get_nutriscore(table_dict)
        return {"Table": table_dict, "Nutri Score": nutri_score}
    else:
        return "Sorry! Cannot Calculate Nutri Score try taking clear image"

# logger.info("Welcome to Safe Bite API")
