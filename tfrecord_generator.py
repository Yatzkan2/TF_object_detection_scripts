# Script to create TFRecord files from train and test dataset folders

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd

from tensorflow.python.framework.versions import VERSION

#Usage example:
#python scripts\tfrecord_generator.py
#    --csv_file=C:\Users\Yair\Tensorflow\workspace\data\test.csv
#    --image_path=C:\Users\Yair\Tensorflow\workspace\data\test
#    --labelmap_file=C:\Users\Yair\Tensorflow\workspace\data\labelmap.pbtxt
#    --output_file=C:\Users\Yair\Tensorflow\workspace\data\test.record

if VERSION >= "2.0.0a0":
    import tensorflow.compat.v1 as tf
else:
    import tensorflow as tf

from PIL import Image
#from object_detection.utils import dataset_utilfrom object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

from object_detection.utils import dataset_util
from object_detection.utils import label_map_util

flags = tf.app.flags
flags.DEFINE_string('csv_file', '', 'Path to the CSV input')
flags.DEFINE_string('labelmap_file', '', 'Path to the labelmap file')
flags.DEFINE_string('image_path', '', 'Path to the image directory')
flags.DEFINE_string('output_file', '', 'Path to output TFRecord file')
FLAGS = flags.FLAGS

def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []
    
    label_map_dict = label_map_util.get_label_map_dict(FLAGS.labelmap_file)
    
    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(label_map_dict[row['class']])

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))

    return tf_example


def main(_):
    # Load and prepare data
    writer = tf.python_io.TFRecordWriter(FLAGS.output_file)
    path = FLAGS.image_path
    examples = pd.read_csv(FLAGS.csv_file)

    # Create TFRecord files
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_file = FLAGS.output_file
    print('Successfully created the TFRecords: {}'.format(output_file))


if __name__ == '__main__':
    tf.app.run()