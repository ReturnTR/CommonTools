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