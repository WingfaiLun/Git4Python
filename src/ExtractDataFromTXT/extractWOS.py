#!/usr/bin/python
from collections import OrderedDict
from pyexcel_xls import save_data
import re

path = r"E:\Users\lockon\Desktop\\"
txtFileName = r"WOS2.txt"
ouputFileName = r"WOS2.xls"

#以utf-8编码读取源文件的所有字节
def getArticles():
    f = open(path + txtFileName, 'r', encoding='utf-8').read()
    regexArticle = re.compile(r'\nPT[\s\S]*?\nER')
    #articles就是所有文章的集合
    articles = re.findall(regexArticle, f)
    return articles
    
#定义保存成xls文件的方法，最后遍历完成后调用
def saveOuput():
    save_data(path + ouputFileName, xls_data)  

#初始化excel的数据
xls_data = OrderedDict()
sheet1 = [["PT", "AU", "AF", "CA", "TI", "SO", "LA", "DT", "ID", "AB", "C1(1)", "C1(2)", "RP", "EM", "RI", "OI", "FU", "FX", "NR", "TC", "Z9", "U1", "U2", "PU", "PI", "PA", "SN", "EI", "J9", "JI", "PD", "PY", "VL", "IS", "BP", "EP", "DI", "PG", "WC", "SC", "GA", "UT", "PM"]]

