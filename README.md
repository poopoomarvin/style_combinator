# Style Combinator

## Introduction
This is a project allowing user generate images with desired art style for each class of objects.
In this project, we combine style transfer and object detection with segmentation.

![](https://i.imgur.com/33pbAG5.png)

## Requirement
 - Python 3.7.5
 - PyTorch
 - Cuda 10.1
 - Tensorflow 2.0.0
 - TensorCV
 - Install other dependencies using pip3
    ```
    pip3 install -r requirements.txt
    ```
 - Run setup
    ```
    python3 setup.py install
    ```

## Run
### Train your own style-transfer model
Put the style image in ```data/```, then go to ```sample/``` 
and run ```python3 fast.py --train --styleim FILE_NAME_OF_STYPE_IMAGE```
### Web application
Go to ```sample/``` and run ```python3 main.py```
then open web browser with address http://localhost:5550/

## Examples
![](https://i.imgur.com/nVJHGR1.png)

![](https://i.imgur.com/IEU3t7O.png)

![](https://i.imgur.com/RBa4vjF.jpg)

![](https://i.imgur.com/j060rDx.jpg)



## Demo
[![Demo](https://img.youtube.com/vi/aB0nw8xTAxs/0.jpg)](https://www.youtube.com/watch?v=aB0nw8xTAxs)
## Reference Repo
 - https://github.com/conan7882/fast-style-transfer
 - https://github.com/matterport/Mask_RCNN
