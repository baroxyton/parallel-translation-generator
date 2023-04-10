import sys
from bs4 import BeautifulSoup
import uuid

# get the file path from command line arguments
file_path = sys.argv[1]

# open the file and read its contents
with open(file_path, 'r') as f:
    content = f.read()

# parse the HTML using Beautiful Soup
soup = BeautifulSoup(content, 'html.parser')

# find all h1 and p tags
for tag in soup.find_all(['h1', 'p']):
    # generate a unique UUID
    uuid_str = str(uuid.uuid4())
    # add [B UUID-str] and [E] to the inner HTML
    tag.contents.insert(0, BeautifulSoup(f'[B TAG-UUID:{uuid_str}]', 'html.parser').contents[0])
    tag.contents.append(BeautifulSoup('[E]', 'html.parser').contents[0])
head = soup.find("head");
new_style = soup.new_tag("style");
new_style.string = "* {font-size: 1px !important; } img{display: none}"
new_style["id"] = "translate-style";
head.append(new_style);
# write the modified content back to the file
with open(file_path, 'w') as f:
    f.write(str(soup))

