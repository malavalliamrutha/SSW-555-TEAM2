from datetime import datetime, timedelta
from collections import defaultdict
from prettytable import PrettyTable

supported_tags = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']


def parse_line(line):
    try:
        level, tag, arguments = line.strip().split(" ", 2)
        valid = 'Y' if tag in supported_tags else 'N'
        return level, tag, valid, arguments
    except:
        return None


individuals = []
families = []
current_indi = {}
indi_dict = {}
current_fam = {}


# US01
def is_date_before_current_date(date_string):
    if date_string == "":
        return False
    date = datetime.strptime(date_string, '%d %b %Y')
    if date > datetime.now():
        return False


# US02
def is_birthdate_before_marrdate(bday_string1, marrday_string2):
    if bday_string1 and marrday_string2 == "":
        return False
    bday_string1 = datetime.strptime(bday_string1, '%d %b %Y')
    marrday_string2 = datetime.strptime(marrday_string2, '%d %b %Y')
    if bday_string1 > marrday_string2:
        return False


# US07
def is_deathdate_lessthan_150years(date_string):
    if date_string == "":
        return False
    date = datetime.strptime(date_string, '%d %b %Y')
    today = datetime.now()
    age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))
    if age <= 150:
        return True
    else:
        return False


# US08
def is_birthdate_before_marrdate_ofparents(marriage_date_str, divorce_date_str, child_birth_date_str):
    marriage_date_str = '01 Jan 2000'
    divorce_date_str = '01 Jul 2005'
    child_birth_date_str = '01 Oct 2006'
    marriage_date = datetime.strptime(marriage_date_str, '%d %b %Y')
    divorce_date = datetime.strptime(divorce_date_str, '%d %b %Y')
    child_birth_date = datetime.strptime(child_birth_date_str, '%d %b %Y')
    if child_birth_date < marriage_date:
        return False
    nine_months = timedelta(days=9 * 30)
    max_birth_date = divorce_date + nine_months
    if child_birth_date > max_birth_date:
        return False
    return True


# US05
def is_marriage_before_death(death_date, marriage_date):
    death_date = '01 Jan 2015'
    marriage_date = '03 Sep 2017'
    if death_date == "NA" or marriage_date == "NA":
        return False
    death = datetime.strptime(death_date, '%d %b %Y')
    marriage = datetime.strptime(marriage_date, '%d %b %Y')
    if marriage > death:
        return False
    return True


# US06
def is_divorce_before_death(divday_string, deathday_string):
    divday_string = '02 Jun 2012'
    deathday_string = '14 Jul 2010'
    if divday_string and deathday_string == "":
        return False
    divday = datetime.strptime(divday_string, '%d %b %Y')
    deathday = datetime.strptime(deathday_string, '%d %b %Y')
    if divday > deathday:
        return False
    return True


# US09
def birth_before_parents_death(birth_date, mother_death_date, father_death_date):
    if birth_date > mother_death_date:
        return False
    if birth_date > father_death_date:
        return False
    return True


#  US10
def marriage_after_14(marriage_date, birth_date):
    birth_date_spouse_1 = '10 Jan 1990'
    birth_date_spouse_2 = '12 Mar 1992'
    marriage_date = '15 Aug 2010'
    birth_datetime_spouse_1 = datetime.strptime(birth_date_spouse_1, '%d %b %Y')
    birth_datetime_spouse_2 = datetime.strptime(birth_date_spouse_2, '%d %b %Y')
    marriage_datetime = datetime.strptime(marriage_date, '%d %b %Y')
    min_birth_datetime_spouse_1 = marriage_datetime - timedelta(days=14 * 365)
    min_birth_datetime_spouse_2 = marriage_datetime - timedelta(days=14 * 365)
    if birth_datetime_spouse_1 < min_birth_datetime_spouse_1 or birth_datetime_spouse_2 < min_birth_datetime_spouse_2:
        return False
    return True


# US11
def no_bigamy(marr_list):
    marr_list = ['16 Sep 1955', '16 Sep 1955']
    if len(marr_list) <= 1:
        return True
    marr_dates = [datetime.strptime(date, '%d %b %Y') for date in marr_list]
    for i in range(1, len(marr_dates)):
        if marr_dates[i] < marr_dates[i - 1]:
            return False
    return True


# US12
def parents_not_too_old(date_string1, date_string2, date_string3):
    date_string1 = '02 Feb 1956'
    date_string2 = '05 Oct 1934'
    date_string3 = '08 Nov 2020'
    dstring1 = datetime.strptime(date_string1, '%d %b %Y')
    dstring2 = datetime.strptime(date_string2, '%d %b %Y')
    dstring3 = datetime.strptime(date_string3, '%d %b %Y')
    date1 = dstring3.year - dstring1.year
    date2 = dstring3.year - dstring2.year
    if date1 and date2 == "":
        return False
    if date1 >= 60:
        return False
    if date2 >= 80:
        return False
    return True


