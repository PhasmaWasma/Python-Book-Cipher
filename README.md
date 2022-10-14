# Python Book Cipher 

Use PDFs to encipher text in a txt file

This uses the [pdfplumber](https://github.com/jsvine/pdfplumber) module to read a given PDF to collect character data.

This project is likely not cryptographically secure so do not use it for any actual information you need to keep private. It does use the Python secrets module, but that does not mean the entire thing is secure.


### To Use

This project has two main parts: the PDF scraping and the enciphering.

#### pdfScraper.py
pdfScraper.py will take the given PDF and collect all of the character data (which character it is, the page its one, the line on the page, and the index in the line) and exports a JSON file of all of that sorted information. To use, you put the name of the PDF as a string into the pdf_name variable with the .pdf still at the end. Or if you import the file, you need to call the `bookCharData` fucntion with the PDF name as the parameter. It will automatically export the JSON with the same name as the PDF. These JSONs are crucial for the encipher/deciphering

#### bookCipher.py
Inside of bookCipher.py there are three important fucntions: `keyGenerator`, `messageEncipher`, and `messageDecipher`.

The `keyGenerator` fucntion allows you to randomly generate keys for the cipher with a few parameters. It requires three things to work: the name you want the key JSON to have (no file ending required), a large string of any Unicode characters you want to be included in the code, and the `key_params` dictionary which you can modify to have as many characters in each as you wish. The `key_params` randomly select a number between the min and max values given for the code. You need more than 10 characters at least for the page, line, and char values. **You need at least one key to be able to use the following fucntions.**

The `messageEncipher` function allows you to encode a txt file with the substitution cipher format this uses. It needs the name of the txt (with the file ending) as a string, the opened `code_key` JSON file, and a dictionary with the names of the PDF/JSON file as a string (no file ending). 

The `messageDecipher` fucntion takes the same parameters as `messageEncipher`, but takes the enciphered file and allows you to decode it

Both the encipher and decipher fucntions currently overwrite the file that is given to them

### WIP Functionality

Currently the `messageEncipher` and `messageDecipher` functions take a dictionary of all the book names you want to use for the enciphering. Eventually, I intend for this to be able to use multiple book sources at once, and this dictionary is planning for that

I also intend to change the way that the character data is stored in the JSON files to make the files much smaller. Smaller files would allow for the multiple PDF sources to be used with less memory. Right now the individual data for each character is in a dictionary. I plan to convert to using tuples, which should help quite a bit, but a lot needs to be changed internally to make that happen

I might also make it so that the file is not overwritten so that you can have a copy of what you encoded if need be
