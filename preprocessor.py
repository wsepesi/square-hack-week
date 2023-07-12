from bs4 import BeautifulSoup
import tiktoken

def tokenLength(input):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(input))

def extract_paragraphs_from_html(html_file):
    with open(html_file, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')
        paragraphs = []
        for paragraph in soup.find_all('p'):
            text = paragraph.get_text()
            if text.strip():  # Exclude empty paragraphs
                paragraphs.append(text)
        return paragraphs

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

if __name__ == "__main__":
    ledger_filepath = "/Users/anthonyzhang/Development/square-hack-week/LedgerFAQ_goledgerfaq_.html"
    paragraphs = extract_paragraphs_from_html("/Users/anthonyzhang/Development/square-hack-week/LedgerFAQ_goledgerfaq_.html")
    real_output = grouper(paragraphs)
    for i in range(10):
        print(tokenLength(real_output[i]), real_output[i])
        print()