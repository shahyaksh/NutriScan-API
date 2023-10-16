import re


# one of the most common OCR error of returning '9' in
# place of 'g' is being handled by this function
def change_to_g(text):
    search_ln = re.search("\d\s|\d$", text)
    if search_ln and search_ln.group().strip() == "9":
        index = search_ln.span()[0]
        text = text[:index] + "g" + text[index + 1:]

    search_lnq = re.search("\dmq\s|\dmq$", text)
    if search_lnq:
        index = search_lnq.span()[0] + 2
        text = text[:index] + "g" + text[index + 1:]
    return text


# Removes all the unnecessary noise from a string
def clean_string(string):
    pattern = "[\|\*\_\'\—\-\{}]".format('"')
    text = re.sub(pattern, "", string)
    text = re.sub(" I ", " / ", text)
    text = re.sub("^I ", "", text)
    text = re.sub("Omg", "0mg", text)
    text = re.sub("Og", "0g", text)
    text = re.sub('(?<=\d) (?=\w)', '', text)
    text = change_to_g(text)
    text = text.strip()
    return text


# Check whether a nutritional label is present in the
# string or not
def check_for_label(text, words):
    # text = text.lower()
    for i in range(len(text)):
        if any(text[i:].startswith(word) for word in words):
            return True
    return False


# Separate the value and its label from the string
def get_label_from_string(string):
    label_arr = re.findall("([A-Z][a-zA-Z]*)", string)
    label_name = ""
    label_value = ""

    if len(label_arr) == 0:
        label_name = "|" + string + '|'
    elif len(label_arr) == 1:
        label_name = label_arr[0]
    else:
        label_name = label_arr[0] + ' ' + label_arr[1]

    digit_pattern = "[-+]?\d*\.\d+g|\d+"
    value_arr = re.findall("{0}g|{0}%|{0}J|{0}kJ|{0}mg|{0}kcal".format(digit_pattern), string)
    # print(value_arr)
    if len(value_arr):
        label_value = value_arr[0]
    else:
        label_value = "|" + string + '|'
    return label_name, label_value


# Separate the unit from its value. (eg. '24g' to '24' and 'g')
def separate_unit(string):
    r1 = re.compile("(\d+[\.\,\']?\d*)([a-zA-Z]+)")
    m1 = r1.match(string)
    r2 = re.compile("(\d+[\.\,\']?\d*)")
    m2 = r2.match(string)
    if m1:
        return (float(m1.group(1).replace(',', '.').replace("'", '.')), m1.group(2))
    elif m2:
        return (float(m2.group(1).replace(',', '.').replace("'", '.')))
    else:
        return ("")


def get_additives_from_ingredients(ingredient_list):
    r1 = re.compile('E\s?\d{4}[a-f]?|E\s?\d{3}[a-f]?')
    r2 = re.compile('[INS]\s?\d{4}[a-f]?|[INS]\s?\d{3}[a-f]?')

    e_num_lst=[]

    for ingredient in ingredient_list[0]:
        additive_1= r1.findall(ingredient)
        additive_2 = r2.findall(ingredient)

        if additive_1:
            additive_1 = [re.sub('E ', 'E', additive) for additive in additive_1]
            e_num_lst.append(*additive_1)
        elif additive_2:
            additive_2=[re.sub('[INS]', 'E', additive) for additive in additive_2]
            e_num_lst.append(*additive_2)

    if e_num_lst:
        return e_num_lst
    else:
        return "None"


if __name__ == "__main__":

    list=[['Kair.Red Chilly Powder. Edible Oil,', 'INGREDIENTS:', 'lodized Salt,Mustard,&Ground Spices.',
           '(Asafoetida.CloveAcidity Regulator', 'Acetic Acid (INS260).Contains Permitted', 'Class lPreservative(INS211)',
           'NETWEIGHT:200q']]
    additive_info = get_additives_from_ingredients(list)
    print(additive_info)