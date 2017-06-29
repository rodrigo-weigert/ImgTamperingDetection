In this test we ran the entire unmodified CASIAv2 set through our method.
We got a 63.5% accuracy, which is not great, considering that always guessing the image's class as authentic (0) would give around 60% accuracy.
This result is expected, as this classifier isn't powerful enough to perform well on this highly nontrivial classification task.

STEPS TO REPRODUCE THE RESULTS:


STEP 1) Extract the features of all the images of dataset **IT TAKES SEVERAL HOURS!**

./extractFeatures.py .../Au > Au_features.dat
./extractFeatures.py .../Tp > Tp_features.dat


STEP 2) Substitute the image file names in the features files for the class label (0: authentic, 1: tampered)

./removeNames.py Au_features.dat Au_features_nonames.dat
./removeNames.py Tp_features.dat Tp_features_nonames.dat

STEP 3) Apply PCA to transform the features, inspect the relevances of the new generated features, decide how many
features are going to be used, and finally split the dataset into training and test set for the classifier (train.dat and test.dat)

./processData.py Au_features_nonames.dat Tp_features_nonames.dat

It will display the relevances of the new features and ask how many should be used.

** WE USED 32. **
(it selects the 32 most relevant ones, if this isn't obvious).

It will then ask for the fraction of the instances that should go on the test set.
** WE USED 0.3. **

After this step, files train.dat and test.dat are generated in the same directory of extractFeatures.py

STEP 5) Make sure the INPUT_SIZE macro of the classifier files (test.cpp and train.cpp) are appropriately set to the
number of features used (in our case, to 32 -- the class label doesn't count). Recompile the classifier (use the Makefile!):

make


STEP 6) Making sure that the generated train.dat and test.dat are in the same directory of the classifier executables (test and train),
run the training program of the classifier with the parameters we used.

./train 20 0.1 0.2

When it is done it'll generate a description file of the trained classifier.
Its name will be classifier-20-0.1-0.2-X.dat, where X is the accuracy the classifier achieved
for the TRAINING set.

STEP 7) Run the testing program of the classifier, passing the description generated in the previous step.

./test classifier-20-0.1-0.2-X.dat

Our results:
-----------------------
./test classifier-20-0.1-0.2-X.dat

right: 2406, wrong: 1378 (0.635835 success rate)
true negative: 1662 (68.23% of all negatives)
false negative: 774 (31.77% of all negatives)
true positive: 744 (55.19% of all positives)
false positive: 604 (44.81% of all positives)
-----------------------

Analysis of the content of the train.dat and test.dat files:
--------------------------
./analyzeData.py train.dat

authentic: 5225 (59.173 %), tampered: 3605 (40.827 %), total: 8830
--------------------------

--------------------------
./analyzeData.py test.dat

authentic: 2266 (59.884 %), tampered: 1518 (40.116 %), total: 3784
--------------------------

All the files we generated/used are located in the same folder as this README.
