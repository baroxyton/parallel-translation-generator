import os
import epub_meta;
import subprocess;
import pathlib;
from bs4 import BeautifulSoup
import uuid
import re
def split_string_by_word_count(text, count):
    words = text.split()
    result = []
    temp = []
    open_tag = 0
    for word in words:
        open_tag += word.count('<') - word.count('>')
        temp.append(word)
        if len(temp) >= count and open_tag <= 0:
            result.append(" ".join(temp))
            temp = []
    if temp:
        result.append(" ".join(temp))
    return result

# Get book
book = input("Filename/path of the book (must be epub): ")
opf_content = str(epub_meta.get_epub_opf_xml(book)).split('<');

# Get HTML files of epub
html_files = [];
for item in opf_content:
    if item.startswith("item "):
        itemName = item.split('"')[1]
        if itemName.endswith("html") or itemName.endswith("xhtml"):
            html_files.append(itemName)
# Unzip epub and get OPF root directory
subprocess.call(["unzip", book, "-d", "unzippedBook"])
containerFile = open("./unzippedBook/META-INF/container.xml", "r")
containerData = str(containerFile.read()).split('<')
rootDir = ""
for element in containerData:
    if element.startswith("rootfile "):
        opfPath = element.split('"')[1]
        rootDir = os.path.dirname(opfPath)
print(rootDir)
# Give each paragraph an unique UUID
text_content = ""
progress=0
for htmlFile in html_files:
    print(f'HTML marking progress: {progress}/{len(html_files)}')
    rawContents = open("unzippedBook/" + rootDir + "/" + htmlFile, 'r').read()
    parsedContents = BeautifulSoup(rawContents, 'html.parser')
    for tag in parsedContents.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']):
        paragraphs = split_string_by_word_count(tag.decode_contents(), 50)
        tag_content = ""
        for paragraph in paragraphs:
            if len(paragraph) == 0:
                continue
            paragraph_uuid = str(uuid.uuid4())
            tag_content += f'[B TAG-UUID:{paragraph_uuid}]{paragraph}[E]<br><br>\n\n'
        new_contents = BeautifulSoup(tag_content, 'html.parser')
        tag.clear()
        tag.append(new_contents)
        text_content += tag.text.replace("\n", "\n\n")
    head = parsedContents.find("head");
    new_style = parsedContents.new_tag("style");
    new_style.string = "td{border: 1px solid black}"
    new_style["id"] = "translate-style";
    head.append(new_style);
    open("unzippedBook/" + rootDir + "/" + htmlFile, 'w').write(str(parsedContents))
    progress += 1
open("untranslatedMarked.txt", "w").write(text_content)
subprocess.call(["pandoc", "-s", "untranslatedMarked.txt", "-o", "untranslatedMarked.docx"])
print("A new file untranslatedMarked.docx has been created in the working directory. Please open translate.google.com and translate this document. Then download the translated version and enter the path to the downloaded version below.")
translated_docx = input("Path to downloaded version: ")
subprocess.call(["pandoc", "-s", translated_docx, "--to", "plain", "--wrap=none", "-o", "translated.txt"])
# Merge the two versions
translated_content = open("translated.txt", "r").read()
for htmlFile in html_files:
    rawContents = str(open("unzippedBook/" + rootDir + "/" + htmlFile, 'r').read())
    for match in re.findall(r'\[B TAG-UUID:(.*?)\](.*?)\[E\]', rawContents, flags=re.DOTALL):
        uuid = match[0]
        html_tag_content = match[1]
        txt_tag_regex = r'\[\s*B\s*T\s*A\s*G\s*\-\s*U\s*U\s*I\s*D\s*:\s*{}\s*\](.*?)\[\s*E\s*\]'.format(uuid)
        txt_tag_match = re.search(txt_tag_regex, translated_content, flags=re.DOTALL)
        if txt_tag_match:
            txt_tag_content = txt_tag_match.group(1)

            # Generate combination of original and translated content, inside of a table
            new_content = f'<table><tr><td>{html_tag_content}</td><td>{txt_tag_content}</td></tr></table>'
            print(new_content);
            html_tag_replacement = new_content
            print(txt_tag_content)

            # Replace tag with table 
            rawContents = rawContents.replace(f'[B TAG-UUID:{uuid}]'+html_tag_content+'[E]', html_tag_replacement)
            open("unzippedBook/" + rootDir + "/" + htmlFile, 'w').write(rawContents)
subprocess.call(["zip", "-r", "zippedBook.epub", "unzippedBook"])
fileFormat=input("What output format would you like? (eg. epub, pdf): ")
subprocess.call(["ebook-convert", "zippedBook.epub", f'finishedBook.{fileFormat}'])
