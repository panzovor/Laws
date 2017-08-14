import src.features as features
import src.train_py as trainer
import src.tools as tools
from src.features import features_extractor
import src.preprocess as pre

### 准备数据
### filepath: 原文件路径（文件内容格式参考标注文件）
### savepath: 处理后的文件保存路径，格式为（标签：句子）
def prepare_data(filepath,savepath):
    pre.label_process(filepath, savepath)

### 训练模型
### filepath: 训练文件路径
### model_path:模型保存路径
### model_name:models = {
###  "randomforest":随机森林,
###  "svm":svm
###  "naivebayes":朴素贝叶斯}
###  result_save_path:分类效果保持路径（None为不保存）
###  train_files,test_files: 若train_files 和test_files都不为空则将训练文件进行切分，以train_files进行训练，test_files进行测试
###
###  return :返回模型训练结果（混淆矩阵，分类准确率，召回率，f值,支持度（正类样本数））
def train_model(filepath,model_path,model_name="naivebayes",result_save_path = None,train_files = None,test_files = None):
    if train_files!=None and test_files!=None:
        pre.seperate_data_by_label(filepath, train_files, test_files)
        result = trainer.train_model(train_file=train_files, test_file=test_files, model_name=model_name,
                            model_save_path=model_path)
    else:
        result = trainer.train_model(filepath,None,model_name=model_name,model_save_path=model_path,res_save_path=result_save_path)
    # report, confuse = trainer.analyse_predict_result(y_test, pre_y_test)
    return result


### 测试模型
### model_path:模型保存路径
### testfile: 测试文件路径格式（标签：句子）
### report: 是否返回报告（true：返回分类结果，及混淆矩阵，false:返回预测类别）
def test_model(model_path,testfile,report=True):
    # print("using test file: ",testfile)
    x_test, y_test = trainer.load_data(testfile)
    pre_y_test = trainer.predict(model_path, x_test)
    real_label = []
    for var in pre_y_test:
        real_label.append(trainer.fea.get_label_name(int(var)))
    # print(len(pre_y_test),len(real_label))
    if report:
        report, confuse = trainer.analyse_predict_result(y_test, pre_y_test)
        return report,confuse
    else:
        return real_label

###
def predict(model_path,testfile):
    x_test, y_test = trainer.load_data(testfile)
    pre_y_test = trainer.predict(model_path, x_test)

    return pre_y_test

def analyze_result(report):
    for line in report:
        if " " not in line[0]:
            print(trainer.fea.get_label_name(int(line[0])) + "\t" + '\t'.join(list(map(str, line[1:]))))

if __name__ == "__main__":

    ## train model
    # file = "../res/data/已完成标注（6818）.txt"
    # labelfile = "../res/data/label.txt"
    #
    # prepare_data(file,labelfile)
    # print("data prepare done")
    #
    # print("start training model")
    model_file = "../res/data/model"
    # train_model(labelfile,model_file)
    # print("model train done")

    ## test model
    file = "../res/data/已完成标注（6818）.txt"
    test_files = "../res/data/test.csv"
    prepare_data(file, test_files)
    print("data prepare done")
    print("start testing model")
    predict(model_file,test_files)
    report,confuse = test_model(model_file,test_files)
    print("test done")

    analyze_result(report)