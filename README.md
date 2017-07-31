This work as done as an assignment for both an Image Processing and a Machine Learning class. We reproduced (aside from a couple of small differences)
the method explored by S. Bayram et al in the paper
*Image manipulation detection with binary similarity measures*. More information about what was done can be found in the various
text files present throughout this repository. The [CASIA v2](http://forensics.idealtest.org/casiav2/) image dataset was used for
training and testing. Credits for the use of the CASIA Image Tempering Detection Evaluation Database (CAISA TIDE) V2.0 are given to the National Laboratory of Pattern Recognition, Institute of Automation, Chinese Academy of Science, Corel Image Database and the photographers. http://forensics.idealtest.org

## Demo Program

Directory `demo` contains a demonstration program. It tries to detect whether an image is blurred or not. It was trained with
authentic images from the CASIA v2 dataset, as well as the same images after being blurred by 7 x 7 gaussian filter, with σ = 1.
The accuracy of the program is hard to measure. It correctly identified authentic images from the dataset in 70 to 90% of the cases.
For blurred images, it depends on how much blur was applied. As the blurring intensifies, it should tend to correctly identify them
100% of the time. For more subtle blurs, the accuracy isn't very good.

### Requirements

* The Makefile file assumes you have `g++` to build the classifier programs.
* Python 3 with NumPy and OpenCV [(installation guide for OpenCV)](http://cyaninfinite.com/tutorials/installing-opencv-in-ubuntu-for-python-3/)

### How to Use
Build everything with `make`.
To test a single image, use `./run image_file.jpg`. To test all the files within a directory, use
`./runall path_to_directory`.

Folder `demo/sample` contains sample testing images. 279 out of the 500 blurred images in `demo/sample/blurred` are correctly classified as so.
342 out of the 500 even more blurred images in `demo/sample/blurred2` are correctly classified as so. Finally 346 out of the 500 authentic images
in `demo/sample/authentic` are correctly identified as so.

