import json
import re
import keyboard
import time

# save facts base from inputted facts and ruleswhen generate is pressed 
def save_facts(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent = 2)

# load facts from the db.json
def load_facts(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def display_facts(existing_facts: dict):

    print("\nFacts from the database:")

    if existing_facts:
        sort_data = sorted(existing_facts.values())

        for facts in sort_data:
            print("[+] " + facts)
    else:
        print("No facts exist.\n")

# helper function to check if certain fact already exist
def is_existing_fact(str_fact: str, facts: dict) -> bool:
    # check if it is in the permanent facts
    for fact in facts.values():
        if str_fact == fact:
            return True
    
    return False
    
    
def is_rule_correct_format(rule):
    # Define a regular expression pattern for a valid rule
    pattern = r'If (.+?)(?: and (.+?))*? then (.+)'

    # Use re.match to check if the rule matches the pattern
    match_pattern = re.match(pattern, rule, re.IGNORECASE)

    if match_pattern:
        return True
    else:
        return False

# helper function to validate rule
def validate_rule(rule: str) -> str:
    # load existing facts in the database
    existing_facts: dict = load_facts('db.json')

    # holder of the extracted rule
    res = []

    # Define a regular expression pattern for a valid rule
    pattern = r'If (.+?)(?: and (.+?))*? then (.+)'

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
    
    if check_statement(res, existing_facts):
        return match_pattern.group(3)
    
    return ""

# generate the partial facts to the facts in the database
def generate_fact(latest_key: str, value: str, existing_facts: dict):
    if not existing_facts:
        existing_facts.update({"A": value})
    else: 
        existing_facts.update({generate_key(latest_key): value})

    # save fact base on rules
    save_facts('db.json', existing_facts)

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

if __name__ == '__main__':

    # holder of all inputted rules
    rules = []


    while True:
        # load existing facts in the database
        existing_facts: dict = load_facts('db.json')

        print("\n\tRULE BASED EXPERT SYSTEM USING FORWARD CHAINING REASONING METHOD")
        display_facts(existing_facts)

        if rules:
            print("\nInputted Rules:")
            for rule in rules:
                print("[/] " + rule)

        print("\nChoose below of what process you want me to do:\n[a] Input Facts\n[b] Input Rules \n[c] Generate \n[q] Exit")

        key_name = keyboard.read_event(suppress=True)
        response = key_name.name

        if response.lower() == 'a':
            str_fact = input("\nProvide me a fact: ")
            latest_key = ""

            for key in existing_facts.keys():
                latest_key = key

            if is_existing_fact(str_fact, existing_facts) or not str_fact:
                print("\nFact already existed or inputted fact is empty.\n")
            else:
                if not existing_facts:
                    generate_fact("A", str_fact, existing_facts)
                else: generate_fact(latest_key, str_fact, existing_facts)

            time.sleep(0.2)

        elif response.lower() == 'b':
            
            str_rule = input("\nProvide me a rule [Format: If (statement 1) then (statement 2).] or [Format: If (statement 1) and (statement 2) and ... then (statement n).]: ")
            
            if is_rule_correct_format(str_rule):
                rules.append(str_rule)
            else: 
                print("\nPlease follow the format I have provided!\n")

            time.sleep(0.2)

        elif response.lower() == 'c':
            if not rules:
                print("\nNothing to generate.\n")
                continue

            while True:
                existing_facts: dict = load_facts('db.json')
                is_fact_exist = False

                for item in rules:
                    fact = validate_rule(item)

                    if fact:
                        if is_existing_fact(fact, existing_facts):
                            continue

                        latest_key = ""

                        for key in existing_facts.keys():
                            latest_key = key

                        generate_fact(latest_key, fact, existing_facts)
                        is_fact_exist = True
                        rules.remove(item)

                if not is_fact_exist:
                    break

            rules.clear()
            time.sleep(0.2)

        elif response.lower() == 'q':
            print("\nThank you for your time. Your the best!\n")
            break

        else: 
            print("\nWrong key input!\n")
            time.sleep(0.2)
            continue
    