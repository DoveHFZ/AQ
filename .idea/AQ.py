import copy
#算法中设置参数
SOLNumber = 2
CONSNumber = 2
StarM = 2
#优化标准为（正例数/反例数）
def select_example(unacc_number,acc_number,good_number,v_good_number):
    file = open("examples.txt")
    file_output = open("exampleshort.txt", 'w')
    #total_number = unacc_number+acc_number+good_number+v_good_number
    unacc_number_count = 0
    acc_number_count = 0
    good_number_count = 0
    v_good_number_count = 0
    while unacc_number_count < unacc_number or acc_number_count < acc_number or good_number_count < good_number or v_good_number_count < v_good_number:              #从大例子集中读出若干条数据，写入exampleshort.txt
        line = file.readline();
        if 'unacc' in line and unacc_number_count < unacc_number:
            file_output.write(line)
            unacc_number_count += 1
        elif 'unacc' not in line and 'acc' in line and acc_number_count < acc_number:
            file_output.write(line)
            acc_number_count += 1
        elif 'vgood' in line and v_good_number_count < v_good_number:
            file_output.write(line)
            v_good_number_count +=1
        elif 'vgood' not in line and 'good' in line and good_number_count < good_number:
            file_output.write(line)
            good_number_count += 1
    file.close()
    file_output.close()

def sort_partial_star(seed,PE,NE):          #Induce得第一步，将选择子进行排序
    dictPE_number = {
        'buying': 0,
        'maint': 0,
        'doors': 0,
        'person': 0,
        'lug_boot': 0,
        'safety': 0}
    dictNE_number = {
        'buying': 0,
        'maint': 0,
        'doors': 0,
        'person': 0,
        'lug_boot': 0,
        'safety': 0
    }

    for key,value in seed.items():      #计算各个选择子对应得正反例得个数
        for example in PE:
            if example.get(key) == value:
                dictPE_number[key] = dictPE_number.get(key) + 1

    for key,value in seed.items():
        #print(key, value)
        for example in NE:
            if example.get(key) == value:
                dictNE_number[key] = dictNE_number.get(key) + 1
    #print(dictPE_number)
    #print(dictNE_number)
    sorted_attribute_list = ['buying','maint','doors','person','lug_boot','safety']
    PE_divide_NE_list = []                  #正反例比值
    PE_and_NE_number_list = []              #正反例个数
    for key,value in dictPE_number.items():
        every_attribute = []
        every_attribute.append(dictPE_number.get(key))
        every_attribute.append(dictNE_number.get(key))
        PE_and_NE_number_list.append(every_attribute)
        if dictNE_number.get(key) == 0:
            PE_divide_NE_list.append(value/0.1)
        else:
            PE_divide_NE_list.append(value/dictNE_number.get(key))
    for i in range(0,len(sorted_attribute_list)):               #对选择子进行排序
        for j in range(i+1,len(sorted_attribute_list)):
            if PE_divide_NE_list[j] > PE_divide_NE_list[i]:
                temp = PE_divide_NE_list[i]
                PE_divide_NE_list[i] = PE_divide_NE_list[j]
                PE_divide_NE_list[j] = temp

                temp = sorted_attribute_list[i]
                sorted_attribute_list[i] = sorted_attribute_list[j]
                sorted_attribute_list[j] = temp

                temp = PE_and_NE_number_list[i]
                PE_and_NE_number_list[i] = PE_and_NE_number_list[j]
                PE_and_NE_number_list[j] = temp
    return sorted_attribute_list,PE_and_NE_number_list

