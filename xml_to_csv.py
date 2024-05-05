import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import argparse

#usage:
#python .\scripts\xml_to_csv.py 
#    C:\Users\Yair\Tensorflow\workspace\data\train 
#    --output_path=C:\Users\Yair\Tensorflow\workspace\data 
#    --csv_file_name=train

parser = argparse.ArgumentParser(description='This script is converting xml files annotation pascal formatted to a csv files.')

parser.add_argument('annotation_path', help='Global path to xml annotation files')
parser.add_argument('--output_path', help='Global path to csv folder', default=os.getcwd())
parser.add_argument('--csv_file_name', help='csv file name', default='annotation_file')

args = parser.parse_args()

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def main():
    xml_df = xml_to_csv(args.annotation_path)
    xml_df.to_csv((args.output_path+os.sep+args.csv_file_name+'.csv'), index=None)
    print('Successfully converted xml to csv.')
if __name__ == '__main__':
    main()