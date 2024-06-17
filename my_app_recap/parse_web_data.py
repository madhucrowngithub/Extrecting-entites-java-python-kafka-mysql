from bs4 import BeautifulSoup

def print_content_text():
     with open('index.html', 'r') as f:
        contents = f.read()

        soup = BeautifulSoup(contents, "html.parser")
        all_tags = soup.find_all()
       
        for tag in all_tags:
            if tag.text.strip():  # Check if there is non-empty text content
                print(tag.text.strip())


def extract_text_from_html(html_content):
   
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all text from the BeautifulSoup object
    all_text = soup.get_text(separator='\n', strip=True)
    # Print all extracted text
    print(all_text)
    return all_text

# content_text()
