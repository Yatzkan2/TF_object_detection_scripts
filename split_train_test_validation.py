import os
import random
import shutil
import argparse

def main(args):
    # Define paths to image folders
    image_folder_path = args.image_folder_path
    train_path = os.path.join(os.path.dirname(image_folder_path), 'train')
    val_path = os.path.join(os.path.dirname(image_folder_path), 'validation')
    test_path = os.path.join(os.path.dirname(image_folder_path), 'test')

    # Create train, validation, and test folders if they do not exist
    os.makedirs(train_path, exist_ok=True)
    os.makedirs(val_path, exist_ok=True)
    os.makedirs(test_path, exist_ok=True)

    # Get list of all files in the image folder
    files = os.listdir(image_folder_path)

    # Filter JPEG/JPG files
    image_files = [f for f in files if f.lower().endswith('.jpeg') or f.lower().endswith('.jpg')]

    # Create a dictionary to store image file paths with their corresponding XML file paths
    file_pairs = {}
    for image_file in image_files:
        image_file_name, _ = os.path.splitext(image_file)
        xml_file = image_file_name + '.xml'
        if xml_file in files:
            file_pairs[image_file] = xml_file

    # Shuffle the file pairs
    random.seed(42)  # for reproducibility
    file_pairs = list(file_pairs.items())
    random.shuffle(file_pairs)

    # Split the file pairs into train, validation, and test sets
    train_split = args.train_split  # 70% for training
    val_split = args.val_split      # 20% for validation
    test_split = args.test_split    # 10% for testing

    total_pairs = len(file_pairs)
    train_count = int(total_pairs * train_split)
    val_count = int(total_pairs * val_split)

    train_pairs = file_pairs[:train_count]
    val_pairs = file_pairs[train_count:train_count + val_count]
    test_pairs = file_pairs[train_count + val_count:]

    # Move files to the train, validation, and test folders
    def move_files(pairs, destination_folder):
        for image_file, xml_file in pairs:
            shutil.move(os.path.join(image_folder_path, image_file), os.path.join(destination_folder, image_file))
            shutil.move(os.path.join(image_folder_path, xml_file), os.path.join(destination_folder, xml_file))

    move_files(train_pairs, train_path)
    move_files(val_pairs, val_path)
    move_files(test_pairs, test_path)

    print("Splitting complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split image and XML files into train, validation, and test sets.')
    parser.add_argument('image_folder_path', type=str, help='Path to the image folder')
    parser.add_argument('--train_split', type=float, default=0.7, help='Fraction of data for training (default: 0.7)')
    parser.add_argument('--val_split', type=float, default=0.2, help='Fraction of data for validation (default: 0.2)')
    parser.add_argument('--test_split', type=float, default=0.1, help='Fraction of data for testing (default: 0.1)')
    args = parser.parse_args()

    main(args)
