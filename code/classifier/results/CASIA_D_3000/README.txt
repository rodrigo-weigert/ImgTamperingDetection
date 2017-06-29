This test is similar to the All_CASIAv2 one, except:
	- We only used tampered images which had content from a different image pasted on them.
	- We didn't use all the authentic images, instead we just selected 1500 of them randomly.
We got a 65.5% accuracy, which is only marginally better than the performance on the All_CASIAv2 test.

STEPS TO REPRODUCE THE RESULTS:


STEP 1) Isolate the features of the desired tampered images from the Tp_features.dat file generated in step 1 of the All_CASIAv2 test.

./separateImages.py Tp_features.dat D AAA A A

It will create the Tp_D_AAA_A_A.dat file, which contains only the tampered images whose name starts with Tp_D.
Rename this file to tampered_features.dat.

STEP 2) Substitute the image file names in the appropriate features files for the class label (0: authentic, 1: tampered)

./removeNames.py tampered_features.dat tampered_features_no_names.dat

STEP 3) Apply PCA to transform the features, inspect the relevances of the new generated features, decide how many
features are going to be used, and finally split the dataset into training and test set for the classifier (train.dat and test.dat)

./processData.py Au_features_nonames.dat tampered_features_no_names.dat

(Au_features_nonames.dat is the same file of All_CASIAv2 test).

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

./train 20 0.05 0.1

When it is done it'll generate a description file of the trained classifier.
Its name will be classifier-20-0.05-0.1-X.dat, where X is the accuracy the classifier achieved
for the TRAINING set.

STEP 7) Run the testing program of the classifier, passing the description generated in the previous step.

./test classifier-20-0.05-0.1-X.dat

Our results:
-----------------------
./test classifier-20-0.05-0.1-X.dat

right: 657, wrong: 348 (0.653731 success rate)
true negative: 251 (63.07% of all negatives)
false negative: 147 (36.93% of all negatives)
true positive: 406 (66.89% of all positives)
false positive: 201 (33.11% of all positives)
-----------------------

Analysis of the content of the train.dat and test.dat files:
--------------------------
./analyzeData.py train.dat

authentic: 5225 (59.173 %), tampered: 3605 (40.827 %), total: 8830
--------------------------

--------------------------
./analyzeData.py test.dat

authentic: 1048 (44.710 %), tampered: 1296 (55.290 %), total: 2344
--------------------------

All the files we generated/used are located in the same folder as this README.
