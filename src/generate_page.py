import os
from block_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as content:
        markdown_content = content.read()

    with open(template_path) as template:
        template_content = template.read()

    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    dest_dir = os.path.dirname(dest_path)
    
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    items = os.listdir(dir_path_content)

    for item in items:
        from_path = os.path.join(dir_path_content, item)

        if os.path.isfile(from_path):
            if item.endswith(".md"):
                dest_file_name = item.replace(".md", ".html")
                dest_path = os.path.join(dest_dir_path, dest_file_name)

                generate_page(from_path, template_path, dest_path)
        
        else:
            new_dest_dir = os.path.join(dest_dir_path, item)

            generate_pages_recursive(from_path, template_path, new_dest_dir)
        