articles = getArticles()
#遍历所有文章的集合，一个个处理
for article in articles:
    row_data = []
    
    pt = ''
    au = ''
    af = ''
    ca = ''
    ti = ''
    so = ''
    la = ''
    dt = ''
    iD = ''
    ab = ''
    c11 = ''
    c12 = ''
    rp = ''
    em = ''
    ri = ''
    oi = ''
    fu = ''
    fx = ''
    nr = ''
    tc = ''
    z9 = ''
    u1 = ''
    u2 = ''
    pu = ''
    pi = ''
    pa = ''
    sn = ''
    ei = ''
    j9 = ''
    ji = ''
    pd = ''
    py = ''
    vl = ''
    iS = ''
    bp = ''
    ep = ''
    di = ''
    pg = ''
    wc = ''
    sc = ''
    ga = ''
    ut = ''
    pm = ''
    
    ptLabel = 'PT '
    auLabel = 'AU '
    afLabel = 'AF '
    caLabel = 'CA '
    tiLabel = 'TI '
    soLabel = 'SO '
    laLabel = 'LA '
    dtLabel = 'DT '
    iDLabel = 'ID '
    abLabel = 'AB '
    c1Label = 'C1 '
    rpLabel = 'RP '
    emLabel = 'EM '
    riLabel = 'RI '
    oiLabel = 'OI '
    fuLabel = 'FU '
    fxLabel = 'FX '
    nrLabel = 'NR '
    tcLabel = 'TC '
    z9Label = 'Z9 '
    u1Label = 'U1 '
    u2Label = 'U2 '
    puLabel = 'PU '
    piLabel = 'PI '
    paLabel = 'PA '
    snLabel = 'SN '
    eiLabel = 'EI '
    j9Label = 'J9 '
    jiLabel = 'JI '
    pdLabel = 'PD '
    pyLabel = 'PY '
    vlLabel = 'VL '
    iSLabel = 'IS '
    bpLabel = 'BP '
    epLabel = 'EP '
    diLabel = 'DI '
    pgLabel = 'PG '
    wcLabel = 'WC '
    scLabel = 'SC '
    gaLabel = 'GA '
    utLabel = 'UT '
    pmLabel = 'PM '
    currentIndex = ''
    semicolon = " ; "
    
    articleLines = article.split('\n')
    for line in articleLines:
        lineIndex = line[0:3]
        lineContent = line[3:]
        if re.match(ptLabel, lineIndex):
            currentIndex = ptLabel
            pt = lineContent
        elif re.match(auLabel, lineIndex):
            currentIndex = auLabel
            au = lineContent + semicolon
        elif re.match(afLabel, lineIndex):
            currentIndex = afLabel
            af = lineContent + semicolon
        elif re.match(caLabel, lineIndex):
            currentIndex = caLabel
            ca = lineContent + semicolon
        elif re.match(tiLabel, lineIndex):
            currentIndex = tiLabel
            ti = lineContent
        elif re.match(soLabel, lineIndex):
            currentIndex = soLabel
            so = lineContent
        elif re.match(laLabel, lineIndex):
            currentIndex = laLabel
            la = lineContent
        elif re.match(dtLabel, lineIndex):
            currentIndex = dtLabel
            dt = lineContent
        elif re.match(iDLabel, lineIndex):
            currentIndex = iDLabel
            iD = lineContent
        elif re.match(abLabel, lineIndex):
            currentIndex = abLabel
            ab = lineContent
        elif re.match(c1Label, lineIndex):
            currentIndex = c1Label
            c11 = lineContent
        elif re.match(rpLabel, lineIndex):
            currentIndex = rpLabel
            rp = lineContent
        elif re.match(emLabel, lineIndex):
            currentIndex = emLabel
            em = lineContent
        elif re.match(riLabel, lineIndex):
            currentIndex = riLabel
            ri = lineContent
        elif re.match(oiLabel, lineIndex):
            currentIndex = oiLabel
            oi = lineContent
        elif re.match(fuLabel, lineIndex):
            currentIndex = fuLabel
            fu = lineContent
        elif re.match(fxLabel, lineIndex):
            currentIndex = fxLabel
            fx = lineContent
        elif re.match(nrLabel, lineIndex):
            currentIndex = nrLabel
            nr = lineContent
        elif re.match(tcLabel, lineIndex):
            currentIndex = tcLabel
            tc = lineContent
        elif re.match(z9Label, lineIndex):
            currentIndex = z9Label
            z9 = lineContent
        elif re.match(u1Label, lineIndex):
            currentIndex = u1Label
            u1 = lineContent
        elif re.match(u2Label, lineIndex):
            currentIndex = u2Label
            u2 = lineContent
        elif re.match(puLabel, lineIndex):
            currentIndex = puLabel
            pu = lineContent
        elif re.match(piLabel, lineIndex):
            currentIndex = piLabel
            pi = lineContent
        elif re.match(paLabel, lineIndex):
            currentIndex = paLabel
            pa = lineContent
        elif re.match(snLabel, lineIndex):
            currentIndex = snLabel
            sn = lineContent
        elif re.match(eiLabel, lineIndex):
            currentIndex = eiLabel
            ei = lineContent
        elif re.match(j9Label, lineIndex):
            currentIndex = j9Label
            j9 = lineContent    
        elif re.match(jiLabel, lineIndex):
            currentIndex = jiLabel
            ji = lineContent
        elif re.match(pdLabel, lineIndex):
            currentIndex = pdLabel
            pd = lineContent
        elif re.match(pyLabel, lineIndex):
            currentIndex = pyLabel
            py = lineContent
        elif re.match(vlLabel, lineIndex):
            currentIndex = vlLabel
            vl = lineContent           
        elif re.match(iSLabel, lineIndex):
            currentIndex = iSLabel
            iS = lineContent          
        elif re.match(bpLabel, lineIndex):
            currentIndex = bpLabel
            bp = lineContent          
        elif re.match(epLabel, lineIndex):
            currentIndex = epLabel
            ep = lineContent
        elif re.match(diLabel, lineIndex):
            currentIndex = diLabel
            di = lineContent
        elif re.match(pgLabel, lineIndex):
            currentIndex = pgLabel
            pg = lineContent
        elif re.match(wcLabel, lineIndex):
            currentIndex = wcLabel
            wc = lineContent           
        elif re.match(scLabel, lineIndex):
            currentIndex = scLabel
            sc = lineContent
        elif re.match(gaLabel, lineIndex):
            currentIndex = gaLabel
            ga = lineContent          
        elif re.match(utLabel, lineIndex):
            currentIndex = utLabel
            ut = lineContent
        elif re.match(pmLabel, lineIndex):
            currentIndex = pmLabel
            pm = lineContent           
        elif re.match(r'   ', lineIndex):
            if currentIndex == ptLabel:
                pt += lineContent + semicolon
            if currentIndex == auLabel:
                au += lineContent + semicolon
            elif currentIndex == afLabel:
                af += lineContent + semicolon
            elif currentIndex == caLabel:
                ca += lineContent + semicolon
            elif currentIndex == tiLabel:
                ti += " " + lineContent
            elif currentIndex == soLabel:
                so += semicolon + lineContent
            elif currentIndex == laLabel:
                la += semicolon + lineContent
#             elif currentIndex == dtLabel:
#                 dt += semicolon + lineContent   
            elif currentIndex == iDLabel:
                iD += " " + lineContent
            elif currentIndex == abLabel:
                ab += "\n" + lineContent
            elif currentIndex == c1Label:
                if len(c11 + " / " + lineContent) < 32767:
                    c11 += " / " + lineContent
                else:
                    if len(c12) > 0:
                        c12 += " / " + lineContent
                    else:
                        c12 = lineContent
            elif currentIndex == rpLabel:
                rp += " / " + lineContent
            elif currentIndex == emLabel:
                em += " / " + lineContent
            elif currentIndex == riLabel:
                ri += " " + lineContent
            elif currentIndex == oiLabel:
                oi += " " + lineContent
            elif currentIndex == fuLabel:
                fu += " " + lineContent
            elif currentIndex == fxLabel:
                fx += " " + lineContent
    row_data = [pt, au, af, ca, ti, so, la, dt, iD, ab, c11, c12, rp, em, ri, oi, fu, fx, nr, tc, z9, u1, u2, pu, pi, pa, sn, ei, j9, ji, pd, py, vl, iS, bp, ep, di, pg, wc, sc, ga, ut, pm]
    sheet1.append(row_data)
xls_data.update({u"Result": sheet1})

saveOuput()