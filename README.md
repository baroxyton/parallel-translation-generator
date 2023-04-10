# Parallel text generator
Given a .epub file, you can use this project to generate a parallel translation
## Prequesiteries: 
- Linux environment (native, WSL, ...)
- Bash shell
- .epub file
- Installed commands: pdf2txt, zip/unzip, ebook-convert, python
## Step 1: prepare directory
Create a new directory using `mkdir`. In this directory, copy your .epub book and `git clone` this repo into the newly created directory.

Next, unzip the book like this: `unzip [epubfile.epub] -d unzippedBook`
## Step 2: add taggings to the book
Create a new copy of the unzippedBook directory: `cp -r unzippedBook taggedBook`

Then run the following command: `for i in taggedBook/OEBPS/Text/*.html; do python parallel-translation-generator/add_taggings.py $i; done;`

Lastly, convert the tagged book back into .epub with the command: `zip -r taggedBook.epub taggedBook/`. Note that this epub is corrupt, however calibre can handle it perfectly fine.
## Step 3: translate the book
Convert the corrupt .epub to a .pdf using the following command: `ebook-convert taggedBook.epub taggedBook.pdf --disable-font-rescaling`. View the pdf to make sure everything is fine. If the font is small, it works as intended; however if the text is overlaid or otherwise unreadable, it is necessary to go back to step 2 and delete the styles in OEBPS/Styles.

Open the site https://translate.google.com in your webbrowser. Use the 'document' option to translate the newly generated .pdf version to your desired language and download the result.

Extract and save the translated text using the command `pdf2txt /path/to/translatedbook.pdf > translated.txt`
## Step 4: merge the two versions
Create a new copy of the directory: `cp -r taggedBook mergedBook`.

Then run the following command: `for i in mergedBook/OEBPS/Text/*.html; do python parallel-translation-generator/merge.py $i translated.txt; done;`

Lastly, generate the result pdf with the following commands:
```
zip -r mergedBook.epub mergedBook
ebook-convert mergedBook.epub mergedBook.pdf
```