def formula_list_sort(formula_list,seed,PE,NE):     #对公式进行排序
    PE_and_NE_number_list = []
    for i in range(0,len(formula_list)):
        PE_number = 0;
        NE_number = 0;

        for example in PE:
            count = 0;
            for j in range(0,len(formula_list[i])):
                if example.get(formula_list[i][j]) == seed.get(formula_list[i][j]):         #若PE中得正例得某一属性值能和公式中某一属性值相等
                    count += 1
            if count == len(formula_list[i]):
                PE_number += 1

        for example in NE:
            count = 0
            for k in range(0,len(formula_list[i])):
                if example.get(formula_list[i][k]) == seed.get(formula_list[i][k]):         #若PE中得正例得某一属性值能和公式中某一属性值相等
                    count += 1
            if count == len(formula_list[i]):
                NE_number += 1

        number_list = []
        number_list.append(PE_number)
        number_list.append(NE_number)
        PE_and_NE_number_list.append(number_list)       #获得每一个公式对应得正例和反例数

    PE_divide_NE_list = []      #正反例比值
    for i in range(0,len(formula_list)):
        if PE_and_NE_number_list[i][1] == 0:
            PE_divide_NE_list.append(PE_and_NE_number_list[i][0]/0.1)
        else:
            PE_divide_NE_list.append(PE_and_NE_number_list[i][0]/PE_and_NE_number_list[i][1])
    for i in range(0,len(formula_list)):
        for j in range(i+1,len(formula_list)):
            if PE_divide_NE_list[j] > PE_divide_NE_list[i]: #比较正例数和反例数得比值
                temp = PE_divide_NE_list[i]
                PE_divide_NE_list[i] = PE_divide_NE_list[j]
                PE_divide_NE_list[j] = temp

                temp = formula_list[i]
                formula_list[i] = formula_list[j]
                formula_list[j] = temp

                temp = PE_and_NE_number_list[i]
                PE_and_NE_number_list[i] = PE_and_NE_number_list[j]
                PE_and_NE_number_list[j] = temp
            elif PE_divide_NE_list[j] == PE_divide_NE_list[i] and len(formula_list[j]) < len(formula_list[i]):    #如果正例数和反例数比值相等，比较公式得长度，长度小得在前面
                temp = PE_divide_NE_list[i]
                PE_divide_NE_list[i] = PE_divide_NE_list[j]
                PE_divide_NE_list[j] = temp

                temp = formula_list[i]
                formula_list[i] = formula_list[j]
                formula_list[j] = temp

                temp = PE_and_NE_number_list[i]
                PE_and_NE_number_list[i] = PE_and_NE_number_list[j]
                PE_and_NE_number_list[j] = temp

    return formula_list,PE_and_NE_number_list

def general_formula(sorted_formula_list,sorted_formula_list_temp,example,PE,NE):     #泛化公式，返回排序结果
    formula_list = []
    for i in range(0,len(sorted_formula_list)):     #只是属性列表
        for j in range(i+1,len(sorted_formula_list_temp)):
            temp = copy.deepcopy(sorted_formula_list[i])
            temp.append(sorted_formula_list_temp[j])
            formula_list.append(temp)
    formula_list_sorted_temp,PE_and_NE_number_list_temp = formula_list_sort(formula_list,example,PE,NE)
    return formula_list_sorted_temp,PE_and_NE_number_list_temp

