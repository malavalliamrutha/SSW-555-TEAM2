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

def is_date_before_current_date(date_string):
    if date_string == "":
        return False
    date = datetime.strptime(date_string, '%d %b %Y')
    if date > datetime.now():
        return False
        
def is_birthdate_before_marrdate(bday_string1, marrday_string2):
    if bday_string1 and marrday_string2 == "":
        return False
    bday_string1 = datetime.strptime(bday_string1, '%d %b %Y')
    marrday_string2 = datetime.strptime(marrday_string2, '%d %b %Y')
    if bday_string1 > marrday_string2:
        return False

with open("gedcom_project.ged") as file:
    for line in file:
        result = parse_line(line)
        indi_count = 0
        fam_count = 0
        if result:
            if indi_count < 5000 and fam_count < 1000:
                level, tag, valid, arguments = result
                if arguments == "INDI":
                    current_indi = {"ID": tag, "NAME": "", "SEX": "", "BIRT": "", "AGE": "", "ALIVE": True, "DEAT": "", "FAMC": [], "FAMS": []}
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
                        print(f"ERROR: Individual {current_indi['ID']} has a birth date {current_indi['BIRT']} after the current date.")
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
                        print(f"ERROR: Families {current_fam['ID']} has a marriage date:{current_fam['MARR']} before birth date: {current_indi['BIRT']}.")
                elif tag == "DIV" and current_fam is not None:
                    current_fam["DIV"] = " ".join(next(file).strip().split()[2:])
                    if is_date_before_current_date(current_fam["DIV"]) == False:
                        print(f"ERROR: Families {current_fam['ID']} has a divorce date after the current date.")

indi_table = PrettyTable(["ID", "NAME", "GENDER", "BIRTHDAY", "AGE", "ALIVE", "DEATH", "FAMILY"])
for indi in individuals:
    fams = ", ".join(indi["FAMS"])
    famc = ", ".join(indi["FAMC"])
    indi_table.add_row([indi["ID"], indi["NAME"], indi["SEX"], indi["BIRT"], indi["AGE"], indi["ALIVE"], indi["DEAT"], indi["FAMS"]])
print("Individuals:")
print(indi_table)

fam_table = PrettyTable(["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])

for fam in families:
    husband_name = indi_dict.get(fam["HUSB"], "")
    wife_name = indi_dict.get(fam["WIFE"], "")
    children = ", ".join(fam["CHIL"])
    fam_table.add_row([fam["ID"], fam.get("MARR", ""), fam.get("DIV", ""), fam["HUSB"], husband_name, fam["WIFE"], wife_name, children])

print("\nFamilies:")
print(fam_table)

