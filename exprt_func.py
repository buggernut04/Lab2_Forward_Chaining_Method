import json
import re

# save facts base from inputted facts and ruleswhen generate is pressed 
def save_facts(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent = 2)

# load facts from the db.json
def load_facts(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# helper function to check if certain fact already exist
def is_existing_fact(str_fact: str, facts: dict) -> bool:
    # check if it is in the permanent facts
    for fact in facts.values():
        if str_fact == fact:
            return True
    
    return False
    
# helper function to check if certain rule is in correct format  
def is_rule_correct_format(rule):
   # Define a regular expression pattern for a valid rule
    pattern = r'If (.+?)(?: and (.+?))(?:,)? then (.+)'

    # Use re.match to check if the rule matches the pattern
    match_pattern = re.match(pattern, rule, re.IGNORECASE)

    if match_pattern:
        return True
    else:
        return False

# generate facts in the database
def generate_fact(latest_key: str, value: str, existing_facts: dict):
    existing_facts.update({generate_key(latest_key): value})
    # save fact base on rules
    save_facts('db.json', existing_facts)

# generate key to be putted in the database
def generate_key(latest_key: str) -> str:
    # Convert the string to a list of characters
    chars = list(latest_key)

    # Start from the rightmost character
    i = len(chars) - 1

    while i >= 0:
        if chars[i] == 'Z':
            chars[i] = 'A'
            i -= 1
        else:
            chars[i] = chr(ord(chars[i]) + 1)
            break

    # If we reach the leftmost character and it's 'A', insert 'A' at the beginning
    if i == -1 and chars[0] == 'A':
        chars.insert(0, 'A')

    # Convert the list of characters back to a string
    result = ''.join(chars)
    return result

# function to validate rule input and will return then statement
def validate_rule(rule: str) -> str:
   # load existing facts in the database
    existing_facts: dict = load_facts('db.json')

    # holder of the extracted rule
    res = []

    # Define a regular expression pattern for a valid rule
    pattern = r'If (.+?)(?: and (.+?))(?:,)? then (.+)'

    # Use re.match to check if the rule matches the pattern
    match_pattern = re.match(pattern, rule, re.IGNORECASE)
    
    # prcocess to check if statement is true or false
    res.append(match_pattern.group(1))
        
    # if 'and' statement occurs
    and_statements = re.findall(r'and (.+?)(?= and | then |$)', match_pattern.group(0))
    
    # to check if 'and' statement occurs 
    if and_statements:
        for statement in and_statements:
            res.append(statement)
    
    # get the last element of the string to check if comma is present
    last_string = res[len(res)  - 1]
    
    # validation
    if last_string[len(last_string) - 1] == ",":
        res[len(res) - 1] = last_string.replace(",", "") # remove comma
    
    if check_statement(res, existing_facts):
        return match_pattern.group(3)
    
    return ""
    
# check if the statement generate a true implication
def check_statement(rule_data: list, existing_facts: dict):
    
    # validator
    ctr = 0

    # check if all data in the rules is existed in the permanent fact data base
    for item in rule_data:
        for fact in existing_facts.values():
            if fact == item:
                ctr += 1
                break

    # if all statements existed then it will return true
    if ctr == len(rule_data):
        return True
    else: return False