def Induce(example,PE,NE):      #生成star(e|NE,m)
    solution_list = []
    consistent_list = []
    sortedPS = []
    sortedPS_temp, PE_and_NE_number_list = sort_partial_star(example,PE,NE)     #按优化标准排序
    #print("选择子排序部分")
    #print(sortedPS_temp)
    #print(PE_and_NE_number_list)
    for i in range(0,len(sortedPS_temp)):   #从PS中保留m个选择符
        temp = []
        if i < 2:
            temp.append(sortedPS_temp[i])
            sortedPS.append(temp)

    #Induce得循环从这里开始
    while 1:#完备性和一致性检查
        for i in range(0,len(sortedPS)):
            if(PE_and_NE_number_list[i][0] == len(PE) and PE_and_NE_number_list[i][1] == 0):    #完备且一致
                solution_list.append(sortedPS[i])
            elif(PE_and_NE_number_list[i][0] < len(PE) and PE_and_NE_number_list[i][1] == 0):   #不完备但一致
                consistent_list.append(sortedPS[i])
            else:continue
        #print("完备性和一致性检查")
        #print(consistent_list)
        #print(solution_list)

        if(len(solution_list) >= SOLNumber or len(consistent_list) >= CONSNumber):#如果consistency或solution大小大于等于m，选取最优得m个公式，并返回
            #按照优化标准排序
            mergelist = copy.deepcopy(consistent_list)
            for i in range(0,len(solution_list)):
                mergelist.append(solution_list[i])
            #print("完备性和一致性部分")
            #print(mergelist)
            sortedPS_temp, PE_and_NE_number_list = formula_list_sort(mergelist,example,PE,NE)
            #按照优化标准对列表进行排序，并返回前m个公式
            #print(sortedPS_temp)
            #print(PE_and_NE_number_list)
            return sortedPS_temp[0:StarM],PE_and_NE_number_list[0:StarM]
        else: #特化公式并排序
            sortedPS,PE_and_NE_number_list = general_formula(sortedPS,sortedPS_temp,example,PE,NE)
            #选出前m个最优得公式

            '''print("特化公式部分")
            print(sortedPS)
            print(PE_and_NE_number_list)'''

def optimal_formula_cover_PE(seek,PE,formula):
    PE_temp = []
    for example in PE:
        count = 0
        for j in range(0,len(formula)):
            if example.get(formula[j]) == seek.get(formula[j]):
                count += 1
        if count != len(formula):
            PE_temp.append(example)
    return PE_temp

#主程序
PE = []     #正例unacc
NE = []     #反例其他
#select_example(10,3,3,3)     #  从例子集中选出一部分例子
file = open("examples.txt")
while 1:        #分出正反例
    line = file.readline().strip('\n')
    if not line:
        break
    linelist = line.split(',')
    if linelist[-1] == 'unacc':
        del linelist[-1]
        dict = {'buying':' ',
                'maint':' ',
                'doors':' ',
                'person':' ',
                'lug_boot':' ',
                'safety':' '}
        dict['buying'] = linelist[0]
        dict['maint'] = linelist[1]
        dict['doors'] = linelist[2]
        dict['person'] = linelist[3]
        dict['lug_boot'] = linelist[4]
        dict['safety'] = linelist[5]
        PE.append(dict)
    else:
        del linelist[-1]
        dict = {'buying': "",
                'maint': "",
                'doors': "",
                'person': "",
                'lug_boot': "",
                'safety': ""}
        dict['buying'] = linelist[0]
        dict['maint'] = linelist[1]
        dict['doors'] = linelist[2]
        dict['person'] = linelist[3]
        dict['lug_boot'] = linelist[4]
        dict['safety'] = linelist[5]
        NE.append(dict)
file.close()
final_formula_list = []
#从正例中选出一个例子，默认选第一个，生成相对于反例集NE的star约束
while len(PE) > 0:
    m_formula_list,m_PE_and_NE_number_list = Induce(PE[0],PE,NE)
    #print("主程序部分")
    #print(m_formula_list)
    #print(m_PE_and_NE_number_list)
    # 从m_formula_list中挑出最好得公式
    # 由于在公式排序的过程中已经考虑到了  覆盖正反例得比值和公式得长度  所以返回公式列表得第一个公式就是最优得
    optimal_formula = m_formula_list[0]
    #最优公式加入final_formula_list
    optimal_formula_temp = []
    for i in range(0,len(optimal_formula)):
        optimal_formula_temp.append(optimal_formula[i]+' = '+PE[0].get(optimal_formula[i]))
    final_formula_list.append(optimal_formula_temp)

    PE = optimal_formula_cover_PE(PE[0],PE,optimal_formula)         #去除被optimal_formula覆盖得正例
#输出最终得公式析取
for i in range(0,len(final_formula_list)):
    for j in range(0,len(final_formula_list[i])):
        print('['+final_formula_list[i][j]+']',end='')
    if i != len(final_formula_list)-1:
        print('V',end='')

