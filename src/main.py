import src.features as features
import src.train_py as trainer
import src.tools as tools
from src.features import features_extractor
import src.preprocess as pre

def prepare_data(filepath,savepath):
    pre.label_process(filepath, savepath)

def train_model(filepath,model_path,model_name="naivebayes",result_save_path = None,train_files = None,test_files = None):
    if train_files!=None and test_files!=None:
        pre.seperate_data_by_label(filepath, train_files, test_files)
        result = trainer.train_model(train_file=train_files, test_file=test_files, model_name=model_name,
                            model_save_path=model_path)
    else:
        result = trainer.train_model(filepath,None,model_name=model_name,model_save_path=model_path,res_save_path=result_save_path)
    # report, confuse = trainer.analyse_predict_result(y_test, pre_y_test)
    return result

def test_model(model_path,testfile):
    # print("using test file: ",testfile)
    x_test, y_test = trainer.load_data(testfile)
    pre_y_test = trainer.predict(model_path, x_test)
    report, confuse = trainer.analyse_predict_result(y_test, pre_y_test)
    # fea = features_extractor()
    # for line in report:
    #     print(fea.get_label_name(int(line[0]))+"\t"+'\t'.join(list(map(str,line[1:]))))
    return report,confuse

def analyze_result(report):
    for line in report:
        if " " not in line[0]:
            print(trainer.fea.get_label_name(int(line[0])) + "\t" + '\t'.join(list(map(str, line[1:]))))

if __name__ == "__main__":

    ## train model
    file = "../res/data/已完成标注（6818）.txt"
    labelfile = "../res/data/label.txt"

    prepare_data(file,labelfile)
    print("data prepare done")

    print("start training model")
    model_file = "../res/data/model"
    train_model(labelfile,model_file)
    print("model train done")

    ## test model
    file = "../res/data/已完成标注（6818）.txt"
    test_files = "../res/data/test.csv"
    prepare_data(file, labelfile)
    print("data prepare done")
    print("start testing model")
    report,confuse = test_model(model_file,test_files)
    print("test done")

    analyze_result(report)