from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        
        if delimiter in node.text and node.text_type == TextType.TEXT:
            new_texts = node.text.split(delimiter)
            split_nodes = []
            if len(new_texts) % 2 == 0:
                raise ValueError("Invalid markdown, formatted section not closed")
            counter = 0
            for segment in new_texts:
                if segment == "":
                    counter += 1
                    continue
                if counter == 0:
                    counter += 1
                    split_nodes.append(TextNode(segment, TextType.TEXT))
                else:
                    counter = 0
                    split_nodes.append(TextNode(segment, text_type))
                
            new_nodes.extend(split_nodes)
            

        else:
            new_nodes.append(node)
    
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        for link in links:

            #split text into list of TEXT node strings, each break is a link
            segments = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(segments) != 2:
                raise ValueError("Invalid markdown, link not closed")
            if segments[0] != "":
                new_nodes.append(TextNode(segments[0], TextType.TEXT))

            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = segments[1]
        
        if text != "":
            new_nodes(text, TextType.TEXT)
        
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        imgs = extract_markdown_images(text)

        if len(imgs) == 0:
            new_nodes.append(node)
            continue
        
        for img in imgs:

            #split text into list of TEXT node strings, each break is a image
            segments = text.split(f"![{img[0]}]({img[1]})", 1)
            if len(segments) != 2:
                raise ValueError("Invalid markdown, link not closed")
            if segments[0] != "":
                new_nodes.append(TextNode(segments[0], TextType.TEXT))

            new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))

            text = segments[1]
        
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
        
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes