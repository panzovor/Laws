
__author__ = 'czb'

import src.tools as tools
import re
import random
# from src.feature_extractor import feature_extractor
from src.features import features_extractor
jingdu= 4
fe = features_extractor()

sentence_min_len =3
# sentence_ = ["，】","。】","：】"]
# replace_ =  ["】#","】#","】#"]
sentences_regex = "，|。|：|；"

max_samples = 50000

def content_filter(content):
    if "。【" in content:
        content = content.replace("。【","。】【")
    if "，【" in content:
        content = content.replace("，【","，】【")
    if "；【" in content:
        content = content.replace("；【","；】【")
    content = get_sucheng(content)
    fake_label_regex = "\[.{2,7}\]"
    fayuan_regex = ".{2,5}省.{1,20}法院\n"
    zihao_regex = ".{3,10}字第.{1,6}号\n"
    content = content.strip()
    content = re.sub(fake_label_regex, "", content)
    content = re.sub(fayuan_regex,"",content)
    content = re.sub(zihao_regex,"",content)
    content = content.replace("\n","")
    # for i in range(len(sentence_)):
    #     sen_ = sentence_[i]
    #     if sen_ in content:
    #         content = content.replace(sen_, replace_[i])
    return content

def get_assey(content,filter = True):
    instrument_regex = "【--\d{1,6}--】"
    asseys = [var.strip() for var in re.split(instrument_regex,content) if len(var.strip())>0]
    asseys_no = re.findall(instrument_regex,content)
    result ={}
    for i in range(len(asseys_no)):
        no = asseys_no[i][len("【--"):-len("--】")]
        # print(no,asseys_no[i])
        if no not in result.keys():
            if filter:
                result[no] = content_filter(asseys[i])
            else:
                result[no] = asseys[i]
    return result

def __label_content(content):
    result = {}
    label_regex = "【.{2,18}?：.*?】"
    content = content.replace(":","：")
    labeled_data = re.findall(label_regex,content)
    unlabeled_data = re.sub(label_regex,"",content)
    for ldata in labeled_data:
        ldata = ldata.strip()
        label = ldata[1:ldata.index("：")]
        label = label.replace("【","")
        label = label.replace("】","")
        label = label.replace("-","")
        data  =ldata[ldata.index("：")+1:-1]
        if label not in result.keys():
            result[label] = []
        if "【" not in data and "】" not in data:
            result[label].append(data.strip())
        # datas = re.split(sentences_regex,data)
        # for d in datas:
        #     if len(d.strip()) > sentence_min_len:
        #         result[label].append(d)
    if len(unlabeled_data) >0:
        result["None"] = []
        for uldata in re.split(sentences_regex,unlabeled_data):
            if len(uldata.strip()) > sentence_min_len and ("【" not in uldata and "】" not in uldata):
                result["None"].append(uldata.strip())
    return result

def content_preprocess(content):
    no_content = get_assey(content)
    nos = list(sorted(no_content.keys()))
    nll,lnl,ll ={},{},{}
    for no in nos:
        content = no_content[no]
        nll[no] = __label_content(content)
        for label in nll[no].keys():
            if label not in lnl.keys():
                lnl[label] = {}
            lnl[label][no] = nll[no][label]
            if label not in ll.keys():
                ll[label]= []
            if len(ll[label]) <  max_samples:
                ll[label].extend(nll[no][label])
    return lnl,nll,ll

def label_content(data_filepth ="../res/data/已完成标注（6818）.txt"):
    data = tools.read_txt(data_filepth)
    return content_preprocess(data)

def save_label_no_line_result(lnl_res,save_path = "../res/labeled_data/lnline.csv"):
    content = [["label","article_no","line"]]
    for l in lnl_res.keys():
        for n in lnl_res[l].keys():
            for line in lnl_res[l][n]:
                content.append([l,n,line])
    tools.save_txt(save_path,content)

def save_no_label_line_result(nll_res,save_path = "../res/labeled_data/nlline_data.csv"):
    content =[["article_no,label","line"]]
    for n in nll_res.keys():
        for l in nll_res[n].keys():
            for line in nll_res[n][l]:
                content.append([n,l,line])
    tools.save_txt(save_path,content)

def save_label_data(ll_res,save_path = "../res/labeled_data/label_data.csv"):
    content = [["label","line"]]
    for l in ll_res:
        for line in ll_res[l]:
            content.append([l,line])
    tools.save_txt(save_path,content)

def load_labels(filepath="../res/data/关键因子.txt"):
    content = tools.read_txt(filepath)
    labels = []
    for var in content.split("\n"):
        var = var.replace("：","")
        var = var.strip()
        if len(var) >0:
            if " " in var:
                for v in var.split(" "):
                    if len(v.strip()) >0:
                        labels.append(v.strip())
            else:
                labels.append(var)
    return labels

### data_file: 标注文件（nlline_data）
### train_file: 切分后的训练文件保存地址
### test_file: 切分后的测试文件保存地址
### rate: 切分比例（训练数据/总体数据）
### shuffle:是否打乱
def seperate_data_by_instrument(data_file,train_file,test_file,rate = 0.75,shuffle = False):
    content = tools.read_txt(data_file).strip().split("\n")
    content.pop(0)
    data ={}
    id = []
    train_data,test_data=[],[]
    for line in content:
        line = line.split(",",maxsplit=3)
        if line[0] not in data.keys():
            data[line[0]] = []
        data[line[0]].append(line[1:])
        id.append(line[0])
    train_size = int(len(data)*rate)
    test_size = int(len(data)-train_size)
    if shuffle:
        random.shuffle(id)
    for no in id[:train_size]:
        for var in data[no]:
            train_data.append([no]+var)
    for no in id[-test_size:]:
        for var in data[no]:
            test_data.append([no] + var)
    tools.save_txt(train_file,train_data)
    tools.save_txt(test_file,test_data)

