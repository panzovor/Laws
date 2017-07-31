__author__ = 'E440'
import jieba
import src.tools as tools
import re

### input:
###     content(str): original content
### output:
###     result(map): label->no-> lines
###     result_no_label(map): no-> label -> lines
###     label_data: label->lines
def __label_content(content,labels):
    labeled_data = {}
    result = {}
    result_no_label ={}
    instrument_regex = "【--\d{1,6}--】"
    sentence_label_regex = []
    asseys = [var.strip() for var in re.split(instrument_regex,content) if len(var.strip())>0]
    asseys_no = re.findall(instrument_regex,content)

    for label in labels:
        tmp ="【"+label+".*?】"
        sentence_label_regex.append(tmp)

    for lregex in sentence_label_regex:
        if lregex not in result.keys():
            result[lregex] ={}
        if lregex not in labeled_data.keys():
            labeled_data[lregex] = []
        for i in range(len(asseys_no)):
            no = asseys_no[i]
            ass_con = asseys[i]

            if no not in result_no_label.keys():
                result_no_label[no]={}
            if lregex not in result_no_label[no].keys():
                result_no_label[no][lregex]= []


            if no not in result[lregex].keys():
                result[lregex][no] = []
            fres = re.findall(lregex,ass_con)
            if len(fres) >0:
                result[lregex][no].extend(list(fres))
                result_no_label[no][lregex].extend(list(fres))
                labeled_data[lregex].extend(list(fres))
    return result,result_no_label,labeled_data

def label_content(data_filepth ="../res/data/已完成标注（6818）.txt",label_filepath="../res/data/关键因子.txt"):
    data = tools.read_txt(data_filepth)
    labels = load_labels(label_filepath)
    # print('\n'.join(labels))
    return __label_content(data,labels)



def save_label_no_line_result(lnl_res,save_path = "../res/labeled_data/lnline.txt"):
    content = []
    for l in lnl_res.keys():
        for n in lnl_res[l].keys():
            for line in lnl_res[l][n]:
                tl =l
                tn = n
                tl = l[1:-4]
                tn = n[3:-3]
                line = line[2+len(tl):-1]
                content.append([tl,tn,line])
    tools.save_txt(save_path,content)

def save_no_label_line_result(nll_res,save_path = "../res/labeled_data/nlline_data.txt"):
    content =[]
    for n in nll_res.keys():
        for l in nll_res[n].keys():
            for line in nll_res[n][l]:
                tl =l
                tn = n
                tl = l[1:-4]
                tn = n[3:-3]
                line = line[2+len(tl):-1]
                content.append([tn,tl,line])
    tools.save_txt(save_path,content)

def save_label_data(ll_res,save_path = "../res/labeled_data/label_data.txt"):
    content = []
    for l in ll_res:
        for line in ll_res[l]:
            tl = l
            tl = l[1:-4]
            line = line[2+len(tl):-1]
            content.append([tl,line])
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


if __name__ =="__main__":
    label_no_line,no_label_line,label_data = label_content()
    save_label_no_line_result(label_no_line)
    save_no_label_line_result(no_label_line)
    save_label_data(label_data)