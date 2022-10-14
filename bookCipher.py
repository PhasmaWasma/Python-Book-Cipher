import random
import secrets
import json

def stringSeparate(string: str) -> "list[str]":
    '''
    Takes a string and separates it into the 10 character length quanta for the
    code. Then adds all of the quanta to a list
    Parameters:
        string: a string of all the quanta to be separated
    Returns:
        quanta_list: a list of all the quanta
    '''
    quanta_list = []
    quanta_length = 10
    for i in range(0, len(string), quanta_length):
        quanta = string[i:i + quanta_length]
        quanta_list += [quanta]

    return quanta_list

def randomChunk(data_type: str, length: int) -> str:
    '''
    Randomly picks a character or characters from the given string representing
    the data type
    Parameters:
        data_type: a string of the characters representing the data type
        length: the length of the string to return
    Returns:
        chunk: a string
    '''
    chunk = ""
    type_offset = ord(data_type[-1]) - ord(data_type[0])

    for i in range(0, length):
        offset = random.randint(0, type_offset)
        char = data_type[offset]
        chunk += char
    return chunk

def randomQuanta(how_many: int, data_dict: dict) -> str:
    '''
    Generates a random quantum for however many are requested. They are not shuffled.
    Used only for testing
    Parameters:
        how_many: the number of quanta to generate
        data_dict: a dictionary of all the data types
    Returns:
        quanta_string: a string of all the quanta generated
    '''
    quanta_string = ""

    for i in range(0, how_many):
        direc = randomChunk(data_dict["direc"], 1)
        book = randomChunk(data_dict["book"], 1)
        page = randomChunk(data_dict["page"], 3)
        line = randomChunk(data_dict["line"], 2)
        char = randomChunk(data_dict["char"], 3)
        quanta_string += direction + book + page + line + char
    return quanta_string

def randomShuffledQuanta(how_many: int, data_dict: dict) -> str:
    '''
    Generates a random quantum for however many are requested. They are shuffled.
    Used only for testing
    Parameters:
        how_many: how many quanta to generate
        data_dict: a dictionary of all the data types
    Returns:
        quanta_string: a string of how_many random and shuffled quanta
    '''
    quanta_string = ""

    for i in range(0, how_many):
        quanta_list = []
        direc_random = randomChunk(data_dict["direc"], 1)
        book_random = randomChunk(data_dict["book"], 1)
        page_random = randomChunk(data_dict["page"], 3)
        line_random = randomChunk(data_dict["line"], 2)
        char_random = randomChunk(data_dict["char"], 3)

        quanta_list.append(direc_random)
        quanta_list.append(book_random)
        quanta_list.append(page_random[0])
        quanta_list.append(page_random[1])
        quanta_list.append(page_random[2])
        quanta_list.append(line_random[0])
        quanta_list.append(line_random[1])
        quanta_list.append(char_random[0])
        quanta_list.append(char_random[1])
        quanta_list.append(char_random[2])

        random.shuffle(quanta_list)

        for n in range(len(quanta_list)):
            quanta_string += str(quanta_list[n])

    return quanta_string

def quantaDirectionSort(quanta_list: "list[str]", data_dict: dict) -> "list[str]":
    '''
    Will correct the direction of a given quantum from a list. If that quantum does
    not have a left to right character, it will reverse the direction of the string
    Parameters:
        quanta_list: a list with an individual quantum at each index
        data_dict: a dictionary of all the data types
    Returns:
        quanta_list: a list of the direction corrected quanta
    '''
    pos_direc = data_dict["left_to_right"]
    for i in range(len(quanta_list)):
        list_of_direc_values = []
        for n in range(len(pos_direc)):
            sample_value = quanta_list[i].find(pos_direc[n])
            list_of_direc_values.append(sample_value)

        if list_of_direc_values.count(-1) == len(list_of_direc_values):
            quanta_list[i] = quanta_list[i][::-1]
        else:
            quanta_list[i] = quanta_list[i]
    return quanta_list

