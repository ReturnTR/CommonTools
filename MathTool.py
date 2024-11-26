def FTF2PRF(FP,TP,FN):
    if TP==0:return 0,0,0
    P = TP / (TP + FP)
    R = TP / (TP + FN)
    F = 2 * P * R / (P + R)
    return P,R,F



def PGR2PRF(gold,predict,right):
    if right==0:return 0,0,0
    P=right/gold
    R=right/predict

    F=2 * P * R / (P + R)
    return P,R,F

def cal_auc(labels, predictions):
    # 排序预测值和标签，按预测值降序排列
    sorted_pairs = sorted(zip(predictions, labels), key=lambda x: x[0], reverse=True)
    predictions, labels = zip(*sorted_pairs)
    
    # 计算真阳性（TP）、假阳性（FP）、真阴性（TN）、假阴性（FN）
    TP = 0
    FP = 0
    prev_TP = 0
    prev_FP = 0
    total_positive = sum(labels)
    total_negative = len(labels) - total_positive
    
    # 用于计算AUC的变量
    auc = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            TP += 1
        else:
            FP += 1
        # 计算当前的TPR和FPR
        TPR = TP / total_positive
        FPR = FP / total_negative
        # 使用梯形法则计算面积
        auc += (FPR - prev_FP / total_negative) * (TPR + prev_TP / total_positive) / 2
        prev_TP = TP
        prev_FP = FP
    
    return auc