### data_file : 标注的文件(lnline.csv)
### train_file: 切分后训练文件的保存地址
### test_file: 切分后测试文件的保存地址
def seperate_data_by_label(data_file,train_file,test_file,rate = 0.75,shuffle = False):
    content = tools.read_txt(data_file).strip().split("\n")
    content.pop(0)
    data = {}
    for line in content:
        line = line.split(",",maxsplit=3)
        label = line[0]
        if label not in data.keys():
            data[label] = []
        data[label].append(line[1:])
    train_data,test_data =[],[]
    for label in data.keys():
        tmp_data = data[label]
        if shuffle:
            random.shuffle(tmp_data)
        train_size = int(len(tmp_data)*rate)
        test_size = int(len(tmp_data)-train_size)
        for var in tmp_data[:train_size]:
            train_data.append([label]+var)
        for var in tmp_data[-test_size:]:
            test_data.append([label]+var)
    if train_file!=None:
        tools.save_txt(train_file,train_data)
    if test_file!=None:
        tools.save_txt(test_file,test_data)
    return train_data,test_data

def test_seperate_label():
    data_file = "../res/labeled_data/label_data.csv"
    train_file = "../res/seperated_data/train_label.csv"
    test_file = "../res/seperated_data/test_label.csv"
    seperate_data_by_label(data_file,train_file,test_file)

def test_seperate_id():
    data_file = "../res/labeled_data/nlline_data.csv"
    train_file = "../res/seperated_data/train_id.csv"
    test_file = "../res/seperated_data/test_id.csv"
    seperate_data_by_instrument(data_file,train_file,test_file)

def transfer_train(train_file,transfer_save_file,skip_first = True):
    fe_size = fe.all_feature_len
    content = tools.read_txt(train_file).strip().split("\n")
    labels= []
    tmp = []
    for i in range(fe_size):
        tmp.append("attr"+str(i))
    tmp.append("class")
    res = [tmp]
    for i in range(len(content)):
        if skip_first and i == 0:
            continue
        tools.show_process(i,len(content),num=10)
        line = content[i]
        line = line.split(",")
        if line[0] not in labels:
            labels.append(line[0])
        features = fe.get_features(line[-1])
        features+=[str(fe.get_label(line[0]))]
        res.append(list(map(str,features)))
    print("train file feature done")
    tools.save_txt(transfer_save_file,res)

def transfer_test(test_file,test_save_file,label_files = "../res/parameter/labels.txt"):
    tmp_labels = tools.read_txt(label_files).strip().split("\n")
    labels =[]
    for line in tmp_labels:
        labels.append(line)
    content = tools.read_txt(test_file).strip().split("\n")
    tmp = []
    fe_size = fe.all_feature_len
    for i in range(fe_size):
        tmp.append("attr"+str(i))
    tmp.append("class")
    res = [tmp]
    for line in content:
        line = line.split(",")
        if line[0] in labels:
            features = fe.get_features(line[-1])
            features+= [str(fe.get_label(line[0]))]
            res.append(list(map(str,features)))
    tools.save_txt(test_save_file,res)

def csv2arff(csv_file,save_path,class_index = -1):
    content = tools.read_lines(csv_file)
    arff_string = "@relation  tmp\n"
    tmp = content[0].strip().split(",")
    for att in tmp[:-1]:
        arff_string+="@attribute "+att+" numeric\n"
    arff_string+= "@attribute class {"

    data = ''.join(content[1:])
    labels = set()
    for i in range(1,len(content)):
        tools.show_process(i,len(content),10)
        labels.add(content[i].split(",")[class_index].strip())

    labels = sorted(list(labels))
    for l in labels:
        arff_string+= l+","
    arff_string = arff_string[:-1]
    arff_string += "}\n @data\n"+data
    tools.save_txt(save_path,arff_string)
    print("csv 2 arff done")

def label_process(filepath = "../res/data/已完成标注（6818）.txt",save_file = "../res/labeled_data/label_data.csv"):
    label_no_line, no_label_line, label_data = label_content(filepath)
    # save_label_no_line_result(label_no_line)
    # save_no_label_line_result(no_label_line)
    save_label_data(label_data,save_file)


def get_sucheng(content):
    sucheng_regex = "\[.{0,2}原告诉称.{0,2}\]"
    common_regex = "\[.{2,8}\]"
    sucheng_index = tools.get_regex_str_index(sucheng_regex,content)
    start = 0
    if  len(sucheng_index)>0:
        start = sucheng_index[0]+content[sucheng_index[0]:].index("]")+1
    end_index = tools.get_regex_str_index(common_regex,content[start:])
    if len(end_index) >0:
        end = start+end_index[0]
    else:
        end = len(content)
    content = content[start:end]
    return content

if __name__ =="__main__":
    label_process()
    # test_seperate_label()
    # test_seperate_id()


    # train_file =  "../res/seperated_data/train_label.csv"
    # test_file =  "../res/seperated_data/test_label.csv"
    # train_save_file ="../res/seperated_data/train_features.csv"
    # test_save_file ="../res/seperated_data/test_features.csv"
    # train_arff_file = "../res/seperated_data/train.arff"
    # test_arff_file = "../res/seperated_data/test.arff"
    # # transfer_train(train_file, train_save_file)
    # # transfer_test(test_file,test_save_file)
    # csv2arff(train_save_file,train_arff_file)
    # csv2arff(test_save_file,test_arff_file)


    # res = label_content()
    # for no in res.keys():
    #     print(no)
    #     for label in res[no].keys():
    #         print(label,"----",'##'.join(res[no][label]))
    #     input()
