import re
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from NutriScanAPI.utils import regex


def check_salt_quantity(nutrition_table):
    """
    High: more than 1.5g of salt per 100g (or 0.6g sodium)
    Low: 0.3g of salt or less per 100g (or 0.1g sodium)
    Source:https://www.nhs.uk/live-well/eat-well/food-guidelines-and-food-labels/how-to-read-food-labels/
    :param nutrition_table:
    :return: {%quantity,High/Medium/Low content}
    """

    if 'Sodium' in nutrition_table.keys():
        result = regex.separate_unit(nutrition_table['Sodium'])

        if type(result) is tuple:
            print(result)
            quant_value = result[0] / 1000
        else:
            quant_value = result / 1000

        if quant_value > 0.6:
            return {'percentage': f'{round(quant_value, 2)}%', 'comment': 'High Sodium Content'}
        elif quant_value < 0.1:
            return {'percentage': f'{round(quant_value, 2)}%', 'comment': 'Low Sodium Content'}
        else:
            return {'percentage': f'{round(quant_value, 2)}%', 'comment': 'Medium Sodium Content'}
    elif 'Salt' in nutrition_table.keys():

        result = regex.separate_unit(nutrition_table['Salt'])

        if type(result) is tuple:
            print(result)
            quant_value = result[0] / 1000
        else:
            quant_value = result / 1000

        if quant_value > 1.5:
            return {'percentage': f'{quant_value}%', 'comment': 'High Salt Content'}
        elif quant_value <= 0.3:
            return {'percentage': f'{quant_value}%', 'comment': 'Low Salt Content'}
        else:
            return {'percentage': f'{quant_value}%', 'comment': 'Medium Salt Content'}
    else:
        return 'Not able to detect'


def check_sugar_quantity(nutrition_table):
    """
    High: more than 22.5g of total sugars per 100g
    Low: 5g of total sugars or less per 100g
    Source:https://www.nhs.uk/live-well/eat-well/food-guidelines-and-food-labels/how-to-read-food-labels/
    :param nutrition_table:
    :return: {%quantity,High/Medium/Low content}
    """

    if 'Total Sugar' in nutrition_table.keys():

        result = regex.separate_unit(nutrition_table['Total Sugar'])

        if type(result) is tuple:
            quant_value = result[0]
        else:
            quant_value = result

        if quant_value > 22.2:
            return {'percentage': f'{quant_value}%', 'comment': 'High Sugar Content'}
        elif quant_value < 5:
            return {'percentage': f'{quant_value}%', 'comment': 'Low Sugar Content'}
        else:
            return {'percentage': f'{quant_value}%', 'comment': 'Medium Sugar Content'}
    else:
        return 'Not able to detect'


def check_total_fat_quantity(nutrition_table):
    """
    High: more than 17.5g of fat per 100g
    Low: 3g of fat or less per 100g
    Source:https://www.nhs.uk/live-well/eat-well/food-guidelines-and-food-labels/how-to-read-food-labels/
    :param nutrition_table:
    :return: {%quantity,High/Medium/Low content}
    """

    if 'Total Fat' in nutrition_table.keys():

        result = regex.separate_unit(nutrition_table['Total Fat'])

        if type(result) is tuple:
            quant_value = result[0]
        else:
            quant_value = result

        if quant_value > 17.5:
            return {'percentage': f'{quant_value}%', 'comment': 'High Fat Content'}
        elif quant_value <= 3:
            return {'percentage': f'{quant_value}%', 'comment': 'Low Fat Content'}
        else:
            return {'percentage': f'{quant_value}%', 'comment': 'Medium Fat Content'}
    else:
        return 'Not able to detect'


def check_saturated_fat_quantity(nutrition_table):
    """
    High: more than 5g of saturated fat per 100g
    Low: 1.5g of saturated fat or less per 100g
    Source:https://www.nhs.uk/live-well/eat-well/food-guidelines-and-food-labels/how-to-read-food-labels/
    :param nutrition_table:
    :return: {%quantity,High/Medium/Low content}
    """

    if 'Saturated Fat' in nutrition_table.keys():

        result = regex.separate_unit(nutrition_table['Saturated Fat'])
        if type(result) is tuple:
            quant_value = result[0]
        else:
            quant_value = result
        if quant_value > 5:
            return {'percentage': f'{quant_value}%', 'comment': 'High Saturated Fat Content'}
        elif quant_value <= 1.5:
            return {'percentage': f'{quant_value}%', 'comment': 'Low Saturated Fat Content'}
        else:
            return {'percentage': f'{quant_value}%', 'comment': 'Medium Saturated Fat Content'}
    else:
        return 'Not able to detect'


