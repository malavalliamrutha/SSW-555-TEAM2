from datetime import datetime
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


# US03
def is_birth_before_death(birth_string, death_string):
    if birth_string and death_string == "":
        return False
    birth = datetime.strptime(birth_string, '%d %b %Y')
    death = datetime.strptime(death_string, '%d %b %Y')
    if birth > death:
        print(f"Error: Birth date {birth_string} is after death date {death_string}")
        return False
    return True


# US04
def is_marriage_before_divorce(marriageday_string, divday_string):
    if not marriageday_string or not divday_string:
        print("Error: Missing date")
        return False
    marriageday = datetime.strptime(marriageday_string, '%d %b %Y')
    divday = datetime.strptime(divday_string, '%d %b %Y')
    if marriageday > divday:
        print("Error: Marriage date is after divorce date")
        return False
    return True


# US05
def is_marriage_before_death(marrday_string, deathday_string):
    if marrday_string and deathday_string == "":
        return False
    marrday = datetime.strptime(marrday_string, '%d %b %Y')
    deathday = datetime.strptime(deathday_string, '%d %b %Y')
    if marrday > deathday:
        return False
    return True


# US06
def is_divorce_before_death(divday_string, deathday_string):
    if divday_string and deathday_string == "":
        return False
    divday = datetime.strptime(divday_string, '%d %b %Y')
    deathday = datetime.strptime(deathday_string, '%d %b %Y')
    if divday > deathday:
        print(f"Error: Divorce date {divday_string} is after death date {deathday_string}")
        return False
    return True


# US11
def no_bigamy(marr_list):
    if len(marr_list) <= 1:
        return True
    marr_dates = [datetime.strptime(date, '%d %b %Y') for date in marr_list]
    for i in range(1, len(marr_dates)):
        if marr_dates[i] < marr_dates[i - 1]:
            print(
                f"Error: Individual is involved in bigamy. Marriage on {marr_dates[i].strftime('%d %b %Y')} occurred before previous marriage on {marr_dates[i - 1].strftime('%d %b %Y')}.")
            return False
    return True


# US12
def parents_not_too_old(mom_birthdate_string, dad_birthdate_string, child_birthdate_string):
    mom_birthdate = datetime.strptime(mom_birthdate_string, '%d %b %Y')
    dad_birthdate = datetime.strptime(dad_birthdate_string, '%d %b %Y')
    child_birthdate = datetime.strptime(child_birthdate_string, '%d %b %Y')

    # # Calculate the maximum ages for the parents
    # max_mom_age = child_birthdate.year - mom_birthdate.year + 60
    # max_dad_age = child_birthdate.year - dad_birthdate.year + 80

    # Check if the parents are not too old
    if mom_birthdate > child_birthdate or dad_birthdate > child_birthdate:
        return False
    if mom_birthdate.year < (child_birthdate.year - 60) or dad_birthdate.year < (child_birthdate.year - 80):
        print(
            f"Error: One of the parents is too old. Mom's birth year: {mom_birthdate.year}, Dad's birth year: {dad_birthdate.year}, Child's birth year: {child_birthdate.year}")
        return False

    # parents are not too old
    return True


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
                elif tag == "DEAT" and current_indi is not None:
                    current_indi["ALIVE"] = False
                    current_indi["DEAT"] = " ".join(next(file).strip().split()[2:])
                    if is_date_before_current_date(current_indi["DEAT"]) == False:
                        print(f"ERROR: Individual {current_indi['ID']} has a death date after the current date.")
                elif tag == "FAMC" and current_indi is not None:
                    current_indi["FAMC"].append(arguments.strip())
                elif tag == "FAMS" and current_indi is not None:
                    current_indi["FAMS"].append(arguments.strip())
                elif tag == "HUSB" and current_fam is not None:
                    current_fam["HUSB"] = arguments.strip()
                elif tag == "WIFE" and current_fam is not None:
                    current_fam["WIFE"] = arguments.strip()
                elif tag == "CHIL" and current_fam is not None:
                    current_fam["CHIL"].append(arguments.strip())
                elif tag == "MARR" and current_fam is not None:
                    current_fam["MARR"] = " ".join(next(file).strip().split()[2:])
                    if is_date_before_current_date(current_fam["MARR"]) == False:
                        print(f"ERROR: Families {current_fam['ID']} has a marriage date after the current date.")
                    if is_birthdate_before_marrdate(current_indi["BIRT"], current_fam["MARR"]) == False:
                        print(
                            f"ERROR: Families {current_fam['ID']} has a marriage date:{current_fam['MARR']} before birth date: {current_indi['BIRT']}.")
                elif tag == "DIV" and current_fam is not None:
                    current_fam["DIV"] = " ".join(next(file).strip().split()[2:])
                    if is_date_before_current_date(current_fam["DIV"]) == False:
                        print(f"ERROR: Families {current_fam['ID']} has a divorce date after the current date.")

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