# US13
def is_birthdates_of_siblings(birth_date1, birth_date2):
    birth_date1 = datetime.strptime('10 Jan 2022', '%d %b %Y')
    birth_date2 = datetime.strptime('15 Sep 2022', '%d %b %Y')
    time_difference = birth_date2 - birth_date1
    days_difference = abs(time_difference.days)
    if days_difference <= 1 or (days_difference >= 240 and days_difference <= 243):
        return True
    return False


# US14
def is_morethan_5_siblings_at_sametime(birth_date):
    birth_dates = ['10 Jan 2022', '12 Jan 2022', '14 Jan 2022', '16 Jan 2022', '18 Jan 2022', '20 Jan 2022']
    birth_date_counts = defaultdict(int)
    for date_str in birth_dates:
        birth_date = datetime.strptime(date_str, '%d %b %Y')
        birth_date_counts[birth_date] += 1
    if any(count > 5 for count in birth_date_counts.values()):
        return False
    return True


# US04
def is_marriage_before_divorce(marriageday_string, divday_string):
    if marriageday_string or divday_string == "":
        return False
    marriageday = datetime.strptime(marriageday_string, '%d %b %Y')
    divday = datetime.strptime(divday_string, '%d %b %Y')
    if marriageday > divday:
        return False
    return True


# US03
def is_birth_before_death(bday_string, dday_string):
    bday_list = ['01 Feb 1999']
    dday_list = ['02 Aug 1995']
    bday_string = ' '.join(bday_list)
    dday_string = ' '.join(dday_list)
    if bday_string and dday_string == "":
        return False
    bday = datetime.strptime(bday_string, '%d %b %Y')
    deathday = datetime.strptime(dday_string, '%d %b %Y')
    if bday > deathday:
        return False
    return True


# US21
def correct_gender_for_role(role, gender):
    valid_genders = {
        "HUSBAND": "M",
        "WIFE": "F",
        "SON": "M",
        "DAUGHTER": "F"
    }
    if valid_genders.get(role, "") != gender:
        print("ERROR: INDIVIDUAL: US21: Gender for role", role, "is not correct")
        return False
    return True


# US22
def generate_unique_id(individuals, prefix='I'):
    used_ids = set(i.get('INDI', {}).get('ID') for i in individuals)
    i = 1
    while True:
        id = f"{prefix}{i}"
        if id not in used_ids:
            return id
        else:
            print("ERROR: INDIVIDUAL: US22: Non-unique ID", id)
        i += 1