def check_quantity(nutrition_table):
    result = {
        'Salt': check_salt_quantity(nutrition_table),
        'Sugar': check_sugar_quantity(nutrition_table),
        'Total Fat': check_total_fat_quantity(nutrition_table),
        'Saturated Fat': check_saturated_fat_quantity(nutrition_table)
    }

    return result


def check_allergens(ingredient_list):
    """
    Potential Allergens: Milk, Soy, Nuts, Gluten

    :param ingredient_list:
    :return: List of allergens that are present
    """
    detect_milk = re.compile('milk', re.I)
    detect_soy = re.compile('soy', re.I)
    detect_nuts = re.compile('nuts', re.I)
    detect_gluten = re.compile('gluten]', re.I)
    allergen_list = []
    ing_lst_to_str = ''.join(ingredient_list[0])
    if detect_milk.findall(ing_lst_to_str):
        allergen_list.append('milk')
    if detect_soy.findall(ing_lst_to_str):
        allergen_list.append('soy')
    if detect_nuts.findall(ing_lst_to_str):
        allergen_list.append('nuts')
    if detect_gluten.findall(ing_lst_to_str):
        allergen_list.append('gluten')
    if allergen_list is []:
        return 'No allergen detected'
    else:
        return allergen_list


def check_ingredients(ingredient_list):
    """

    :param ingredient_list:
    :return: weather the food is vegan or veg, is palm oil free,is without onion or garlic
    """
    detect_palm_oil = re.compile('palm', re.I)
    detect_onion = re.compile('onion', re.I)
    detect_garlic = re.compile('garlic', re.I)
    ing_lst_to_str = ''.join(ingredient_list[0])
    result = []
    if detect_palm_oil.findall(ing_lst_to_str):
        result.append("palm oil")
    if detect_garlic.findall(ing_lst_to_str) and detect_onion.findall(ing_lst_to_str):
        result.append("onion and garlic")
    elif detect_garlic.findall(ing_lst_to_str):
        result.append("garlic")
    elif detect_onion.findall(ing_lst_to_str):
        result.append("onion")

    return result


def check_users_nutrition_preferences(nutrition_table: dict, user_nutrition_preferences: dict):
    """

    :param nutrition_table:
    :param user_nutrition_preferences:    {
                                            'Salt': 0/1,
                                            'Sugar': 0/1,
                                            'Fat': 0/1,
                                            'Saturated Fat': 0/1
                                          }

    :return: final_result
    """
    final_result = {}

    nutrition_quantity_result = check_quantity(nutrition_table)

    for k, v in user_nutrition_preferences.items():
        if v == 1:
            final_result[k] = nutrition_quantity_result[k]
        else:
            final_result[k] = 'Not Important'

    return final_result


def check_users_allergen_preferences(ingredient_list: list, user_allergen_preferences: dict):
    """

    :param ingredient_list:
    :param user_allergen_preferences:{

                                        'Milk':0/1,
                                        'Soy':0/1,
                                        'Peanuts':0/1,
                                        'Gluten':0/1

                                    }

    :return: final_result
    """
    final_result = {}

    allergen_list = check_allergens(ingredient_list)

    if allergen_list:
        for k, v in user_allergen_preferences.items():
            if v == 1 and k.lower() in allergen_list:
                final_result[k] = f'Contains {k}'

    return final_result


def check_users_ingredient_preferences(ingredient_list: list, user_ingredient_preferences: dict):
    """

    :param ingredient_list:
    :param user_ingredient_preferences:{

                                        'Palm Oil':0/1,
                                        'Onion and Garlic':0/1
                                    }

    :return: final_result
    """
    final_result = {}

    detected_ingredient_list = check_ingredients(ingredient_list)

    if detected_ingredient_list:
        for k, v in user_ingredient_preferences.items():

            if v == 1 and k.lower() in detected_ingredient_list:
                final_result[k] = f'Contains {k}'

    return final_result


