import os

from xml.etree import ElementTree
from urllib.request import urlopen
from jinja2 import Environment, FileSystemLoader


# CONFIG
ILIDATA_XML_URL = 'https://models.opengis.ch/ilidata.xml'
METADATA_XML_PATH = './ili:DATASECTION/ili:DatasetIdx16.DataIndex/ili:DatasetIdx16.DataIndex.DatasetMetadata'
OUTPUT_PATH = 'build/index.html'

# Interlis namespaces
namespaces = {'ili': "http://www.interlis.ch/INTERLIS2.3"}

# Load XML document
xmlfile = urlopen(ILIDATA_XML_URL)
document = ElementTree.parse(xmlfile)

# Parse items
items = []
for xmlitem in document.findall(METADATA_XML_PATH, namespaces=namespaces):

    item = {}

    # ID
    id_xmlitem = xmlitem.find('./ili:id', namespaces=namespaces)
    if id_xmlitem is not None:
        item['id'] = id_xmlitem.text

    # Title (multilingual)
    item['titles'] = {}
    titles_xmlitems = xmlitem.findall('./ili:title/ili:DatasetIdx16.MultilingualMText/ili:LocalisedText/ili:DatasetIdx16.LocalisedMText', namespaces=namespaces)
    for title_xmlitem in titles_xmlitems:
        language = title_xmlitem.find('./ili:Language', namespaces=namespaces).text
        title = title_xmlitem.find('./ili:Text', namespaces=namespaces).text
        item['titles'][language] = title

    # Description (multilingual)
    item['descs'] = {}
    descs_xmlitems = xmlitem.findall('./ili:shortDescription/ili:DatasetIdx16.MultilingualMText/ili:LocalisedText/ili:DatasetIdx16.LocalisedMText', namespaces=namespaces)
    for desc_xmlitem in descs_xmlitems:
        language = desc_xmlitem.find('./ili:Language', namespaces=namespaces).text
        desc = desc_xmlitem.find('./ili:Text', namespaces=namespaces).text
        item['descs'][language] = desc

    # Files
    item['files'] = []
    files_xmlitems = xmlitem.findall('./ili:files/ili:DatasetIdx16.DataFile', namespaces=namespaces)
    for file_xmlitem in files_xmlitems:
        format = file_xmlitem.find('./ili:fileFormat', namespaces=namespaces).text
        path = file_xmlitem.find('./ili:file/ili:DatasetIdx16.File/ili:path', namespaces=namespaces).text
        url = f'https://models.opengis.ch/{path}'
        item['files'].append({"format":format,"path":path,"url":url})

    # Categories
    item['categories'] = []
    categories_xmlitems = xmlitem.findall('./ili:categories/ili:DatasetIdx16.Code_', namespaces=namespaces)
    for category_xmlitem in categories_xmlitems:
        value = category_xmlitem.find('./ili:value', namespaces=namespaces).text
        name = value.split('/')[-1]
        item['categories'].append({'name':name,'value':value})

    # Owner
    owner_xmlitem = xmlitem.find('./ili:owner', namespaces=namespaces)
    if owner_xmlitem is not None:
        item['owner_name'] = owner_xmlitem.text.replace('mailto:','')
        item['owner_url'] = owner_xmlitem.text

    items.append(item)

# Render the template
jinja_loader = FileSystemLoader(searchpath=os.path.dirname(__file__))
jinja_env = Environment(loader=jinja_loader)

template = jinja_env.get_template('index.template.html')
output = template.render(items=items)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w') as f:
    f.write(output)
