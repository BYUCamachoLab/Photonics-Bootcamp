from bs4 import BeautifulSoup
import shutil
import os

content_path = "../_build/html"
css_path = "../_build/html/_static/styles/chattutor.css"
js_path = "../_build/html/_static/scripts/chattutor.js" 

with open("./chattutor.html") as f:
    chattutor_html = f.read()
    parsed_chattutor_html = BeautifulSoup(chattutor_html)

def add_chattutor_html(dirpath, filename):
    file = os.path.join(dirpath, filename)
    with open(file, "r") as f:
        page_html = f.read()
        parsed_page_html = BeautifulSoup(page_html)
        main = parsed_page_html.find("main", {"id": "main-content"})
        if main == None: return
        main.append(BeautifulSoup(chattutor_html))
        parsed_page_html.html.body.append(parsed_page_html.new_tag("script", src=os.path.relpath(js_path, dirpath)))
        parsed_page_html.html.head.append(parsed_page_html.new_tag("link",
            rel="stylesheet",
            type="text/css",
            href=os.path.relpath(css_path, dirpath)
        ))

    with open(file, "w") as f:
        f.write(str(parsed_page_html))

for dirpath, dirnames, filenames in os.walk(content_path):
    for file in filenames:
        if file.endswith(".html"): add_chattutor_html(dirpath, file)

shutil.copyfile("./chattutor.css", css_path)
shutil.copyfile("./chattutor.js", js_path)