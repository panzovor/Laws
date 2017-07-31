__author__ = 'E440'
import src.preprocess as preprocess
import src.tools as tools

def distribution(data_path,label_path,save_path):
    content = tools.read_txt(data_path)
    labels = preprocess.load_labels(label_path)
    label_no_line,no_label_line,label_line =  preprocess.__label_content(content,labels)
    save_content =[["label","num"]]
    for label in label_line.keys():
        save_content.append([label[1:-4],str(len(label_line[label]))])

    tools.save_txt(save_path,save_content)



if __name__ == "__main__":
    data_path = "../res/data/已完成标注（6818）.txt"
    label_path = "../res/data/关键因子.txt"
    save_path = "../res/analysis_result/label_sample_num.csv"

    distribution(data_path,label_path,save_path)