import math
import pandas as pd


def calculate_entropy(zeros_count, ones_count):

    if zeros_count == 0 or ones_count == 0:
        return 0

    if heuristic_val.lower() == "h1":
        value_one = ones_count/(ones_count+zeros_count)
        value_zero = zeros_count/(ones_count+zeros_count)

        if value_one != 0 and value_zero != 0:
            entropy = -value_one*math.log2(value_one) - \
                value_zero*math.log2(value_zero)
        elif value_one == 0 and value_zero != 0:
            entropy = - value_zero*math.log2(value_zero)
        elif value_one != 0 and value_zero == 0:
            entropy = -value_one*math.log2(value_one)
        elif value_one == 0 and value_zero == 0:
            entropy = 0
        return entropy
    elif heuristic_val.lower() == "h2":
        return (zeros_count * ones_count)/((zeros_count+ones_count) ** 2)


def calculate_gain(entropy, attr_one, attr_zero, attr_one_one, attr_one_zero, attr_zero_one, attr_zero_zero):

    weight_attr_one = attr_one/(attr_one+attr_zero)
    weight_attr_zero = attr_zero/(attr_one+attr_zero)

    entropy_one = calculate_entropy(attr_one_zero, attr_one_one)
    entropy_zero = calculate_entropy(attr_zero_zero, attr_zero_one)

    gain = entropy - weight_attr_one * entropy_one - weight_attr_zero * entropy_zero

    return gain


class node_tree:
    def __init__(self, leaf_node=False):
        self.node_name = None  # node_name
        self.left_node = None  # left_node
        self.right_node = None  # right_node
        self.leaf_node = leaf_node  # leaf_node
        self.leaf_0_value = None
        self.leaf_1_value = None
        self.one_len_1 = None
        self.one_len_0 = None
        self.zero_len_1 = None
        self.zero_len_0 = None

    def loop_cols(self, datafrm):
        max_gain = -99

        jkl = 0
        for col in datafrm.columns:
            jkl = jkl + 1
            if col != "Class":
                gain = gain_of_col(col, datafrm)
                if gain >= max_gain:
                    max_gain = gain
                    max_gain_node = col
            elif jkl == 1:
                max_gain_node = col

        if max_gain_node == 'Class':
            print("Class Detected")

        self.node_name = max_gain_node

        temp_df = datafrm[datafrm[self.node_name]
                          > 0].drop(self.node_name, axis=1)
        temp_df1 = datafrm[datafrm[self.node_name]
                           < 1].drop(self.node_name, axis=1)

        self.one_len_1 = len(temp_df[temp_df['Class'] > 0])
        self.zero_len_1 = len(temp_df[temp_df['Class'] < 1])

        self.one_len_0 = len(temp_df1[temp_df1['Class'] > 0])
        self.zero_len_0 = len(temp_df1[temp_df1['Class'] < 1])

        if len(temp_df.columns) == 1:
            self.leaf_node = True
            self.leaf_1_value = 1 if max(
                self.one_len_1, self.zero_len_1) == self.one_len_1 else 0
            self.type = 1
        elif self.zero_len_1 == 0 or self.one_len_1 == 0:
            self.leaf_node = True
            self.leaf_1_value = 1 if self.zero_len_1 == 0 else 0
            self.type = 1
        else:

            self.right_node = node_tree()
            self.right_node.loop_cols(temp_df)

        if len(temp_df1.columns) == 1:
            self.leaf_node = True
            self.leaf_0_value = 1 if max(
                self.one_len_0, self.zero_len_0) == self.one_len_0 else 0
            self.type = 0
        elif self.zero_len_0 == 0 or self.one_len_0 == 0:
            self.leaf_node = True
            self.leaf_0_value = 1 if self.zero_len_0 == 0 else 0
            self.type = 0
        else:
            self.left_node = node_tree()
            self.left_node.loop_cols(temp_df1)


def gain_of_col(col, df1):
    df2 = df1[df1[col] > 0]

    df3 = df1[df1[col] < 1]

    if df3.empty:
        c = d = 0
    else:
        if df3[df3['Class'] > 0].empty:
            c = 0
        else:
            c = len(df3[df3['Class'] > 0])
        if df3[df3['Class'] < 1].empty:
            d = 0
        else:
            d = len(df3[df3['Class'] > 0])

    if df2.empty:
        a = b = 0
    else:
        if df2[df2['Class'] > 0].empty:
            a = 0
        else:
            a = len(df2[df2['Class'] > 0])
        if df2[df2['Class'] < 1].empty:
            b = 0
        else:
            b = len(df2[df2['Class'] > 0])

    if df1[df1['Class'] > 0].empty:
        A = 0
    else:
        A = len(df1[df1['Class'] > 0])

    if df1[df1['Class'] < 1].empty:
        B = 0
    else:
        B = len(df1[df1['Class'] < 1])
    if df1[df1[col] > 0].empty:
        C = 0
    else:
        C = len(df1[df1[col] > 0])
    if df1[df1[col] < 1].empty:
        D = 0
    else:
        D = len(df1[df1[col] < 1])

    return calculate_gain(calculate_entropy(A, B), C, D, a, b, c, d)


