# Inducing Decision Trees
## Description
Implement and test the decision tree learning algorithm.

 - Download the two datasets available on myCourses. Each data set is divided into three sets: the training set, the validation set and the test set. Data sets are in CSV format. The first line in the file gives the attribute names. Each line after that is a training (or test) example that contains a list of attribute values separated by a comma. The last attribute is the class-variable. Assume that all attributes take values from the domain (0,1).

 - Implemented the decision tree learning algorithm. The main step in decision tree learning is choosing the next attribute to split on. Implemented the following two heuristics for selecting the next attribute -
 
1. Information gain heuristic.
2. Variance impurity heuristic described below.
Let K denote the number of examples in the training set. Let K0 denote the number of training examples that have class = 0 and K1 denote the number of training examples that have class = 1. The variance impurity of the training set S is defined as:

![pic1](/images/pic1.JPG)

Notice that the impurity is 0 when the data is pure. The gain for this impurity is defined as usual.

![pic2](/images/pic2.JPG)

where X is an attribute, Sx denotes the set of training examples that have X = x and Pr(x) is the fraction of the training examples that have X = x (i.e., the number of training examples that have X = x divided by the number of training examples in S).


Implemented a function to print the decision tree to standard output. We will use the following format.

![pic3](/images/pic3.JPG)

According to this tree, if wesley = 0 and honor = 0 and barclay = 0, then the class value of the corresponding instance should be 1. In other words, the value appearing before a colon is an attribute value, and the value appearing after a colon is a class value.

## How to Run?
a. Place the file `DecisionTree.py` in a directory.
b. use below command to run the script
   ```
   python DecisionTree.py
   ```
c. Parameters for the script would be asked now. Please provide in below format -   
   <Training dataset Path> <Validation dataset Path> <Test dataset Path> <Print Tree?Yes/No> <Heuristic?H1/H2>  
   Ex:-  
   ```
   D:\data_TEMP\\training_set.csv D:\data_TEMP\\validation_set.csv D:\data_TEMP\\test_set.csv yes h1
   ```
d. Thats it! Output would show the accuracies for training, validation, test data. Along with decision tree based on input provided.