def get_nutriscore(nutrition_table: dict):
    """
    :param nutrition_table

    negative_elements: if present in high amount might be harmful to once health

    positive_elements: have positive effect on health when present in good quantity

    category:  A --> Best Nutritional Quality (final_score <= -1)
                              to
               E --> Weakest Nutritional Quality (final_score >= 20)

    Negative_Points: negative_element_quantity % negative_element_threshold

    Positive_Points: positive_element_quantity % positive_element_threshold

    :return: final_score (negative_points-positive_points)
    """
    negative_elements = {'Energy': 335, 'Saturated Fat': 1, 'Sugars': 4.5, 'Sodium': 90}
    positive_elements = {'Protein': 1.6, 'Fibers': 0.9}
    category = {'A': -1, 'B': 2, 'C': 10, 'D': 18, 'E': 20}
    negative_points = 0
    positive_points = 0
    for k, v in nutrition_table.items():

        if k in negative_elements.keys():
            quant = regex.separate_unit(v)
            if type(quant) is tuple:
                quant = quant[0]
            negative_points += int((quant % negative_elements[k]))

        if k in positive_elements.keys():
            quant = regex.separate_unit(v)
            if type(quant) is tuple:
                quant = quant[0]
            positive_points = positive_points + int((quant % positive_elements[k]))

    final_score = negative_points - positive_points
    if final_score <= category['A']:
        return 'A'
    elif final_score <= category['B']:
        return 'B'
    elif final_score <= category['C']:
        return 'C'
    elif final_score <= category['D']:
        return 'D'
    elif final_score >= category['E']:
        return 'E'


def get_ingredients_info(additive_list, collection):
    """

    :param additive_list: list of additives present in the ingredients
    :param collection: mongodb database collection from which data is to fetched
    :return: additive_information fetched from database
    """
    additive_information = []
    for additive in additive_list:
        info = collection.find({'code': additive}, {'_id': 0})
        # Convert the cursor result to a list of dictionaries
        additive_information.extend(info)

    return additive_information


if __name__ == '__main__':
    import pymongo

    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Database Name
    db = client["FoodAdditives"]

    # Collection Name
    col = db["Additives"]

    ing_list = [["COATED WAFER LAYERS",
                 "Ingredients:Sugar.Hydrogenated",
                 "vegetable fat,Refined wheat flour. Milk",
                 "solids,Starch,Cocoa solids 5%",
                 "Palmolein oil,Emulsifiers (442,322,476),Edible salt",
                 "Yeast, Raising agent 500(ii,Improver Enzyme",
                 "CONTAINS ADDED FLAVOUR NATURAL, NATURE IDENTICAL AND",
                 "ARTIPICIAL (CARAMEL AND ETHYL VANILLIN) FLAVOURING SUBSTANCES)",
                 "Allergen informationContains Gluten & WheatSoynuts."]]

    additive_info = regex.get_additives_from_ingredients(ing_list)
    a = get_ingredients_info(additive_info, col)
    for i in a:
        print(i)
    user_allergen_preferences_1 = {

        'milk': 1,
        'soy': 1,
        'peanuts': 1,
        'nuts': 1,
        'gluten': 1

    }
    user_nutrition_preferences_1 = {
        'Salt': 0,
        'Sugar': 0,
        'Total Fat': 1,
        'Saturated Fat': 1
    }
    user_ingredient_preferences_1={
        'Palm Oil': 1,
        'Onion and Garlic': 1
    }
    nutrition_table_1 = {
        "Energy": "527.69",
        "Protein": "6.08",
        "Total Fat": "30.09g",
        "Saturated Fat": "13.65",
        "Trans Fat": "0.04",
        "Total Sugar": "5.78",
        "Carbohydrate": "58.26",
        "Sodium": "469.27g"
    }
    allergen_info = check_users_allergen_preferences(ing_list, user_allergen_preferences_1)
    nutrition_info = check_users_nutrition_preferences(nutrition_table_1, user_nutrition_preferences_1)
    ingredient_info = check_users_ingredient_preferences(ing_list, user_ingredient_preferences_1)
    print(allergen_info)
    print(nutrition_info)
    print(ingredient_info)

    client.close()
