__author__ = 'E440'

encoding ="utf-8"
def read_txt(filepath,encoding= "utf-8"):
    with open(filepath,mode="r",encoding=encoding) as file:
        content = file.read()
    return content

def save_txt(filepath,content, encoding= encoding,split =","):
    with open(filepath,mode="w",encoding=encoding) as file:
        if isinstance(content,str):
            file.write(content)
        elif isinstance(content,list):
            for line in content:
                if isinstance(line,list):
                    file.write(split.join(line)+"\n")
                else:
                    file.write(line)


