import pdfplumber
import json

################################################################################
def pageScraper(pdf: list, page: int) -> bool:
    '''
    Takes the given page of a pdf and determines if the page has characters on it.
    If so, it returns True. Otherwise it returns False. It also creates a text file
    of all of the characters that are on the page
    Parameters:
        pdf:  the pdfplumber class for the given book
        page: an int that represents the page number
    Returns:
        bool
    '''
    output_file = open("page_scrape.txt", "w")

    '''
    with pdfplumber.open(pdf_name) as pdf:
    '''
    page_data  = pdf.pages[page]
    page_chars = page_data.chars

    if len(page_chars) == 0:
        return False

    char_num = 0
    initial_dist = page_chars[0]["top"]
    while char_num < len(page_chars):
        char = page_chars[char_num]["text"]
        dist_from_page_top = page_chars[char_num]["top"]

        if initial_dist < dist_from_page_top:
            output_file.write("\n")
            output_file.write(f"{char}")
        else:
            output_file.write(f"{char}")

        initial_dist = dist_from_page_top
        char_num += 1

    output_file.close()
    return True

def pageSort(page: int) -> dict:
    '''
    Creates a location dictionary for each character on the page that tells which
    page of the book it is on, which line on the page it is on, and which character
    in the line it is on
    Parameters:
        page: an int representing the page number of the book
    Returns:
        a dictionary of all of the character data dictionaries on the page, sorted by
        character
    '''
    input_file = open("page_scrape.txt", "r")

    line_num = 0
    page_info = {}

    line = input_file.readline()
    while line != "":
        line_string = line.strip()
        for i in range(len(line_string)):
            char = line_string[i]
            char_info = {
            "page": page,
            "line": line_num,
            "char": i   }

            if char in page_info:
                page_info[char].append(char_info)
            elif char == "“" or char == "”" or char == '"':
                page_info['"'] = [char_info]
            elif char == "’":
                page_info["'"] = [char_info]
            else:
                page_info[char] = [char_info]

        line = input_file.readline()
        line_num += 1

    line = input_file.close()
    return page_info

def bookScraper(pdf_name: str) -> "dict{list}":
    '''
    Takes the given pdf filename and creates a dictionary of the locations of every single
    character in the file, where each key of the dictionary is the character. Each key
    has a list of location data dictionaries inside
    Parameters:
        pdf_name: the name of the pdf to be read as a string with .pdf still at the end
    Returns:
        a dictionary of all the characters in the file and their locations
    '''
    with pdfplumber.open(pdf_name) as pdf:

        if pageScraper(pdf, 0) == True:
            book_info = pageSort(0)
        else:
            book_info = {}

        print(f"Page 0 of {len(pdf.pages) - 1} scraped and sorted")

        for i in range(1, len(pdf.pages)):
            page_have_chars = pageScraper(pdf, i)
            page_info = pageSort(i)

            if page_have_chars == True:
                for page_key in list(page_info.keys()):
                    if page_key in list(book_info.keys()):
                        new_list = book_info[page_key]
                        for n in range(len(page_info[page_key])):
                            new_list.append(page_info[page_key][n])
                        new_dict = {page_key: new_list}
                        book_info.update(new_dict)
                    else:
                        new_dict = {page_key: page_info[page_key]}
                        book_info.update(new_dict)

            print(f"Page {i} of {len(pdf.pages) - 1} scraped and sorted")

    return book_info

def bookDataToJSON(book_data: dict, filename: str) -> None:
    '''
    Exports the given dictionary to a JSON file
    Parameters:
        book_data: a dictionary of all the characters in the file and their locations
        filename: the name of the pdf file that was read
    Returns:
        None
    '''
    filename = filename[0:-4:]

    with open(f"{filename}.json", "w") as write_file:
        json.dump(book_data, write_file, ensure_ascii = False, separators=(',', ':'))

def bookCharData(pdf_name: str) -> None:
    '''
    Scrapes all of the character data in a given pdf and exports the resulting
    dictionary as a JSON file
    Parameters:
        pdf_name: the filename of the pdf with .pdf still at the end
    Returns:
        None
    '''
    book_data = bookScraper(pdf_name)
    bookDataToJSON(book_data, pdf_name)
    print("JSON completed")
################################################################################
def main():
    # just put the name of whatever pdf you want to scrape here
    pdf_name = ""
    bookCharData(pdf_name)

if __name__ == "__main__":
    main()
