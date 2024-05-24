import re
import pandas as pd


def get_data(res):

    data = {
        "company_name": [],
        "card_holder": [],
        "designation": [],
        "mobile_number": [],
        "email": [],
        "website": [],
        "area": [],
        "city": [],
        "state": [],
        "pin_code": [],
    }
    city = ""  # Initialize the city variable
    for ind, i in enumerate(res):
        # To get WEBSITE_URL
        if "www " in i.lower() or "www." in i.lower() or "www" in i.lower():
            data["website"].append(i)
        elif "WWW" in i:
            data["website"].append(res[ind - 1] + "." + res[ind])
        # To get email ID
        elif "@" in i:
            data["email"].append(i)
        # To get MOBILE NUMBER
        elif "-" in i:
            data["mobile_number"].append(i)
            if len(data["mobile_number"]) == 2:
                data["mobile_number"] = " & ".join(data["mobile_number"])
        # To get COMPANY NAME
        elif ind == len(res) - 1:
            data["company_name"].append(i)
        # To get CARD HOLDER NAME
        elif ind == 0:
            data["card_holder"].append(i)
        # To get designation
        elif ind == 1:
            data["designation"].append(i)
        # To get AREA
        if re.findall("^[0-9].+, [a-zA-Z]+", i):
            data["area"].append(i.split(",")[0])
        elif re.findall("[0-9] [a-zA-Z]+", i):
            data["area"].append(i)
        # To get CITY NAME
        match1 = re.findall(".+St , ([a-zA-Z]+).+", i)
        match2 = re.findall(".+St,, ([a-zA-Z]+).+", i)
        match3 = re.findall("^[E].*", i)
        if match1:
            city = match1[0]  # Assign the matched city value
        elif match2:
            city = match2[0]  # Assign the matched city value
        elif match3:
            city = match3[0]  # Assign the matched city valu
        # To get STATE
        state_match = re.findall("[a-zA-Z]{9} +[0-9]", i)
        if state_match:
            data["state"].append(i[:9])
        elif re.findall("^[0-9].+, ([a-zA-Z]+);", i):
            data["state"].append(i.split()[-1])
        if len(data["state"]) == 2:
            data["state"].pop(0)
        # To get PINCODE
        if len(i) >= 6 and i.isdigit():
            data["pin_code"].append(i)
        elif re.findall("[a-zA-Z]{9} +[0-9]", i):
            data["pin_code"].append(i[10:])
    data["city"].append(city)  # Append the city value to the 'city' array

    return data