def quantaDataSort(quantum: str, dataset: str) -> str:
    '''
    Separates the individual data type in a direction corrected quantum and returns a string of that data type
    Parameters:
        quantum: an individual quantum string
        dataset: a string of all the characters for a given data type
    Returns:
        data_chunk: a string of the characters in the quantum of the requested data type
    '''
    data_list = []
    data_chunk = ""

    for i in range(len(dataset)):
        data_list += [dataset[i]]

    for n in range(len(quantum)):
        if quantum[n] in data_list:
            data_chunk += quantum[n]
    return data_chunk

def quantaSort(quanta: str, data_dict: dict) -> "dict[str]":
    '''
    Separates a direction corrected quantum into the four data types and returns
    a dictionary of those elements
    Parameters:
        quanta: a single quantum as a string
        data_dict: a dictionary of all the data types
    Returns:
        data_list: a list of the separated data types
    '''
    book = quantaDataSort(quanta, data_dict["book"])
    page = quantaDataSort(quanta, data_dict["page"])
    line = quantaDataSort(quanta, data_dict["line"])
    char = quantaDataSort(quanta, data_dict["char"])

    quantum_dict = {
    "book": book,
    "page": page,
    "line": line,
    "char": char
    }
    return quantum_dict

def dataSort(quanta_list: "list[str]", data_dict: dict) -> "list[str]":
    '''
    Sorts the data types from each quantum in a list of quanta and returns the sorted
    ones as a list
    Parameters:
        quanta_list: a list of quanta
        data_dict: a dictionary of all the data types
    Returns:
        quanta_list: a list of lists
    '''
    for i in range(len(quanta_list)):
        quanta_list[i] = quantaSort(quanta_list[i], data_dict)
    return quanta_list

def completeSort(quanta_string: str, data_dict: dict) -> "list[dict]":
    '''
    Takes a string of quanta and separates each one into its data types. Each quantum
    becomes a dictionary of its data types in a list. This list can then be decoded
    Parameters:
        quanta_string: a string of quanta
        data_dict: dictionary of all the data types
    Returns:
        sorted_list: a list of dictionaries
    '''
    sorted_quanta = stringSeparate(quanta_string)

    corrected_direc = quantaDirectionSort(sorted_quanta, data_dict)

    sorted_list = dataSort(corrected_direc, data_dict)

    return sorted_list

def sortCodedMessage(filename: str, data_dict: dict) -> "list[list[dict]]":
    '''
    Takes a txt file of ciphertext and separates each line into all of the
    data types for each quanta on the line and creates a list of the sorted dictionaries
    of its contents. Then all of the line lists are put into a final list, in order
    Parameters:
        filename: a string of the name of the file to be read
        data_dict: dictionary of all the data types
    Returns:
        message_list: a list of lists of dictionaries with the char data for each line in the file
    '''
    message_list = []
    input_file = open(filename, "r")
    line = input_file.readline()

    while line != "":
        stripped_line = line.strip()
        line_list = completeSort(stripped_line, data_dict)
        message_list.append(line_list)

        line = input_file.readline()
    input_file.close()

    return message_list

def charDecipher(char_dict: dict, code_key: "dict{dict}") -> dict:
    '''
    Uses the code key to take the coded character data and convert it back into integers
    representing the positional locations for the character.
    Parameters:
        char_dict: the coded character dict that has been sorted into its data types
        code_key: a dictionary containing the key to decode each data type
    Returns:
        new_char: the dictionary representing where the character is in its book
    '''
    new_char = {}
    for dict_key in char_dict:
        data = char_dict[dict_key]
        new_dict_entry = ""

        for char in data:
            letter = str(code_key[dict_key][char])
            new_dict_entry += letter

        new_char[dict_key] = int(new_dict_entry)

    return new_char

def listLengthChecker(list_to_test: list) -> int:
    '''
    If the list is odd numbered, it will add one to the int value of the length.
    If even it will return the list as is
    Parameters:
        list_to_test: the list that is being tested
    Returns:
        an int of the updated list length
    '''
    list_length = len(list_to_test)
    if len(list_to_test) % 2 != 0:
        list_length += 1

    return list_length

