#!/usr/bin/env python3
#
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Script to run generic MobileNet based classification model."""
import argparse
from gpiozero import Buzzer
from aiy.pins import (PIN_A, PIN_B, PIN_C, PIN_D)
from picamera import PiCamera, Color

from time import sleep
from aiy.vision import inference
from aiy.vision.models import utils
#find = ''
check = 0
bz1=Buzzer(PIN_A)
bz2=Buzzer(PIN_B)
bz3=Buzzer(PIN_C)
def read_labels(label_path):
    with open(label_path) as label_file:
        return [label.strip() for label in label_file.readlines()]


def get_message(result, threshold, top_k):
    if result:
        return 'Detecting:\n %s' % '\n'.join(result)

    return 'Nothing detected when threshold=%.2f, top_k=%d' % (threshold, top_k)


def process(result, labels, tensor_name, threshold, top_k,search):
    """Processes inference result and returns labels sorted by confidence."""
    # MobileNet based classification model returns one result vector.
  #  find = input("Enter the object to hit")
  #  print(find)
    assert len(result.tensors) == 1
    tensor = result.tensors[tensor_name]
    probs, shape = tensor.data, tensor.shape
    assert shape.depth == len(labels)
    pairs = [pair for pair in enumerate(probs) if pair[1] > threshold]
    pairs = sorted(pairs, key=lambda pair: pair[1], reverse=True)
    pairs = pairs[0:top_k]
    print("Labels")
    print(labels)
    for x in range(0,len(labels)-1):
        print(labels[x])
        if labels[x] == search:
             if(probs[x]>0.5):
                check = 0
                print("Object is found")
                print(probs[x])
                bz1.on()
                bz2.off()
                bz3.on()
                bz4.off()
             elif(probs[x]>0.2):
                print("Not sure")
                print(probs[x])
                if(check>probs[x]):
                    bz1.on()
                    bz2.off()
                    bz3.on()
                    bz4.off()
                check = probs[x]
                else:
                    bz1.off()
                    bz2.on()
                    bz3.off()
                    bz4.on()
                    sleep(2)
                    bz1.off()
                    bz2.on()
                    bz3.on()
                    bz4.off()
                    sleep(2)
             else:
                check = 0
                print("Object not found,Searching")
                print(probs[x])
                bz1.on()
                bz2.off()
                bz3.off()
                bz4.on()
    return [' %s (%.2f)' % (labels[index], prob) for index, prob in pairs]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', required=True,
        help='Path to converted model file that can run on VisionKit.')
    parser.add_argument('--label_path', required=True,
        help='Path to label file that corresponds to the model.')
    parser.add_argument('--input_height', type=int, required=True, help='Input height.')
    parser.add_argument('--input_width', type=int, required=True, help='Input width.')
    parser.add_argument('--input_layer', required=True, help='Name of input layer.')
    parser.add_argument('--output_layer', required=True, help='Name of output layer.')
    parser.add_argument('--num_frames', type=int, default=None,
        help='Sets the number of frames to run for, otherwise runs forever.')
    parser.add_argument('--input_mean', type=float, default=128.0, help='Input mean.')
    parser.add_argument('--input_std', type=float, default=128.0, help='Input std.')
    parser.add_argument('--input_depth', type=int, default=3, help='Input depth.')
    parser.add_argument('--threshold', type=float, default=0.1,
        help='Threshold for classification score (from output tensor).')
    parser.add_argument('--top_k', type=int, default=3, help='Keep at most top_k labels.')
    parser.add_argument('--show_fps', action='store_true', default=False,
        help='Shows end to end FPS.')
    args = parser.parse_args()
    find = input("Enter the name of the object to hit")

    model = inference.ModelDescriptor(
        name='mobilenet_based_classifier',
        input_shape=(1, args.input_height, args.input_width, args.input_depth),
        input_normalizer=(args.input_mean, args.input_std),
        compute_graph=utils.load_compute_graph(args.model_path))
    labels = read_labels(args.label_path)

    with PiCamera(sensor_mode=4, resolution=(1640, 1232), framerate=30) as camera:
        with inference.CameraInference(model) as camera_inference:
            for result in camera_inference.run(args.num_frames):
                processed_result = process(result, labels, args.output_layer,
                                           args.threshold, args.top_k,find)
                print(processed_result)
#                print(processed_result[0].prob)
            #    message = get_message(processed_result, args.threshold, args.top_k)
            #    if args.show_fps:
            #        message += '\nWith %.1f FPS.' % camera_inference.rate
            #    print(message)

main()
