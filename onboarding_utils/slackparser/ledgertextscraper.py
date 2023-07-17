import re

import tiktoken

def tokenLength(input):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(input))


def clean_text(text):
    # Remove names
    text = re.sub(r'^[a-zA-Z\s]+$', '', text, flags=re.MULTILINE)
    
    # Remove time stamps
    text = re.sub(r':\w+:\s+\d{1,2}:\d{2}\s+[APM]+', '', text, flags=re.MULTILINE)
    
    # Remove extra whitespace
    text = re.sub(r'\n{2,}', '\n', text)
    
    return text.strip()

def get_slack_data(file_name):
    """
    Scrapes slack data from a text file assuming the data was manually copied from the slack webapp
    """
    data = []

    # Open the text file
    with open(file_name, 'r') as file:
        # Read the contents of the file
        contents = file.read()

        # Clean the text
        cleaned_text = clean_text(contents)

        # Print the cleaned text   
        data = cleaned_text.split('\n')

    for i in range(len(data)):
        if tokenLength(data[i]) > 256:
            data[i] = "seller has multiple adjustments with no explanations , looks like he had 2 disputes on 6/15 (271.88 and 200.00), we took 116.96 on 6/20 for an adjustment when seller took a payment , then a transfer of 271.88 which im guessing is for the dipsute ,  on 6/22 seller transfers 60.00 bucks into this account, we then have adjuments for giving back the 116.96 then removing 176.96, taking the 60.00 , on 6/26 we have back the 176.96 then the seller transfer the funds out, on 7/3 we gave 400.00 , took 200.00 , then took 197.30 , on 7/10 we give back the 197.30 , take 400.00 leaving the account negative 202.70 , seller then takes 2 payments 193.90 and 237.29 with 146.80 going to savings, i ask for your help cause im trying to understand where the seller stands, he started out owing 471.88 ,"



    # for a in data:
    #     if ":chocobo-face:" in a or ":rolling_kirby:" in a or ":canary:" in a:
    #         print(a)

    for a in data:
        if ":chocobo-face:" in a or ":rolling_kirby:" in a or ":canary:" in a:
            data.remove(a)



    for a in data:
        if ("AM" in a or "PM" in a) and len(a) < 16:
            data.remove(a)



    newdata = []
    tempstr = ""

    for a in data:
        if len(tempstr + a) < 256:
            tempstr += a 
        else:
            newdata.append(tempstr)
            tempstr = ""

    return newdata
    # print(len(newdata))
    # # print(newdata)

    # sum = 0
    # for a in newdata:
    #     sum += len(a)

    # print(sum/740)

    # for a in range(10):
    #     print(a, newdata[a])