def predic_test(curr, curr1, row_attr, name):

    if curr.node_name == None:
        print("NONE skipped")
        return 1

    if curr.leaf_1_value == None:

        curr = curr.right_node
        return_value = predic_test(curr, curr, row_attr, name)

    elif curr.leaf_1_value == 0 or curr.leaf_1_value == 1:

        if row_attr[curr.node_name] == 1:
            return_value = curr.leaf_1_value
            return return_value
    if curr1.leaf_0_value == None:
        curr1 = curr1.left_node
        return_value = predic_test(curr1, curr1, row_attr, name)
        return return_value
    elif curr1.leaf_0_value == 0 or curr1.leaf_0_value == 1:
        if row_attr[curr1.node_name] == 0:
            return_value = curr1.leaf_0_value
            return return_value
    return return_value


def find_accuracy(name, df):
    counter = 0
    for i in range(len(df)):
        return_value = None
        predicted_value = predic_test(curry, curry, df.iloc[i], name)
        original_value = df.iloc[i]['Class']

        if predicted_value == original_value:
            counter = counter + 1

    accuracy = counter / len(df)
    print(name+" data's accuracy is: " + str(round(accuracy*100, 2)) + "%")


def draw_tree(curr, curr1, string, counter):
    if curr.leaf_1_value == None:

        counter += 1
        temp = ""
        for i in range(counter):
            temp += "| "
        print(temp+str(curr.node_name)+" = 1 : ")

        curr = curr.right_node
        draw_tree(curr, curr, string, counter)
    elif curr.leaf_1_value == 0 or curr.leaf_1_value == 1:
        counter += 1
        temp = ""
        for i in range(counter):
            temp += "| "
        print(temp+curr.node_name+" = 1 : "+str(curr.leaf_1_value))

    if curr1.leaf_0_value == None:

        temp = ""
        for i in range(counter):
            temp += "| "
        print(temp+curr1.node_name+" = 0 : ")
        curr1 = curr1.left_node
        draw_tree(curr1, curr1, string, counter)
    elif curr1.leaf_0_value == 0 or curr1.leaf_0_value == 1:
        temp = ""
        for i in range(counter):
            temp += "| "
        print(temp+curr1.node_name+" = 0 : "+str(curr1.leaf_0_value))


return_value = 0

input_value = input(
    "Enter the inputs with spaces: <Training Set Path> <Validation Set Path> <Test Set Path> <Print Tree?Yes/No> <Heuristic?H1/H2>")

# input_value = "D:\data_TEMP\\training_set.csv D:\data_TEMP\\validation_set.csv D:\data_TEMP\\test_set.csv yes h1"

input_value = input_value.replace("\\", "/")
input_value = input_value.split(' ')
training_data = input_value[0]
validation_data = input_value[1]
test_data = input_value[2]
print_tree = input_value[3]
heuristic_val = input_value[4]

if print_tree.lower() != "yes" and print_tree.lower() != "no":
    print("You have selected a unknown option for print tree. Please provide yes/no and retry.\nExiting..")
    exit()
if heuristic_val.lower() != "h1" and heuristic_val.lower() != "h2":
    print("You have selected a unknown option for Heuristic_val. Please provide h1/h2 and retry.\nExiting..")
    exit()


df = pd.read_csv(training_data)
vf = pd.read_csv(validation_data)
tf = pd.read_csv(test_data)

if heuristic_val.lower() == "h1":
    print("Showing details for Information Gain Heuristic:")
    dt = node_tree()  # training
    dt.loop_cols(df)

    curry = dt

    find_accuracy("Training", df)
    find_accuracy("Validation", vf)
    find_accuracy("Test", tf)

    if print_tree.lower() == "yes":
        string = "a"
        draw_tree(curry, curry, string, -1)
elif heuristic_val.lower() == "h2":
    print("Showing details for Variance Impurity Heuristic:")
    dt = node_tree()  # training
    dt.loop_cols(df)

    curry = dt

    find_accuracy("Training", df)
    find_accuracy("Validation", vf)
    find_accuracy("Test", tf)

    if print_tree.lower() == "yes":
        string = "a"
        draw_tree(curry, curry, string, -1)