from bs4 import BeautifulSoup
import shutil
import os
import argparse

parser = argparse.ArgumentParser(description='A test program.')

parser.add_argument("--local", help="true | false(default): \t Makes requests for chattutor either to chattutor.org if false,\n or to localhost:5000 if true\n\tExamples:\n\t\t$ python3 ./book/chattutor_setup/install.py --local true\n\t\t$ python3 ./book/chattutor_setup/install.py", default="false")

args = parser.parse_args()

print(args.local)

content_path = "book/_build/html"
css_path = "book/_build/html/_static/styles/chattutor.style.css"
js_path = "book/_build/html/_static/scripts/chattutor.min.js" 
config_path = "book/_build/html/_static/scripts/chattutor.config.js" 

shutil.copyfile("book/chattutor_setup/chattutor.style.css", css_path)
shutil.copyfile("book/chattutor_setup/chattutor.config.js", config_path)
shutil.copyfile("book/chattutor_setup/chattutor.min.js", js_path)


def add_chattutor(dirpath, filename):
    file = os.path.join(dirpath, filename)
    with open(file, "r") as f:
        page_html = f.read()
        parsed_page_html = BeautifulSoup(page_html)
        main = parsed_page_html.find("main", {"id": "main-content"})
        if main == None: return
                
        
        parsed_page_html.html.body.append(parsed_page_html.new_tag("script", src=os.path.relpath(config_path, dirpath)))

        parsed_page_html.html.body.append(parsed_page_html.new_tag("script", src=os.path.relpath(js_path, dirpath), type="module"))
        
        parsed_page_html.html.head.append(parsed_page_html.new_tag("link",
            rel="stylesheet",
            type="text/css",
            href=os.path.relpath(css_path, dirpath)
        ))

    with open(file, "w") as f:
        f.write(str(parsed_page_html))

for dirpath, dirnames, filenames in os.walk(content_path):
    for file in filenames:
        if file.endswith(".html"): add_chattutor(dirpath, file)