def binarySearchChecker(to_find: dict, sample_dict : dict) -> str:
    '''
    Helper fuction that checks to see if the sampling locations value is the same as what it's looking for.
    If the value is the same, it will return "0". If the value it's looking for is
    greater than the value found, it will return "+". If the value is lower than
    it's looking for, it will return "-".
    Parameters:
        to_find: the character dictionary that it is trying to find
        sample_dict: the test dictionary it is comparing
    Returns:
        a string that signifies if the two are the same or which direction it needs to look
        to find the dictionary
    '''
    find_page = to_find["page"]
    find_line = to_find["line"]
    find_char = to_find["char"]

    sample_page = sample_dict["page"]
    sample_line = sample_dict["line"]
    sample_char = sample_dict["char"]

    page = ""
    line = ""
    char = ""

    if sample_page == find_page:
        page += "0"
    elif sample_page < find_page:
        return "+"
    else:
        return "-"

    if sample_line == find_line:
        line += "0"
    elif sample_line < find_line:
        return "+"
    else:
        return "-"

    if sample_char == find_char:
        char += "0"
    elif sample_char < find_char:
        return "+"
    else:
        return "-"

    return char

def binarySearch(to_find: 'dict', looking_in: 'list[dict]') -> "dict | None":
    '''
    Looks for the given dictionary in the given list of dictionaries by using
    a binary search. If in the list, it returns the item. If not, it returns None
    Parameters:
        to_find: the dictionary to find
        looking_in: a list of dictionaries
    Returns:
        None if not in the list; the given dictionary if in the list
    '''

    list_length = listLengthChecker(looking_in)

    while list_length > 1:
        if len(looking_in) != list_length:
            list_length -= 1
        sample_location = int(list_length / 2)
        sample_dict = looking_in[sample_location]

        comparison_result = binarySearchChecker(to_find, sample_dict)
        if comparison_result == "0":
            return sample_dict
        elif comparison_result == "+":
            looking_in = looking_in[(sample_location + 1)::]
            list_length = len(looking_in)
        else:
            looking_in = looking_in[0: (sample_location):]
            list_length = len(looking_in)

    if len(looking_in) == 0:
        return None
    sample_dict = looking_in[0]
    comparison_result = binarySearchChecker(to_find, sample_dict)
    if comparison_result == "0":
        return sample_dict
    else:
        return None

def jsonFinderDecode(char_dict: dict, book_data: dict) -> int:
    '''
    Checks each character list in the dictionary until it finds the character associated
    with the given character data
    Parameters:
        char_dict: the character dictionary to look for
        book_data: the dictionary of all the character data for the given book
    Returns:
        the character string that is the key for the dictionary with the given dictionary
        None if it cannot be found in the book
    '''
    for i in book_data:
        is_in = binarySearch(char_dict, book_data[i])
        if is_in != None:
            return i

    return None

def charDecode(char_dict: dict, code_key: dict, book_data: dict) ->  str:
    '''
    Removes the book data in the character dictionary and looks inside of that
    books dictionary to find the character associated with the given character dictionary
    Parameters:
        char_dict: a dictionary containing the location and book data for the character
        code_key: a dictionary containing the key to decode each data type
        book_data: the dictionary of all the character data in the book its looking in
    Returns:
        a string of the character it found or None if it could not be found
    '''
    book_id = char_dict.pop("book")
    char_dict.update()
    #book_title = code_key["book"][book_id]

    key = jsonFinderDecode(char_dict, book_data)
    return key

def decodeMessage(message_char_data: "list[list[dict]]", code_key: "dict{dict}", book_title: str) -> list:
    '''
    Decodes the given lists of character data into the characters they represent and
    gives back the list with the character dictionaries replaced with their strings
    Parameters:
        message_char_data: a list of lists of character data dictionaries
        code_key: a dictionary containing the key to decode each data type
        books_dict: the dictionary containing the names of each book title being used
    Returns:
        a list of lists of individual character strings
    '''

    with open(f"{book_title}.json", "r") as read_file:
        book_data = json.load(read_file)

        for line in range(len(message_char_data)):
            for char in range(len(message_char_data[line])):
                char_dict = message_char_data[line][char]
                char_dict = charDecipher(char_dict, code_key)
                new_letter = charDecode(char_dict, code_key, book_data)
                message_char_data[line][char] = new_letter
        read_file.close()

    return message_char_data

