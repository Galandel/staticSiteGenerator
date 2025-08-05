import shutil, os
from markdown_blocks import markdown_to_html_node
from functions import extract_title

def copy_files(src, dest):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Making directory: {dest_path}")
            os.mkdir(dest_path)
            copy_files(src_path, dest_path)
    # original code below prior to refactor:
    # print(f"Source directory: {src}")
    # print(f"Destination directory: {dest}")
    # src_dir = os.listdir(src)
    # for item in src_dir:
    #     if os.path.isfile(os.path.join(src,item)):
    #         print(f"Copying file: {os.path.join(src,item)}")
    #         shutil.copy(os.path.join(src,item), os.path.join(dest,item))
    #     else:
    #         print(f"Making directory: {os.path.join(dest, item)}")
    #         os.mkdir(os.path.join(dest,item))
    #         copy_files(os.path.join(src,item), os.path.join(dest,item))

def generate_page(from_path, template_path, dest_path):
    src = os.path.abspath(from_path)
    template = os.path.abspath(template_path)
    dest = os.path.abspath(dest_path)
    print(f"Generating page from {src} to {dest} using {template}")
    with open(src, 'r') as file:
        markdown = file.read()
    with open(template, 'r') as file:
        template_body = file.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    body = template_body.replace("{{ Title }}", title).replace("{{ Content }}", content)
    with open(dest, "w") as file:
        file.write(body)

def generate_pages_recursive(src, template, dest):
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)
        print(f"DEBUG: source: {src_item}; destination: {dest_item}")
        if os.path.isfile(src_item):
            print(f"Generating file for: {src_item}")
            dest_html_item = dest_item.replace('.md','.html')
            generate_page(src_item, template, dest_html_item)
        else: 
            print(f"Building directory and recursively calling function: {dest_item}")
            os.mkdir(dest_item)
            generate_pages_recursive(src_item, template, dest_item)

if __name__ == "__main__":
    src = os.path.abspath('static')
    dest = os.path.abspath('public')
    if os.path.exists(dest):
        if os.path.isdir(dest):
            print(f"Deleting destination directory: {dest}")
            shutil.rmtree(dest)
        else:
            raise Exception(f"Destination is not a directory: {dest}")
    print(f"Making destination directory: {dest}")
    os.mkdir(dest)
    copy_files(src, dest)
    content_path = os.path.abspath('content')
    generate_pages_recursive(content_path,'template.html', dest)


# Boots
# Thank you for sharing your complete file, apprentice! Here's some feedback and possible improvements:

# Strengths
# Your recursion is sound.
# Clearing out and recreating the destination works.
# Logging gives you good visibility into what is happening.
# Suggestions
# Robust Directory Creation

# Using os.mkdir is acceptable here because you’ve deleted the destination, so each dir is genuinely new.
# If someone ever reused this code in a different scenario, they would need to ensure the parent directories exist. os.makedirs(path, exist_ok=True) can be more robust for nested structures outside this assignment.
# Copying Logic

# Your logic copies files and recurses into directories—good!
# You could use os.path.join for all path building, which you already do.
# Edge Cases

# Your code ignores special file types (like symlinks), but for most static sites this won't be a problem.
# Code Clarity

# You could assign src_path = os.path.join(src, item) and dest_path = os.path.join(dest, item) at the top of the loop to avoid repetition.
# Refactor Example