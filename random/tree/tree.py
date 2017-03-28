#!/usr/bin/env python

import lxml.etree as etree
import yaml


def build_node(label, parent):
    child = etree.SubElement(parent[-1], 'li')
    element = '<a>{}</a>'.format(str(label).strip().replace('\n', '<br>'))
    child.insert(0, etree.HTML(element))
    return child


def build_tree(element, parent=None):

    if parent is None:
        parent = etree.Element('div')
        parent.attrib['class'] = 'tree'
        etree.SubElement(parent, 'ul')

    if isinstance(element, dict):
        for key, value in element.items():
            child = build_node(key, parent)
            etree.SubElement(child, 'ul')
            build_tree(value, child)
    elif isinstance(element, list):
        for item in element:
            build_tree(item, parent)
    else:
        build_node(element, parent)

    return parent


if __name__ == '__main__':

    page = etree.Element('html')
    head = etree.SubElement(page, 'head')
    body = etree.SubElement(page, 'body')

    style = etree.SubElement(head, 'style')
    with open('tree.css', 'r') as css_file:
        css_styles = css_file.read()
    style.text = css_styles

    with open('tree.yml', 'r') as yml_file:
        data = yaml.safe_load(yml_file.read())
    tree = build_tree(data)

    body.insert(0, tree)
    html = etree.tostring(page).decode()
    with open('tree.html', 'w') as html_file:
        html_file.write(html)
