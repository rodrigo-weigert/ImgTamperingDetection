Scaling by a factor of 0.5  was applied to a random sample of 500 authentic images from the CASIA v2
dataset, creating a dataset of 1000 images. This dataset was randomly split into 50% for training and 50% for testing.
We obtained an accuracy of 72% on the testing set.

STEPS TO REPRODUCE THE RESULTS:

STEP 1) Get the sample:

./randomSample.py [directory of the authentic images of CASIA v2] [destination directory for the random sample] 500


STEP 2) Get the scaled version of the sample and add it to the sample as tampered images.

./scaling.py [directory of the random sample] [directory of the random sample] 2


STEP 3) Extract the features of the sample **IT TAKES SEVERAL MINUTES!**

./extractFeatures.py [directory of the random sample] > scalinghalfsize.dat


STEP 4) Substitute the image file names in features.dat for the class label (0: authentic, 1: tampered)

./removeNames.py scalinghalfsize.dat scalinghalfsize2.dat

STEP 5) Apply PCA to transform the features, inspect the relevances of the new generated features, decide how many
features are going to be used, and finally split the dataset into training and test set for the classifier (train.dat and test.dat)

./processData.py scalinghalfsize2.dat

It will display the relevances of the new features and ask how many should be used.

** WE USED 32. **
(it selects the 32 most relevant ones, if this isn't obvious).

It will then ask for the fraction of the instances that should go on the test set.
** WE USED 0.5. **

After this step, files train.dat and test.dat are generated in the same directory of extractFeatures.py


STEP 6) Make sure the INPUT_SIZE macro of the classifier files (test.cpp and train.cpp) are appropriately set to the
number of features used (in our case, to 32 -- the class label doesn't count). Recompile the classifier (use the Makefile!):

make

STEP 7) Making sure that the generated train.dat and test.dat are in the same directory of the classifier executables (test and train),
run the training program of the classifier with the parameters we used.

./train 10 0.2 0.1

When it is done it'll generate a description file of the trained classifier.
Its name will be classifier-10-0.2-0.1-X.dat, where X is the accuracy the classifier achieved
for the TRAINING set.

STEP 8) Run the testing program of the classifier, passing the description generated in the previous step.

./test classifier-10-0.2-0.1-X.dat

Our results:
-----------------------
./test classifier-10-0.2-0.1-X.dat

right: 362, wrong: 138 (0.724 success rate)
true negative: 163 (75.12% of all negatives)
false negative: 54 (24.88% of all negatives)
true positive: 199 (70.32% of all positives)
false positive: 84 (29.68% of all positives)
-----------------------

Analysis of the content of the train.dat and test.dat files:

--------------------------
./analyzeData.py train.dat

authentic: 253 (50.600 %), tampered: 247 (49.400 %), total: 500
--------------------------

--------------------------
./analyzeData.py test.dat

authentic: 247 (49.400 %), tampered: 253 (50.600 %), total: 500
--------------------------

All the files we generated/used are located in the same folder as this README.
