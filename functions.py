import pandas as pd
import re
import os

def sum_of_list(l):
    total = 0
    for val in l:
        if type(val)== int or type(val)== float:
            total = total + val
        else:
            try:
                total = total + int(val)
            except Exception:
                pass
                
    return total


def find_keywords(csv, colum, dir_file):
    s = set()
    df = pd.read_csv(csv)
    for i in df[colum].values:
        if type(i)== str:
            x = re.findall(r"[\w']+", i)
            for item in x:
                s.add(item)
        else:
            print(i)
        with open(dir_file, 'w') as f:
            for line in s:
                f.write(line)
                f.write('\n')

def find_keywords_sep(csv, colum):
    s = set()
    df = pd.read_csv(csv)
    dir_file = "/".join(csv.split("/")[:-1])
    for i in df[colum].values:
        if type(i)== str:
            x = re.findall(r"[\w']+", i)
            for item in x:
                if len(item) > 2:
                    s.add(item)
                    
    newpath = (dir_file +"/" + "keywords")
    if not os.path.exists(newpath):
            os.makedirs(newpath)
    
    for line in s:
        with open(newpath +"/"+line + ".txt", 'w') as f:
            f.write(line)
            f.write('\n')


def count(b, themes,df,colum):
    l= []
    try:
        a = df[colum]
    except Exception:
        print("wrong cloumn name")
    ind_value=[]
    for i in range(len(b)):
        ind_value.append([])
    name= []
    i = 0
    #print(b)
    for k in b:
        i = 0
        #print(k)
        
       

        while i < len(df):
            
            x = df[k].values[i]
            #if i == 1:
                #print(x)
                
            
            
            #print(len(themes))
            if type(df[colum].values[i]) == str:
                if len([ele for ele in themes if(ele in df[colum].values[i])]) > 0 and len([ele for ele in themes if(ele in df[colum].values[i])][0])>0:
                    if type(x)== int:
                        l[themes.index(f)] = l[themes.index(f)] + x
                    ind_value[b.index(k)].append(x)
                    if b.index(k) == 0:
                        name.append(df[colum].values[i])
        #else:
            #print(df2["Video title"].values[i])
            #print(i)       
            i = i+1
    #print(ind_value)

    return(l, ind_value, name)
            






throw = ["and", "And", "the", "The", "with", "With", "for", "For" , "You", "get", "Get"]


def make_themes(lis):
    #themes = []
    x = []
    try:
        with open(lis) as f:
            lines = f.read()

            y = lines.split("\n")
            for i in y:
                if i not in throw:
                    if len(i)>2:
                        x.append(i)
            #themes.append(x)
    except Exception:
        print("search_term file not found or in wrong format\ncheck if file is a .txt file and has one search term per line")
    return(x)



def search_themes( df,list_files, colum, b):
    themes = make_themes(list_files)
    x, y , z = count(b, themes,df, colum)
    return(x, y , z)


def search(search_list,csv_file, colum,save_file):
    try:
        df_org = pd.read_csv(csv_file)
    except Exception:
        print("csv directory not found\ncheck if it is the correct directory path and speeled corectly")
        return -1

    dir_org = "/".join(csv_file.split("/")[:-1])
    values = list(df_org.columns)
    try:
        x = search_themes(df_org, search_list, colum, values)
    except Exception:
        return -1
    df = pd.DataFrame(({'video tital' : x[2]}))
    #print(len(x[2]))
    for i in range(len(x[1])):
        if values[i] != colum:
        #print(len(x[1][i]))
            df[values[i]] = x[1][i]
    df.to_csv(dir_org +"/" + save_file)
    #print("Done")
    
    return(df)


def search_nosave( search_list,csv_file, colum):
    df_org = pd.read_csv(csv_file)
    values = list(df_org.columns)
    x = search_themes(df_org, search_list, colum, values)
    df = pd.DataFrame(({'video tital' : x[2]}))
    #print(len(x[2]))
    for i in range(len(x[1])):
        if values[i] != colum:
        #print(len(x[1][i]))
            df[values[i]] = x[1][i]
    #df.to_csv(save_file)
    #print("Done")
    return(df)



def themes(csv_file,colum,save_file):
    dir_org = "/".join(csv_file.split("/")[:-1])
    find_keywords_sep(csv_file, colum)
    number = []
    name = []
    header= [] 
    df_og = pd.read_csv(csv_file)
    for item in range(len(list(df_og.columns))):
        header.append([])
    #print(len(header))
    #print(list(df_og.columns))
    counter = 0
    find_keywords_sep(csv_file, colum)
    for i in os.listdir(dir_org + "/" + "keywords"):
        df = search_nosave(dir_org + "/" + "keywords/" + i, csv_file , colum)
        columns =[]
        number.append(len(df))
        name.append(i.split(".")[0])
        #print(len(list(df.columns)))
        #print(list(df.columns))
        for k in range(len(list(df.columns))):
            if "%" in list(df.columns)[k]:
                try:

                    header[k].append(sum_of_list(df[list(df.columns)[k]].values)/len(df[list(df.columns)[k]].values))
                    columns.append(list(df.columns)[k])
                except Exception:
                    pass
            else:
                try:
                    header[k].append(sum_of_list(df[list(df.columns)[k]].values))
                    columns.append(list(df.columns)[k])
                except Exception:
                    pass
            
        counter = counter +1
        if (counter % 10)==0 :
            print(str(counter) + "/" + str(len(os.listdir(dir_org + "/" + "keywords"))))           
   
    df2 = pd.DataFrame(({'key word' : name,'number of videos' : number}))
    for q in range(len(columns)):
        if sum(header[q]) != 0:
            df2[columns[q]] = header[q]
    df2.to_csv(dir_org +"/" + save_file)
    return(df2)
