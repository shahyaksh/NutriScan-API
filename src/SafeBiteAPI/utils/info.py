import re
from src.SafeBiteAPI.utils import regex


def check_salt_quantity(nutrition_table):
    """
    High: more than 1.5g of salt per 100g (or 0.6g sodium)
    Low: 0.3g of salt or less per 100g (or 0.1g sodium)
    Source:https://www.nhs.uk/live-well/eat-well/food-guidelines-and-food-labels/how-to-read-food-labels/
    :param nutrition_table:
    :return: {%quantity,High/Medium/Low content}
    """
    quant = 0
    if 'Sodium' in nutrition_table.keys():
        quant = regex.separate_unit(nutrition_table['Sodium'])
        if quant > 0.6:
            return {'percentage': f'{quant}%', 'comment': 'High Sodium Content'}
        elif quant < 0.1:
            return {'percentage': f'{quant}%', 'comment': 'Low Sodium Content'}
        else:
            return {'percentage': f'{quant}%', 'comment': 'Medium Sodium Content'}
    elif 'Salt' in nutrition_table.keys():
        quant = regex.separate_unit(nutrition_table['Salt'])
        if quant > 1.5:
            return {'percentage': f'{quant}%', 'comment': 'High Salt Content'}
        elif quant <= 0.3:
            return {'percentage': f'{quant}%', 'comment': 'Low Salt Content'}
        else:
            return {'percentage': f'{quant}%', 'comment': 'Medium Salt Content'}
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
    quant = 0
    if 'Sugar' in nutrition_table.keys():
        quant = regex.separate_unit(nutrition_table['Sugar'])
        if quant > 22.2:
            return {'percentage': f'{quant}%', 'comment': 'High Sugar Content'}
        elif quant < 5:
            return {'percentage': f'{quant}%', 'comment': 'Low Sugar Content'}
        else:
            return {'percentage': f'{quant}%', 'comment': 'Medium Sugar Content'}
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
    quant = 0
    if 'Total Fat' in nutrition_table.keys():
        quant = regex.separate_unit(nutrition_table['Total Fat'])
        if quant > 17.5:
            return {'percentage': f'{quant}%', 'comment': 'High Fat Content'}
        elif quant <= 3:
            return {'percentage': f'{quant}%', 'comment': 'Low Fat Content'}
        else:
            return {'percentage': f'{quant}%', 'comment': 'Medium Fat Content'}
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
    quant = 0
    if 'Saturated Fat' in nutrition_table.keys():
        quant = regex.separate_unit(nutrition_table['Saturated Fat'])
        if quant > 5:
            return {'percentage': f'{quant}%', 'comment': 'High Saturated Fat Content'}
        elif quant <= 1.5:
            return {'percentage': f'{quant}%', 'comment': 'Low Saturated Fat Content'}
        else:
            return {'percentage': f'{quant}%', 'comment': 'Medium Saturated Fat Content'}
    else:
        return 'Not able to detect'


def check_quantity(nutrition_table):
    result = {}

    result['Salt'] = check_salt_quantity(nutrition_table)
    result['Sugar'] = check_sugar_quantity(nutrition_table)
    result['Total Fat'] = check_total_fat_quantity(nutrition_table)
    result['Saturated Fat'] = check_saturated_fat_quantity(nutrition_table)
    return result


def check_allergens(ingredient_list):
    """
    Potential Allergens: Milk, Soy, Nuts, Gluten

    :param ingredient_list:
    :return: List of allergens that are present
    """
    detect_milk = re.compile('[Mm]ilk')
    detect_soy = re.compile('[Ss]oy')
    detect_nuts = re.compile('[Nn]uts')
    detect_gluten = re.compile('[Gg]luten]')
    allergen_list = []
    if detect_milk.findall(ingredient_list[0]):
        allergen_list.append('Milk')
    if detect_soy.findall(ingredient_list[0]):
        allergen_list.append('Soy')
    if detect_nuts.findall(ingredient_list[0]):
        allergen_list.append('Nuts')
    if detect_gluten.findall(ingredient_list[0]):
        allergen_list.append('Gluten')
    if allergen_list is []:
        return 'No allergen detected'
    else:
        return allergen_list


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
    final_score = 0
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
            print({v: quant})
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


def check_user_preferences(ingredient_list: list, nutrition_table: dict, user_preferences: dict):
    """

    :param ingredient_list:
    :param user_preferences:{
                                Nutrition_Quantity:{
                                                    'Salt': 0/1,
                                                    'Sugar': 0/1,
                                                    'Fat': 0/1,
                                                    'Saturated Fat': 0/1
                                                 },
                                Allergens:{
                                                'Milk':0/1,
                                                'Soy':0/1,
                                                'Peanuts':0/1,
                                                'Gluten':0/1

                                           }


                            }

    :return: final_result
    """
    final_result = {}

    nutrition_quantity_result = check_quantity(nutrition_table)

    for k,v in user_preferences['Nutrition_Quantity'].values():
        if v==1:
            final_result['Nutrition_Quantity'][k]=nutrition_quantity_result[k]
        else:
            final_result['Nutrition_Quantity'][k] = 'Not Important'

    allergen_list = check_allergens(ingredient_list)

    if allergen_list:
        for k, v in user_preferences['Allergens'].values():
            if v == 1 and k in allergen_list:
                final_result['Allergens'][k] = f'Contains {k}'

    return final_result


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

    list = [['Kair.Red Chilly Powder. Edible Oil,', 'INGREDIENTS:', 'lodized Salt,Mustard,&Ground Spices.',
             '(Asafoetida.CloveAcidity Regulator', 'Acetic Acid (INS260).Contains Permitted',
             'Class lPreservative(INS211)','Milk'
             'NETWEIGHT:200q']]
    additive_info = regex.get_additives_from_ingredients(list)
    a = get_ingredients_info(additive_info, col)
    for i in a:
        print(i)

    client.close()