def sortOutgoingMessage(filename: str) -> "list[list[str]]":
    '''
    Reads each line of the given plaintext txt file and converts it into a list of the characters
    on the line. Then it puts each of the lists of each line into one larger list
    Parameters:
        filename: the name of the txt file to be read
    Returns:
        a list of list of strings
    '''
    input_file = open(filename, "r")
    line = input_file.readline()
    message_list = []

    while line != "":
        line_list = []
        stripped_line = line.strip()
        for i in range(len(stripped_line)):
            char = stripped_line[i]
            line_list.append(char)

        message_list.append(line_list)

        line = input_file.readline()
    input_file.close()
    return message_list

def jsonFinderEncode(char: str, book_data: dict) -> dict:
    '''
    Takes the given character and book dictionary and randomly picks a dictionary
    from it to use for the character. If there is an error with single parentheses,
    it converts it into the type found in pdfs to see if that will work instead.
    Parameters:
        char: a string of a character
        book_data: a dictionary of lists of dictionaries of each character in the book
    Returns:
        a dictionary of the character location data
    '''
    try:
        char_options = book_data[char]
        index = secrets.randbelow(len(char_options))
        char_dict = char_options[index]
        char_dict.update({"book": 1})
    except:
        if   char == "'":
             char = '’'
             char_options = book_data[char]
             index = secrets.randbelow(len(char_options))
             char_dict = char_options[index]
             char_dict.update({"book": 1})

    return char_dict

def keyFlipper(code_key: dict) -> "dict{list}":
    '''
    Takes a dictionary that has the characters as a key and turns it into a dictionary
    where the numbers the characters represent are the key. When the key is used,
    it will return a list of the characters that have that value
    Parameters:
        code_key: a dictionary containing the key to decode each data type
    Returns:
        an inverted dictionary where the values of the original are the new keys
        and the old keys are the new values
    '''
    reversed_dict = {}
    for i in code_key:
        new_key = code_key.get(i)
        does_exist = reversed_dict.get(new_key)
        if  does_exist == None:
            reversed_dict.update({new_key: [i]})
        else:
            new_key_list = reversed_dict.get(new_key)
            new_key_list.append(i)
            reversed_dict[new_key] = new_key_list

    return reversed_dict

def charDictEncoder(char_dict: dict, reversed_code_key: "dict{dict}") -> "list[list[str]]":
    '''
    Takes a character dictionary and encodes the location data using the cipher,
    then returns it as a list. Does not include the directional component yet
    Parameters:
        char_dict: a plaintext dictionary of the location data for the character
        reversed_code_key: a dictionary containing the key to decode each data type that is inverted
                           with keyFlipper
    Returns:
        a list of all the ciphertext characters, which are in their own lists
    '''
    #need to give the char dict a book value when extracting it from a book before putting it here
    #needs to NOT have the directional components yet as well
    encoded_list = []
    for i in char_dict:
        data_location = str(char_dict[i])

        if i == "page" and len(data_location) == 2:
            data_location = "0" + data_location
        elif i == "page" and len(data_location) == 1:
            data_location = "00" + data_location

        if i == "line" and len(data_location) == 1:
            data_location = "0" + data_location

        if i == "char" and len(data_location) == 2:
            data_location = "0" + data_location
        elif i == "char" and len(data_location) == 1:
            data_location = "00" + data_location


        data_list = []
        for n in range(0, len(data_location)):
            location_num = int(data_location[n])
            new_num_str  = secrets.choice(reversed_code_key[i][location_num])
            data_list.append(new_num_str)

        encoded_list.append(data_list)

    return encoded_list

