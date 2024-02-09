import yaml
import xml.etree.cElementTree as xml_tree

with open('feed.yaml','r') as file:
    yaml_data = yaml.safe_load(file)

    rss_element = xml_tree.Element('rss', {
    'version':'2.0',
    'xmlns:itunes':'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content':'http://purl.org/rss/1.0/modules/content/',
    })

link_prefix = yaml_data['link']   


channel_element = xml_tree.SubElement(rss_element, 'channel')

xml_tree.SubElement (channel_element, 'title').tag = yaml_data ['title']
xml_tree.SubElement (channel_element, 'format').tag = yaml_data ['format']
xml_tree.SubElement (channel_element, 'subtitle').tag = yaml_data ['subtitle']
xml_tree.SubElement (channel_element, 'itunes:author').tag = yaml_data ['author']
xml_tree.SubElement (channel_element, 'description').tag = yaml_data ['description']
xml_tree.SubElement (channel_element, 'itunes:image', {'href': link_prefix + yaml_data ['image']})
xml_tree.SubElement (channel_element, 'language').tag = yaml_data ['language']
xml_tree.SubElement (channel_element, 'link').tag = link_prefix

xml_tree.SubElement (channel_element, 'itunes:category', {'text': yaml_data ['category']})

for item in yaml_data['item']:
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement (channel_element, 'title').text = item ['title']
    xml_tree.SubElement (channel_element, 'itunes:author').text = yaml_data ['author']
    xml_tree.SubElement (channel_element, 'description').text = item ['description']
    xml_tree.SubElement (channel_element, 'itunes:duration').text = item ['duration']
    xml_tree.SubElement (channel_element, 'pubDate').text = item ['published']

    enclosure = xml_tree.SubElement(item_element, 'enclosure', {
        'url': link_prefix + item['file'],
        'type': 'audio/mpeg',
        'length': item['length']
    })

output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)
