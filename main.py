from src.SafeBiteAPI.utils import regex, info
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import uuid
from paddleocr import PaddleOCR
import pymongo
from pymongo.server_api import ServerApi
import re

uri = "mongodb+srv://yakshshah:Yaksh1782@nutriscan.bsfbzvl.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = pymongo.MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# Database Name
db = client["FoodAdditives"]

# Collection Name
col = db["Additives"]

app = FastAPI(debug=True)
ING_IMGDIR = "images/ingredients/"
NUTRI_IMGDIR = "images/nutritiontable/"

ocr_model = PaddleOCR(lang='en', use_gpu=False)


def convert_nutrition_table_to_dict(table):
    labels = ['Energy', 'Saturated Fat', 'Protein', 'Carbohydrate', 'Total Sugar',
              'Added Sugars', 'Total Fat', 'Trans Fat', 'Sodium']
    table_dict = {}
    index = 0
    for text in table[0]:
        for label in labels:
            if label in text:
                table_dict[label] = table[0][index + 1]
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


@app.get("/")
async def home():
    return "Welcome to OCR API"


@app.post("/upload/ingredients")
async def get_image_by_upload(file: UploadFile = File(...), milk: int = Form(...),
                              nuts: int = Form(...), soy: int = Form(...), gluten: int = Form(...),
                              palm_oil: int = Form(...), onion_and_garlic: int = Form(...)):
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
    users_allergen_preferences = {
        'milk': milk,
        'soy': soy,
        'peanuts': nuts,
        'nuts': nuts,
        'gluten': gluten
    }
    users_ingredients_preferences = {
        'Palm Oil': palm_oil,
        'Onion and Garlic': onion_and_garlic,
        'Onion': onion_and_garlic,
        'Garlic': onion_and_garlic
    }

    allergen_info = info.check_users_allergen_preferences(text, users_allergen_preferences)
    ingredients_info = info.check_users_ingredient_preferences(text, users_ingredients_preferences)
    ing_str = re.sub('[():{}]',' ',' '.join(text[0]))
    print(ing_str)

    return {"ingredients": ing_str, 'additives': additive_information, 'allergen_info': allergen_info,
            'ingredients_info': ingredients_info}


@app.post("/upload/nutritiontable")
async def get_image_by_upload(file: UploadFile = File(...), salt: int = Form(...),
                              sugar: int = Form(...), total_fat: int = Form(...), sat_fat: int = Form(...)):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    path = f"{NUTRI_IMGDIR}{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)
    texts = get_results_of_ocr(path)
    table_dict = convert_nutrition_table_to_dict(texts)
    if table_dict != {}:
        nutri_score = info.get_nutriscore(table_dict)
        user_nutrition_preferences = {
            'Salt': salt,
            'Sugar': sugar,
            'Total Fat': total_fat,
            'Saturated Fat': sat_fat
        }
        nutrition_info = info.check_users_nutrition_preferences(table_dict, user_nutrition_preferences)
        table_data_and_nutriscore = {"Table": table_dict, "Nutri Score": nutri_score}
        for k,v in nutrition_info.items():
            table_data_and_nutriscore[k]=v

        return table_data_and_nutriscore
    else:
        return None

# logger.info("Welcome to Safe Bite API")
