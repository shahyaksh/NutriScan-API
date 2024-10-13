# NutriScan API

**NutriScan API** is a FastAPI-powered service that processes images of ingredient lists and nutrition tables from food products. It uses Optical Character Recognition (OCR) to extract text from the images, checks for the presence of food additives, allergens, and nutritional content, and evaluates the data against user preferences (e.g., allergies, dietary restrictions).

---

## Features
- Extracts text from images of ingredients and nutrition tables using PaddleOCR.
- Identifies and retrieves information about food additives from a MongoDB database.
- Checks the ingredients and nutritional information against user-specified allergens and ingredient preferences.
- Calculates Nutri-Score based on the extracted nutrition data.
  
---

## Technologies Used
- **FastAPI**: Web framework for building APIs.
- **PaddleOCR**: OCR tool to extract text from images.
- **MongoDB**: Database to store and retrieve food additive information.
- **Pymongo**: Python client for interacting with MongoDB.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/shahyaksh/NutriScanAPI.git
cd NutriScanAPI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Ensure you have a MongoDB instance running or use MongoDB Atlas for cloud storage. Replace the MongoDB URI in the script with your credentials, or set it using environment variables.

### 4. Run the FastAPI Server
```bash
uvicorn main:app --reload
```

The API will be accessible at `http://127.0.0.1:8000`.

---

## Endpoints

### 1. **GET `/`**  
**Description**: Health check route to verify the API is running.  
**Response**:
```json
{
  "message": "Welcome to OCR API"
}
```

### 2. **POST `/upload/ingredients`**
**Description**: Upload an image of an ingredient list. The API processes the image using OCR, detects food additives, allergens, and specific ingredients based on user preferences.  
**Parameters**:
- **file** (*UploadFile*): The image of the ingredient list.
- **milk** (*int*): User's preference for milk allergens (1 for allergic, 0 for non-allergic).
- **nuts** (*int*): User's preference for nuts allergens (1 for allergic, 0 for non-allergic).
- **soy** (*int*): User's preference for soy allergens (1 for allergic, 0 for non-allergic).
- **gluten** (*int*): User's preference for gluten allergens (1 for allergic, 0 for non-allergic).
- **palm_oil** (*int*): User's preference for palm oil (1 for avoiding, 0 for no issue).
- **onion_and_garlic** (*int*): User's preference for avoiding onion and garlic (1 for avoiding, 0 for no issue).

**Response**:
- **ingredients** (*str*): Extracted ingredient list.
- **additives** (*str*): Detected additives and their information.
- **allergen_info** (*dict*): Information about potential allergens based on user preferences.
- **ingredients_info** (*dict*): Information about ingredients like palm oil, onion, or garlic based on user preferences.

**Example Request (via CURL)**:
```bash
curl -X 'POST' 'http://127.0.0.1:8000/upload/ingredients' \
  -F 'file=@path_to_image.jpg' \
  -F 'milk=1' -F 'nuts=0' -F 'soy=1' -F 'gluten=0' \
  -F 'palm_oil=1' -F 'onion_and_garlic=1'
```

**Example Response**:
```json
{
  "ingredients": "sugar, wheat flour, vegetable oil (palm), milk powder...",
  "additives": "E202 (Potassium sorbate): Preservative, generally safe...",
  "allergen_info": {
    "milk": "Contains milk",
    "soy": "Safe for soy allergy",
    "peanuts": "Safe for peanut allergy",
    "gluten": "Contains gluten"
  },
  "ingredients_info": {
    "Palm Oil": "Contains palm oil",
    "Onion": "No onion detected",
    "Garlic": "No garlic detected"
  }
}
```

### 3. **POST `/upload/nutritiontable`**
**Description**: Upload an image of a nutrition table. The API processes the image, extracts the nutrition information, and calculates a Nutri-Score based on the data. It also checks user preferences for salt, sugar, total fat, and saturated fat content.  
**Parameters**:
- **file** (*UploadFile*): The image of the nutrition table.
- **salt** (*int*): User's preference for avoiding high salt content (1 for strict, 0 for lenient).
- **sugar** (*int*): User's preference for avoiding high sugar content (1 for strict, 0 for lenient).
- **total_fat** (*int*): User's preference for avoiding high fat content (1 for strict, 0 for lenient).
- **sat_fat** (*int*): User's preference for avoiding high saturated fat content (1 for strict, 0 for lenient).

**Response**:
- **Table** (*dict*): Extracted nutrition information.
- **Nutri Score** (*str*): Calculated Nutri-Score based on the nutrition table.
- **additional info** (*dict*): Information based on user preferences for salt, sugar, total fat, and saturated fat.

**Example Request (via CURL)**:
```bash
curl -X 'POST' 'http://127.0.0.1:8000/upload/nutritiontable' \
  -F 'file=@path_to_image.jpg' \
  -F 'salt=1' -F 'sugar=1' -F 'total_fat=0' -F 'sat_fat=0'
```

**Example Response**:
```json
{
  "Table": {
    "Energy": "250 kcal",
    "Total Fat": "12 g",
    "Saturated Fat": "5 g",
    "Carbohydrate": "30 g",
    "Sugar": "15 g",
    "Sodium": "0.5 g"
  },
  "Nutri Score": "C",
  "Salt": "High salt content",
  "Sugar": "High sugar content",
  "Total Fat": "Fat content is acceptable",
  "Saturated Fat": "Saturated fat content is acceptable"
}
```



## MongoDB Integration
This API connects to a MongoDB database to retrieve information about food additives. Ensure your MongoDB instance is running and that the connection URI is properly set. The database and collection names used are:
- **Database**: `FoodAdditives`
- **Collection**: `Additives`

# API Demo
Watch working of the API [here](https://drive.google.com/file/d/1x40lju3RnY4X-gbP00R4zvgIircnKc5G/view?usp=drive_link)

# Flutter Application
Get our Flutter App [here](https://github.com/bhakti1509/nutricsan)

# Checkout the Full video
Get the full video of out NutriScan Application [here](https://drive.google.com/file/d/1XL3nSaGOhTcGiCDLzhRyKHcaNAXea17H/view?usp=drive_link)

## License
This project is licensed under the MIT License.
