import sys
import re

# get the file paths from command line arguments
html_file_path = sys.argv[1]
txt_file_path = sys.argv[2]

# read the contents of the TXT file
with open(txt_file_path, 'r') as f:
    txt_content = f.read()
    # Remove google watermarks
    txt_content = txt_content.replace("Machine Translated by Google", "");
# find all [B TAG-UUID:{uuid}] tags in the HTML file
with open(html_file_path, 'r') as f:
    html_content = f.read()
    # Remove translation style, add style to tables
    html_content = html_content.replace("* {font-size: 1px !important; } img{display: none}", "td{border: 1px solid black}");
    for match in re.findall(r'\[B TAG-UUID:(.*?)\](.*?)\[E\]', html_content, flags=re.DOTALL):
        print(match[0]);
        uuid = match[0]
        html_tag_content = match[1]
        
        # find the corresponding [B] tag in the TXT file
        txt_tag_regex = r'\[\s*B\s*T\s*A\s*G\s*\-\s*U\s*U\s*I\s*D\s*:\s*{}\s*\](.*?)\[\s*E\s*\]'.format(uuid)
        txt_tag_match = re.search(txt_tag_regex, txt_content, flags=re.DOTALL)
        if txt_tag_match:
            txt_tag_content = txt_tag_match.group(1)

            # Generate combination of original and translated content, inside of a table
            new_content = f'<table><tr><td>{html_tag_content}</td><td>{txt_tag_content}</td></tr></table>'
            print(new_content);
            html_tag_replacement = new_content
            print(txt_tag_content)

            # Replace tag with table 
            html_content = html_content.replace(f'[B TAG-UUID:{uuid}]'+html_tag_content+'[E]', html_tag_replacement)

# write the modified content back to the HTML file
with open(html_file_path, 'w') as f:
    f.write(html_content)


