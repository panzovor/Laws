__author__ = 'E440'
import src.preprocess as pre
import src.tools as tools


if __name__ == "__main__":
    filepath = "../res/data/已完成标注（6818）.txt"

    label_file = "../res/weka/labeled_data.csv"
    # pre.label_process(filepath,label_file)

    feature_file = "../res/weka/feature_data_less.csv"
    # pre.transfer_train(label_file,feature_file)

    arff_file = "../res/weka/train_less.arff"
    pre.csv2arff(feature_file,arff_file)
