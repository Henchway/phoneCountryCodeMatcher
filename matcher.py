import json

number = "+431234123412341234"
with open("data.json", "r") as file:
    data = file.read()

codes = json.loads(str(data))


def match(input_number, country_codes, current_slice=5) -> tuple:
    """ Returns the number (without prefix) and the matched country"""
    input_number = input_number.replace(" ", "")
    if current_slice == 0:
        return None
    part = input_number[0:current_slice]
    if part in country_codes.keys():
        return input_number[len(part):], country_codes[part]
    return match(input_number, country_codes=country_codes, current_slice=current_slice - 1)


actual_match = match(input_number=number, country_codes=codes)
print(actual_match)
