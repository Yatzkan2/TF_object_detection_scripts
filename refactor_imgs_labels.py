import os
import uuid
import xml.etree.ElementTree as ET
import argparse

#RUN THE FOLLOWING COMMAND:
#python rename_files.py <path_to_images_xml_folder>


def rename_files(folder_path):
    # Iterate over each file in the folder
    for image_file in os.listdir(folder_path):
        if image_file.endswith(('.jpg', '.jpeg', '.JPG', '.JPEG')):
            # Generate a unique ID
            special_id = str(uuid.uuid4())

            # Create new file names
            new_image_name = f'{special_id}.jpg'
            new_xml_name = f'{special_id}.xml'
            
            # Rename image file
            os.rename(os.path.join(folder_path, image_file), os.path.join(folder_path, new_image_name))

            # Check if corresponding XML file exists
            xml_file = image_file.split('.')[0] + '.xml'
            if not os.path.exists(os.path.join(folder_path, xml_file)):
                # Delete the image file and move on to the next iteration
                os.remove(os.path.join(folder_path, new_image_name))
                continue

            # Rename XML file
            os.rename(os.path.join(folder_path, xml_file), os.path.join(folder_path, new_xml_name))

            # Update XML content
            xml_path = os.path.join(folder_path, new_xml_name)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Update folder tag
            folder_tag = root.find('folder')
            folder_tag.text = folder_path

            # Update filename tag
            filename_tag = root.find('filename')
            filename_tag.text = new_image_name

            # Update path tag
            path_tag = root.find('path')
            path_tag.text = os.path.join(folder_path, new_image_name)

            # Save the modified XML
            tree.write(xml_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rename image and XML files in a folder.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing image and XML pairs')
    args = parser.parse_args()

    rename_files(args.folder_path)