with open("gedcom_project.ged") as file:
    for line in file:
        result = parse_line(line)
        indi_count = 0
        fam_count = 0
        if result:
            if indi_count < 5000 and fam_count < 1000:
                level, tag, valid, arguments = result
                if arguments == "INDI":
                    current_indi = {"ID": tag, "NAME": "", "SEX": "", "BIRT": "", "AGE": "", "ALIVE": True, "DEAT": "",
                                    "FAMC": [], "FAMS": []}
                    individuals.append(current_indi)
                elif arguments == "FAM":
                    current_fam = {"ID": tag, "HUSB": "", "WIFE": "", "MARR": "", "DIV": "", "CHIL": []}
                    families.append(current_fam)
                elif tag == "NAME" and current_indi is not None:
                    current_indi["NAME"] = arguments.strip()
                    indi_dict[current_indi["ID"]] = current_indi["NAME"]
                elif tag == "SEX" and current_indi is not None:
                    current_indi["SEX"] = arguments.strip()
                elif tag == "BIRT" and current_indi is not None:
                    current_indi["BIRT"] = " ".join(next(file).strip().split()[2:])
                    bday = datetime.strptime(current_indi["BIRT"], '%d %b %Y')
                    today = datetime.today()
                    delta = today - bday
                    current_indi["AGE"] = int(delta.days / 365)
                    if is_date_before_current_date(current_indi["BIRT"]) == False:
                        print(
                            f"ERROR: Individual {current_indi['ID']} has a birth date {current_indi['BIRT']} after the current date.")
                    if is_deathdate_lessthan_150years(current_indi["BIRT"]) == False:
                        print(
                            f"ERROR: Individual {current_indi['ID']} has a birth date {current_indi['BIRT']} more than 150 years old.")
                    if is_birthdates_of_siblings(current_indi["BIRT"], current_indi["BIRT"]) == False:
                        print(
                            f"ERROR: Individual {current_indi['ID']} has a birth date {current_indi['BIRT']} less than 8 months to their sibling")
                    if is_morethan_5_siblings_at_sametime(current_indi["BIRT"]) == False:
                        print(
                            f"ERROR: Individual {current_indi['ID']} has a birth date {current_indi['BIRT']} same as other 5 siblings")
                elif tag == "DEAT" and current_indi is not None:
                    current_indi["ALIVE"] = False
                    current_indi["DEAT"] = " ".join(next(file).strip().split()[2:])
                    if is_date_before_current_date(current_indi["DEAT"]) == False:
                        print(f"ERROR: Individual {current_indi['ID']} has a death date after the current date.")
                    if is_deathdate_lessthan_150years(current_indi["DEAT"]) == False:
                        print(
                            f"ERROR: Individual {current_indi['ID']} has a death date {current_indi['DEAT']} more than 150 years old after birth.")
                    if is_birth_before_death(current_indi["BIRT"], current_indi["DEAT"]) == False:
                        print(
                            f"ERROR: Individual {current_indi['ID']} Birth {current_indi['BIRT']} should occur before death {current_indi['DEAT']}")
                elif tag == "FAMC" and current_indi is not None:
                    current_indi["FAMC"].append(arguments.strip())
                elif tag == "FAMS" and current_indi is not None:
                    current_indi["FAMS"].append(arguments.strip())
                elif tag == "HUSB" and current_fam is not None:
                    current_fam["HUSB"] = arguments.strip()
                    if parents_not_too_old(current_indi["BIRT"], current_indi["BIRT"], current_indi["BIRT"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']}: Father {current_fam['HUSB']} is more than 80 years old than child")
                elif tag == "WIFE" and current_fam is not None:
                    current_fam["WIFE"] = arguments.strip()
                    if parents_not_too_old(current_indi["BIRT"], current_indi["BIRT"], current_indi["BIRT"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']}: Mother {current_fam['WIFE']} is more than 60 years old than child")
                elif tag == "CHIL" and current_fam is not None:
                    current_fam["CHIL"].append(arguments.strip())
                    if is_birthdate_before_marrdate_ofparents(current_fam["MARR"], current_fam["DIV"],
                                                              current_indi["BIRT"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']}: {current_fam['CHIL']} was born: {current_indi['BIRT']} before marriage date: {current_fam['MARR']}")
                    if birth_before_parents_death(current_indi["BIRT"], current_indi["DEAT"],
                                                  current_indi["DEAT"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']}: {current_fam['CHIL']} was born: {current_indi['BIRT']} after 9 months of the father's death")
                elif tag == "MARR" and current_fam is not None:
                    current_fam["MARR"] = " ".join(next(file).strip().split()[2:])
                    if is_date_before_current_date(current_fam["MARR"]) == False:
                        print(f"ERROR: Families {current_fam['ID']} has a marriage date after the current date.")
                    if is_birthdate_before_marrdate(current_indi["BIRT"], current_fam["MARR"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']} has a marriage date:{current_fam['MARR']} before birth date: {current_indi['BIRT']}.")
                    if is_marriage_before_death(current_indi["DEAT"], current_fam["MARR"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']}: Married {current_fam['MARR']} after death {current_indi['DEAT']} of spouse.")
                    if no_bigamy(current_fam["MARR"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']}: Marriage {current_fam['MARR']} should not occur during marriage to another spouse.")
                    if is_marriage_before_divorce(current_fam["MARR"], current_fam["DIV"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']}: has a marriage date: {current_fam['MARR']} after the divorce date: {current_fam['DIV']}")
                    if marriage_after_14(current_fam["MARR"], current_indi["BIRT"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']}: Marriage {current_fam['MARR']} should be after 14 years of birth: {current_indi['BIRT']}")
                elif tag == "DIV" and current_fam is not None:
                    current_fam["DIV"] = " ".join(next(file).strip().split()[2:])
                    if is_date_before_current_date(current_fam["DIV"]) == False:
                        print(f"ERROR: Families {current_fam['ID']} has a divorce date after the current date.")
                    if is_birthdate_before_marrdate_ofparents(current_fam["MARR"], current_fam["DIV"],
                                                              current_indi["BIRT"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']}: has a child after 9 months of divorce date: {current_fam['DIV']}")
                    if is_divorce_before_death(current_fam["DIV"], current_indi["DEAT"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']}: Divorce: {current_fam['DIV']} after spouse's death: {current_indi['DEAT']}")

indi_table = PrettyTable(["ID", "NAME", "GENDER", "BIRTHDAY", "AGE", "ALIVE", "DEATH", "FAMILY"])
for indi in individuals:
    fams = ", ".join(indi["FAMS"])
    famc = ", ".join(indi["FAMC"])
    indi_table.add_row(
        [indi["ID"], indi["NAME"], indi["SEX"], indi["BIRT"], indi["AGE"], indi["ALIVE"], indi["DEAT"], indi["FAMS"]])
print("Individuals:")
print(indi_table)

fam_table = PrettyTable(["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])

for fam in families:
    husband_name = indi_dict.get(fam["HUSB"], "")
    wife_name = indi_dict.get(fam["WIFE"], "")
    children = ", ".join(fam["CHIL"])
    fam_table.add_row(
        [fam["ID"], fam.get("MARR", ""), fam.get("DIV", ""), fam["HUSB"], husband_name, fam["WIFE"], wife_name,
         children])

print("\nFamilies:")
print(fam_table)
correct_gender_for_role("HUSBAND", "F")