def charEncipher(encoded_list: "list[list[str]]", data_dict: "dict{str | list}") -> str:
    '''
    Takes the character location data list and adds a directional component, ranndomly
    deciding whether to reverse the direction or not. Then it takes the list and
    converts it into a single string quantum.
    Parameters:
        encoded_list: a list of ciphertext characters, which are in their own lists
        data_dict: a dictionary containing a string with each character in a data type
    Returns:
        a single quantum in a string
    '''
    direction = secrets.randbelow(len(data_dict["direc"]))
    direction = data_dict["direc"][direction]
    encoded_list.append([direction])

    if direction not in data_dict["left_to_right"]:
        for n in range(0, len(encoded_list)):
            encoded_list[n].reverse()

    encoded_char_quantum = ""
    for i in range(0, 10): #each quanta is 10 chars long
        item = secrets.choice(encoded_list)
        item_index = encoded_list.index(item)

        if len(item) == 1:
            encoded_char_quantum += encoded_list[item_index][0]
            encoded_list.pop(item_index)
        else:
            encoded_char_quantum += encoded_list[item_index][0]
            encoded_list[item_index].pop(0)

    return encoded_char_quantum

def messageEncipher(filename: str, code_key: "dict{dict}", books_dict: dict) -> None:
    '''
    Reads the given text file and concerts it into ciphertext (quanta), then rewrites the file
    in ciphertext
    Parameters:
        filename: the name of the txt file to be read, with the .txt
        code_key: a dictionary containing the key to decode each data type
    Returns:
        a ciphertext txt file containing the given message
    '''
    reversed_code_key = {
    "book": keyFlipper(code_key["book"]),
    "page": keyFlipper(code_key["page"]),
    "line": keyFlipper(code_key["line"]),
    "char": keyFlipper(code_key["char"])
    }

    data_dict = keyToDataDict(code_key)

    message_plaintext = sortOutgoingMessage(filename)

    book_title = books_dict[1]

    with open(f"{book_title}.json", "r") as read_file:
        book_data = json.load(read_file)

        with open(filename, "w") as outgoing_txt:

            for i in range(0, len(message_plaintext)):
                line_string = ""
                for n in range(0, len(message_plaintext[i])):
                    new_char = jsonFinderEncode(message_plaintext[i][n], book_data)
                    new_quantum = charEncipher(charDictEncoder(new_char, reversed_code_key), data_dict)
                    line_string += new_quantum

                outgoing_txt.write(line_string + '\n')

            outgoing_txt.close()

    print("Message encrypted")

def messageDecipher(filename: str, code_key: "dict{dict}", books_dict: dict) -> None:
    '''
    Takes a given ciphertext messgae and converts it into plaintext if the code_key
    is the same it was enciphered with
    Parameters:
        filename: the name of the txt file as a string
        code_key: a dictionary containing the key to decode each data type
    Returns:
        a ciphertext txt file containing the given message
    '''
    book_title = books_dict[1]

    data_dict = keyToDataDict(code_key)

    message_char_list = sortCodedMessage(filename, data_dict)
    message_char_list = decodeMessage(message_char_list, code_key, book_title)

    with open(filename, "w") as outgoing_txt:

        for i in range(0, len(message_char_list)):
            line_string = ""
            for n in range(0, len(message_char_list[i])):
                line_string += message_char_list[i][n]

            outgoing_txt.write(line_string + '\n')

        outgoing_txt.close()

    print("Message decrypted")

