from textnode import TextNode, TextType
from htmlnode import *
from inline_markdown import *
from block_markdown import *
import os
import shutil
import sys

def copy_from(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(f"Copied file from {src_path} to {dest_path}")
        elif os.path.isdir(src_path):
            copy_from(src_path, dest_path)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
        
    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    actual_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    actual_html = actual_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(actual_html)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        
        if os.path.isdir(content_path):
            generate_pages_recursive(content_path, template_path, dest_path, basepath)
        elif os.path.isfile(content_path) and content_path.endswith(".md"):
            dest_html_path = os.path.splitext(dest_path)[0] + ".html"
            os.makedirs(os.path.dirname(dest_html_path), exist_ok=True)
            generate_page(content_path, template_path, dest_html_path, basepath)
        
        
def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_from("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
if __name__ == "__main__":
    main()