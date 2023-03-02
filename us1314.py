##US13 and US14

from time import monotonic, strptime
import datetime
import itertools

def getNameUsingID(individualList, ID):
    for i in individualList:
        if(i[0] == ID):
            return i[1]
    
def plist():
    ilist = [0 for i in range(7)]
    ilist[5] = []
    return ilist

    
def flist():
    flist = [0 for i in range(6)]
    flist[5] = []
    return flist

def lastName(s):
    temp=''
    for i in s:
        if(i != '/'):
            temp += i
    return temp

def currentDate():
    currDate = str(datetime.date.today())
    return currDate

def getBirthDateByID(pdata, id):
    for i in pdata:
        if(i[0] == id):
            return i[3]

def difference_months(dateData1, dateData2):
    temp1 = dateData1.split('-')
    temp2 = dateData2.split('-')
    ndateData1 = datetime.date(int(temp1[0]), int(temp1[1]), int(temp1[2]))
    ndateData2 = datetime.date(int(temp2[0]), int(temp2[1]), int(temp2[2]))
    return int((ndateData1 - ndateData2).days / 30.4)


def difference_days(dateData1, dateData2):
    temp1 = dateData1.split('-')
    temp2 = dateData2.split('-')
    ndateData1 = datetime.date(int(temp1[0]), int(temp1[1]), int(temp1[2]))
    ndateData2 = datetime.date(int(temp2[0]), int(temp2[1]), int(temp2[2]))
    return abs(int((ndateData1 - ndateData2).days))
	        
def convertDateFormat(date):
    temp = date.split()
    if(temp[1] == 'JAN'): temp[1] = '01';
    if(temp[1] == 'FEB'): temp[1] = '02';
    if(temp[1] == 'MAR'): temp[1] = '03';
    if(temp[1] == 'APR'): temp[1] = '04';
    if(temp[1] == 'MAY'): temp[1] = '05';
    if(temp[1] == 'JUN'): temp[1] = '06';
    if(temp[1] == 'JUL'): temp[1] = '07';
    if(temp[1] == 'AUG'): temp[1] = '08';
    if(temp[1] == 'SEP'): temp[1] = '09';
    if(temp[1] == 'OCT'): temp[1] = '10';
    if(temp[1] == 'NOV'): temp[1] = '11';
    if(temp[1] == 'DEC'): temp[1] = '12';
    if(temp[2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']):
        temp[2] = '0' + temp[2]
    return (temp[0] + '-' + temp[1] + '-' + temp[2])

dateList = []
todayDate = currentDate()

def Gparse(file_name):
    f = open(file_name,'r')
    personvalue = 0
    famvalue = 0
    pdata = []
    fdata = []
    inddata = plist()
    famdata = flist()
    for line in f:
        s = line.split()
        if(s != []):
            if(s[0] == '0'):
                if(personvalue == 1):
                    pdata.append(inddata)
                    inddata = plist()
                    personvalue = 0
                if(famvalue == 1):
                    fdata.append(famdata)
                    famdata = flist()
                    famvalue = 0
                if(s[1] in ['NOTE', 'HEAD', 'TRLR']):
                    pass
                else:
                    if(s[2] == 'INDI'):
                        personvalue = 1
                        inddata[0] = (s[1])
                    if(s[2] == 'FAM'):
                        famvalue = 1
                        famdata[0] = (s[1])
            if(s[0] == '1'):
                if(s[1] == 'NAME'):
                    inddata[1] = s[2] + " " + lastName(s[3])
                if(s[1] == 'SEX'):
                    inddata[2] = s[2]
                if(s[1] in ['BIRT', 'DEAT', 'MARR', 'DIV']):
                    date_id = s[1]
                if(s[1] == 'FAMS'):
                    inddata[5].append(s[2])
                if(s[1] == 'FAMC'):
                    inddata[6] = s[2]
                if(s[1] == 'HUSB'):
                    famdata[1] = s[2]
                if(s[1] == 'WIFE'):
                    famdata[2] = s[2]
                if(s[1] == 'CHIL'):
                    famdata[5].append(s[2])
            if(s[0] == '2'):
                if(s[1] == 'DATE'):
                    date = s[4] + " " + s[3] + " " + s[2]
                    if(date_id == 'BIRT'):
                        inddata[3] = convertDateFormat(date)
                    if(date_id == 'DEAT'):
                        inddata[4] = convertDateFormat(date)
                    if(date_id == 'MARR'):
                        famdata[3] = convertDateFormat(date)
                    if(date_id == 'DIV'):
                        famdata[4] = convertDateFormat(date)
    return pdata, fdata

def get_sibling_pairs(family, individuals):
    siblings = family[5]
    if siblings and len(siblings) > 1:
        return list(itertools.combinations(siblings, 2))
    return []

def US13(families, individuals):
    date_list = []
    for family in families:
        for sibling_pair in get_sibling_pairs(family, individuals):
            sibling1_birth = getBirthDateByID(individuals, sibling_pair[0])
            sibling2_birth = getBirthDateByID(individuals, sibling_pair[1])
            siblings_months = abs(difference_months(sibling1_birth, sibling2_birth))
            siblings_days = abs(difference_days(sibling1_birth, sibling2_birth))
            if siblings_months <= 8 and siblings_days >= 3:
                date_list.append(sibling_pair)
                print(f"ERROR: INDIVIDUAL: US13: Siblings {sibling_pair[0]} and {sibling_pair[1]} have their birth dates eight months apart")
            elif siblings_months == 0 and siblings_days >= 2:
                date_list.append(sibling_pair)
                print(f"ERROR: INDIVIDUAL: US13: Siblings {sibling_pair[0]} and {sibling_pair[1]} have their birth days 2 or more days apart")
    if not date_list:
        print("US13: All the siblings have correct spacing")
    else:
        print("ERROR: INDIVIDUAL: US13: The following sibling pairs have bad birth date spacings:")
        print(date_list)

def US14(list_individual,list_family):
    multipleBirthsList = []
    for i in list_family:
        birthList = []
        if(i[5] != [] and len(i[5]) > 5):
            print(i[5])
            for j in i[5]:
                birthList.append(getBirthDateByID(list_individual, j))
            birthListLength = len(birthList)
            birthListSet = set(birthList)
            listsetLength = len(birthListSet)
            m = (birthListLength - listsetLength)
            if( m >= 5):
                multipleBirthsList.append(i[0])
                print("ERROR: FAMILY: US14: The Family with ID " + i[0] + " had more than 5 Births and hence is not valid.")
    print (birthList)
    if(len(multipleBirthsList)!=0):
        print("ERROR: FAMILY: US14: The families mentioned below had more than 5 kids during the time of birth:")
        print(multipleBirthsList)       
    else:
        print("Us14: There are no families with more than 5 kids.")



def Main(file_name):
    pdata, fdata = Gparse(file_name)
    pdata.sort()
    fdata.sort()
    US13(fdata,pdata)
    US14(pdata, fdata)  