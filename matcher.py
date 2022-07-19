import json

number = "+11234123412341234"
country = "AT"
with open("data.json", "r") as file:
    data = file.read()

codes = json.loads(str(data))[0]


def match(input_number, country_codes, country, current_slice=5):
    """ Returns the number (without prefix) and the matched country"""
    if input_number is None:
        return None, None
    input_number = input_number.replace(" ", "").replace("-", "")
    if current_slice == 0:
        return None, None
    part = input_number[0:current_slice]
    if part in country_codes.keys():
        country_code = [x['ID'] for x in country_codes[part] if x['2dig'] == country]
        if len(country_code) == 0 and len(country_codes[part]) != 0:
            country_code = [x['ID'] for x in country_codes[part]]
        if country_code:
            return input_number[len(part):], country_code.pop(0)
        else:
            return None, None
    return match(input_number, country_codes=country_codes, current_slice=current_slice - 1, country=country)


actual_match = match(input_number=number, country_codes=codes, country=country)
print(actual_match)