def keyGenerator(filename: str, string_of_chars: str, key_params: "dict[dict]") -> "dict[dict]":
    '''
    Takes the given string of characters and creates a random code key using characters
    in the string and the given parameters dictionary. It will create a code within the
    parameters given
    Parameters:
        filename: the name of the JSON file that will be exported as a string, do not include .json at the end
        string_of_chars: a string of all of the characters you want to use for the code
        key_params: a dictionary containing a dictionary of each range of how many items can be included in the code
    Returns:
        code_key: a dictionary containing the key to decode each data type
    '''
    chars_list = []
    for i in range(len(string_of_chars)):
        chars_list.append(string_of_chars[i])

    code_key_chars = {
    "book": [],
    "page": [],
    "line": [],
    "char": [],
    "direc": [],
    "left_to_right": []
    }
    remaining_params = {}
    for data_type in key_params:
        remaining_params[data_type] = key_params[data_type]["max"] - key_params[data_type]["min"]
        for n in range(0, key_params[data_type]["min"]):
            if data_type == "left_to_right":
                pass
            else:
                char_int = random.randint(0, len(chars_list) - 1)
                code_key_chars[data_type].append(chars_list[char_int])
                chars_list.pop(char_int)

    for data_type in remaining_params:
        remaining_char_amount = random.randint(0, remaining_params[data_type])
        if remaining_char_amount == 0:
            pass
        elif data_type == "left_to_right":
            pass
        else:
            for i in range(0, remaining_char_amount):
                char_int = random.randint(0, len(chars_list) - 1)
                code_key_chars[data_type].append(chars_list[char_int])
                chars_list.pop(char_int)

    new_code_key = {
    "book": {},
    "page": {},
    "line": {},
    "char": {},
    "direc": {},
    "left_to_right": []}
    for data_type in code_key_chars:
        if data_type == "direc":
            new_code_key["direc"] = code_key_chars["direc"]
        elif data_type == "left_to_right":
            item_count = key_params["left_to_right"]["min"] + random.randint(0, remaining_params["left_to_right"])
            direction_chars = code_key_chars["direc"].copy()
            for n in range(0, item_count):
                new_code_key[data_type].append(direction_chars[n])
        elif data_type != "book":
            list_of_chars = code_key_chars[data_type].copy()
            for n in range(0, 10):
                new_code_key[data_type].update({list_of_chars[0]: n})
                list_of_chars.pop(0)

            for i in range(0, len(list_of_chars)):
                char_int = random.randint(0, 9)
                new_code_key[data_type].update({list_of_chars[i]: char_int})
        else:
            for n in range(0, len(code_key_chars[data_type])):
                new_code_key[data_type].update({code_key_chars[data_type][n]: n})

    with open(f"{filename}.json", "w") as write_file:
        json.dump(new_code_key, write_file, ensure_ascii = False)
        write_file.close()

    print("New code key created and exported as JSON")

def keyToDataDict(code_key: "dict[dict]") -> "dict[string | list]":
    '''
    Takes a given code key and converts it into the data type dictionary format the quanta sorters use
    Parameters:
        code_key: a dictionary containing the key to decode each data type
    Returns:
        a dictionary of strings and one list
    '''
    data_dict = {}
    for data_type in code_key:
        if  data_type == "left_to_right":
            data_dict[data_type] = code_key[data_type]
        else:
            string_of_chars = ""
            for key in code_key[data_type]:
                string_of_chars += key

            data_dict[data_type] = string_of_chars

    return data_dict

################################################################################
def main():

    ##### Key generation #####
    key_name = "key_1"

    string_of_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZαβγδεζηθικλμνξοπρςστυφχψω#$%&!?"
    # This is all of the characters that will be used for the code. It should work
    # with any unicode characters. Just make sure that the total max parameters do
    # not exceed the length of the string

    key_params = {
    "book" : {"min": 3,  "max": 3},
    "page" : {"min": 15, "max": 30},
    "line" : {"min": 15, "max": 30},
    "char" : {"min": 15, "max": 30},
    "direc": {"min": 4,  "max": 5},       #all of the direction characters
    "left_to_right": {"min": 2, "max": 3}
    }
    # These are the parameters used when generating a new key for the code
    # It will randomly pick a value to use for each category between the max
    # and min values (inclusive). left_to_right determines how many of the direction
    # characters represent reading it left to right. Should be lower than the total
    # number of direction characters

    #keyGenerator(key_name, string_of_chars, key_params)
    # Only need to use the key generator function when you want to create a new key

    ############################################################################

    books_dict = {1: ""} #only uses the first book here for now (no file ending, just the name of the file)
    code_key = "code_key.json"

    with open(f"{code_key}", "r") as read_file:
        code_key = json.load(read_file)

    #comment these in/out depending on which you want to use

    #messageEncipher("secret_message.txt", code_key, books_dict)
    #messageDecipher("secret_message.txt", code_key, books_dict)

    #read_file.close()


if __name__ == "__main__":
    main()
