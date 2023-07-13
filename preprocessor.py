from bs4 import BeautifulSoup
import tiktoken

# outputs the token length of a string according to the "cl100k_base" model
def tokenLength(input):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(input))

# cleans up all images and whitespace from an HTML, then outputs a list where each entry is a text paragraph
def extract_paragraphs_from_html(html_filepath):
    with open(html_filepath, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        paragraphs = []
        for paragraph in soup.find_all('p'):
            text = paragraph.get_text()
            if text.strip():  # Exclude empty paragraphs
                paragraphs.append(text)
        return paragraphs

# groups the paragraphs into tokens of length 256 or less
def grouper(paragraphs):
    output = []
    currentSegment = paragraphs[0]
    i = 1
    while i < len(paragraphs):
        nextSegment = paragraphs[i]
        if tokenLength(currentSegment + " " + nextSegment) <= 256:
            currentSegment = currentSegment + " " + nextSegment
        else:
            output.append(currentSegment)
            currentSegment = paragraphs[i]
        i += 1
    return output

# given a list of html filepaths, outputs a hashmap with filename: chunk_list as its key:value pairs
def chunker(html_filepaths_list):
    output = dict()
    for html_filepath in html_filepaths_list:
        filename = html_filepath.split("/")[-1][:-5]
        output[filename] = grouper(extract_paragraphs_from_html(html_filepath))
    return output

# testing
if __name__ == "__main__":
    ledger_filepath = "/Users/anthonyzhang/Development/square-hack-week/LedgerFAQ_goledgerfaq_.html"
    test_output = chunker([ledger_filepath])
    print(len(test_output))