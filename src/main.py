from markdownblocks import markdown_to_html_node
import os
import shutil
from pathlib import Path



def extract_title(markdown):
    title = ""
    for line in markdown.split("\n"):
        if line[:2] == "# ":
            title = line[2:]
            break
        raise Exception("No title found!")
    return title

def copy_directory(src_dir, dest_dir):
    
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    files = os.listdir(src_dir)
    for file in files:
        if os.path.isfile(os.path.join(src_dir, file)):
            shutil.copy(os.path.join(src_dir, file), os.path.join(dest_dir, file))
        else:
            copy_directory(os.path.join(src_dir, file), os.path.join(dest_dir, file))

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    Path(dest_dir_path).mkdir(parents=True, exist_ok=True)

    files = os.listdir(dir_path_content)
    for file in files:
        full_path = os.path.join(dir_path_content, file)
        if os.path.isfile(full_path):
            # Handle markdown files here
            if file.endswith(".md"):
                generate_page(full_path, template_path, os.path.join(dest_dir_path, file[:-3] + ".html"))
        elif os.path.isdir(full_path):
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))
                
        

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise ValueError(f"Path doesn't exist: {from_path}")
    if not os.path.exists(template_path):
        raise ValueError(f"Path doesn't exist: {template_path}")
    
    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dir_to_create = os.path.dirname(dest_path)
    os.makedirs(dir_to_create, exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(template)

    

def main():
    copy_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    

if __name__ == "__main__":
    main()