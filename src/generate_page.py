from block_to_html import markdown_to_html_node

import os


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")








# def extract_title(markdown):
#     return markdown.split("\n\n")[0].strip("# ").strip()

# def generate_page(from_path, template_path, dest_path):
#     print(f"Generating page from {from_path} to {dest_path} using {template_path}")

#     with open(from_path, "r") as f:
#         markdown = f.read()

#     with open(template_path, "r") as f:
#         template = f.read()

#     title = extract_title(markdown)

#     html = markdown_to_html_node(markdown).to_html()

#     final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

#     if not os.path.exists(os.path.dirname(dest_path)):
#         os.mkdir(os.path.dirname(dest_path))
#     with open(dest_path, "w") as f:
#         f.write(final_html)
