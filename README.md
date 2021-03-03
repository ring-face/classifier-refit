# This is the repo for the classifier retrain service

This service will use the directory structure that is sampled in the `sample-data` dir. It will refit the classifier, and persist the fitted classifier in a persistent file. 

# How to train the classifier
```bash
pip3 install -r requirements.txt
#rm -rf data
cp -r sample-data data
python3 main.py
```

# How to use the trained classifier
```bash
python3 recognitionCmd.py ./data/images/barack/test-images/barack4.jpeg
```


# The process will do the following steps.

Phase 1: Encode the unencoded images
* Encode images in the `new-images` dir and move the file to `encoded-images` dir
* The encoding information is saved as a json array to file in the `encodings` dir under the same file name as the image with `.json` extension
* encoding is using the face_recognition lib, which uses dlib as underlying
* the dlib pretrained model for encoding is loaded at startup from [face_recoginition_models](https://github.com/ageitgey/face_recognition_models/tree/master/face_recognition_models/models) lib


Phase 2: Fit the [Support Vector Classifier](https://scikit-learn.org/stable/modules/svm.html#svm-classification) with the data from the `encodings` dir
* Load each file from the `encodings` folder into a numpy array
* create the same sized array with the name of the persons, where `encodings[i]` represents the encoded face of `persons[i]`
* run `newClassifier=SVC.fit(encodings, persons)`
* [persist](https://scikit-learn.org/stable/modules/model_persistence.html) the `newModel` to the `data/classifier` dir in as `fitting.timestamp` 

Phase 3: Test the new model
* loads the persisted classifier, and tests ist capabilities on the test set of the **/test-images folder
* in addition to the classification, it calculates an euclidian distance from the encodings of the found person
* only if the distance is below a treshold, is the classification valid
* this avoids recognising arbitrary face as known person


Once this is finished, the proces exits