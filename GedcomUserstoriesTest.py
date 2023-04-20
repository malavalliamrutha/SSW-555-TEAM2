import unittest
import pytest
import GedcomUserstories
from GedcomUserstories import*


from datetime import datetime, timedelta


class TestDates(unittest.TestCase):

    def test_birth_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_date_before_current_date(futuredate_string), False,
                         "Birth date should not be after current date")

    def test_marriage_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_date_before_current_date(futuredate_string), False,
                         "Marriage date should not be after current date")

    def test_divorce_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_date_before_current_date(futuredate_string), False,
                         "Divorce date should not be after current date")

    def test_death_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_date_before_current_date(futuredate_string), False,
                         "Death date should not be after current date")

    def test_birthdate_after_marrdate(self):
        futuredate = datetime.now()
        futuredate_str = futuredate.strftime('%d %b %Y')
        birthdate = datetime.now() + timedelta(days=10)
        birthday_string = birthdate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_birthdate_before_marrdate(birthday_string, futuredate_str), False,
                         "Birth date should not be after marriage date")

    def test_birthdate_before_marrdate(self):
        birthdate = datetime.now()
        birthday_string = birthdate.strftime('%d %b %Y')
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_str = futuredate.strftime('%d %b %Y')
        self.assertNotEqual(GedcomUserstories.is_birthdate_before_marrdate(birthday_string, futuredate_str), False,
                            "Birth date is before marriage date")

    def test_marriage_before_death(self):
        marr_date_str = '01 Jan 2020'
        death_date_str = '01 Jan 2021'
        self.assertFalse(GedcomUserstories.is_marriage_before_death(marr_date_str, death_date_str))

    def test_divorce_before_death(self):
        # Test when divorce is before death
        divday = "1 JAN 2022"
        deatday = "12 JAN 2022"
        self.assertNotEqual(GedcomUserstories.is_divorce_before_death(divday, deatday), True,
                            "Divorce before death test failed.")

        # Test when divorce is after death
        divday = "12 JAN 2022"
        deatday = "1 JAN 2022"
        self.assertEqual(GedcomUserstories.is_divorce_before_death(divday, deatday), False,
                         "Divorce after death test failed.")

        # Test when either divorce or death date is missing
        divday = "10 MAR 2000"
        deatday = ""
        self.assertEqual(GedcomUserstories.is_divorce_before_death(divday, deatday), False,
                         "Missing death date test failed.")

    def test_birth_before_parents_death(self):
        # Test case where birth is before both parents' deaths
        birth_date = datetime.strptime('01 Jan 1990', '%d %b %Y')
        mother_death_date = datetime.strptime('01 Jan 2000', '%d %b %Y')
        father_death_date = datetime.strptime('01 Jan 2005', '%d %b %Y')
        self.assertTrue(GedcomUserstories.birth_before_parents_death(birth_date, mother_death_date, father_death_date))

        # Test case where birth is after mother's death
        birth_date = datetime.strptime('01 Jan 2010', '%d %b %Y')
        mother_death_date = datetime.strptime('01 Jan 2000', '%d %b %Y')
        father_death_date = datetime.strptime('01 Jan 2005', '%d %b %Y')
        self.assertFalse(GedcomUserstories.birth_before_parents_death(birth_date, mother_death_date, father_death_date))

        # Test case where birth is after father's death
        birth_date = datetime.strptime('01 Jan 2010', '%d %b %Y')
        mother_death_date = datetime.strptime('01 Jan 2000', '%d %b %Y')
        father_death_date = datetime.strptime('01 Jan 2005', '%d %b %Y')
        self.assertFalse(GedcomUserstories.birth_before_parents_death(birth_date, mother_death_date, father_death_date))

    def test_marriage_after_14(self):
        # Test case where marriage is after 14 years from birth
        birth_date = datetime.strptime('01 Jan 2000', '%d %b %Y')
        marriage_date = birth_date + timedelta(days=365 * 14)
        self.assertFalse(GedcomUserstories.marriage_after_14(marriage_date, birth_date))

        # Test case where marriage is before 14 years from birth
        birth_date = datetime.strptime('01 Jan 2000', '%d %b %Y')
        marriage_date = birth_date + timedelta(days=365 * 13)
        self.assertFalse(GedcomUserstories.marriage_after_14(marriage_date, birth_date))

    def test_fewer_than_15_siblings(self):
        family_with_fewer_siblings = {'children': ['C1', 'C2', 'C3']}
        family_with_many_siblings = {
            'children': ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14',
                         'C15']}

        self.assertTrue(GedcomUserstories.fewer_than_15_siblings(family_with_fewer_siblings))
        self.assertFalse(GedcomUserstories.fewer_than_15_siblings(family_with_many_siblings))

    def test_male_last_names(self):
        family = {'children': ['I1', 'I2', 'I3']}
        individuals = {
            'I1': {'gender': 'M', 'last_name': 'Smith'},
            'I2': {'gender': 'M', 'last_name': 'Smith'},
            'I3': {'gender': 'F', 'last_name': 'Smith'}
        }
        self.assertTrue(GedcomUserstories.male_last_names(family, individuals))

        individuals['I2']['last_name'] = 'Johnson'
        self.assertFalse(GedcomUserstories.male_last_names(family, individuals))

    def test_no_bigamy(self):
        # Test case where there are no marriages
        marr_list = []
        self.assertTrue(GedcomUserstories.no_bigamy(marr_list))

        # Test case where there is only one marriage
        marr_list = ['01 Jan 2000']
        self.assertTrue(GedcomUserstories.no_bigamy(marr_list))

        # Test case where all marriages are in chronological order
        marr_list = ['01 Jan 2000', '01 Jan 2001', '01 Jan 2002']
        self.assertTrue(GedcomUserstories.no_bigamy(marr_list))

        # Test case where there are multiple marriages and some are not in chronological order
        marr_list = ['01 Jan 2000', '01 Jan 1999', '01 Jan 2002']
        self.assertTrue(GedcomUserstories.no_bigamy(marr_list))

    def test_parents_not_too_old(self):
        # Test case where parents are not too old
        mom_birthdate = '01 Jan 1960'
        dad_birthdate = '01 Jan 1950'
        child_birthdate = '01 Jan 2000'
        self.assertFalse(GedcomUserstories.parents_not_too_old(mom_birthdate, dad_birthdate, child_birthdate))

        # Test case where mom is too old
        mom_birthdate = '01 Jan 1930'
        dad_birthdate = '01 Jan 1950'
        child_birthdate = '01 Jan 2000'
        self.assertFalse(GedcomUserstories.parents_not_too_old(mom_birthdate, dad_birthdate, child_birthdate))

        # Test case where both parents are too old
        mom_birthdate = '01 Jan 1930'
        dad_birthdate = '01 Jan 1920'
        child_birthdate = '01 Jan 2000'
        self.assertFalse(GedcomUserstories.parents_not_too_old(mom_birthdate, dad_birthdate, child_birthdate))

    def test_both_dates_provided(self):
        self.assertFalse(GedcomUserstories.is_marriage_before_divorce("01 Jan 2000", "01 Jan 2001"))

    def test_birthdate_lessthan_150years(self):
        birthdate = datetime.now() - timedelta(days=365 * 30)
        birthday_string = birthdate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_deathdate_lessthan_150years(birthday_string), True,
                         "Current date is less than 150 years after birth")

    def test_birthdate_morethan_150years(self):
        birthdate = datetime.now() - timedelta(days=365 * 200)
        birthday_string = birthdate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_deathdate_lessthan_150years(birthday_string), False,
                         "Current date is more than 150 years after birth")

    def test_birthdate_before_death(self):
        birthdate = datetime.now()
        birthday_string = birthdate.strftime('%d %b %Y')
        deathdate = datetime.now() + timedelta(days=10)
        deathdate_str = deathdate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_birth_before_death(birthday_string, deathdate_str), False,
                         "Birth date is before death date")

    def test_birthdate_of_siblings_before_8_months(self):
        birthdate = datetime.now()
        birthday_string = birthdate.strftime('%d %b %Y')
        birthday2 = datetime.now() + timedelta(days=240)
        birthday2_string = birthday2.strftime('%d %b %Y')
        self.assertFalse(GedcomUserstories.is_birthdates_of_siblings(birthday_string, birthday2_string))

    def test_morethan_5_siblings_birth_on_sameday(self):
        birth_dates_valid = ['10 Jan 2022', '12 Jan 2022', '14 Jan 2022', '16 Jan 2022', '18 Jan 2022', '20 Jan 2022',
                             '22 Jan 2022', '24 Jan 2022', '26 Jan 2022', '28 Jan 2022']
        self.assertTrue(GedcomUserstories.is_morethan_5_siblings_at_sametime(birth_dates_valid))
        birth_dates_invalid = ['10 Jan 2022', '12 Jan 2022', '14 Jan 2022', '16 Jan 2022', '18 Jan 2022', '20 Jan 2022',
                               '22 Jan 2022', '24 Jan 2022', '26 Jan 2022', '28 Jan 2022', '30 Jan 2022', '30 Jan 2022',
                               '30 Jan 2022', '30 Jan 2022', '30 Jan 2022', '01 Feb 2022']
        self.assertTrue(GedcomUserstories.is_morethan_5_siblings_at_sametime(birth_dates_invalid))

    def test_valid_genders(self):
        self.assertTrue(GedcomUserstories.correct_gender_for_role("HUSBAND", "M"))
        self.assertTrue(GedcomUserstories.correct_gender_for_role("WIFE", "F"))
        self.assertTrue(GedcomUserstories.correct_gender_for_role("SON", "M"))
        self.assertTrue(GedcomUserstories.correct_gender_for_role("DAUGHTER", "F"))

    def test_invalid_genders(self):
        self.assertFalse(GedcomUserstories.correct_gender_for_role("HUSBAND", "F"))
        self.assertFalse(GedcomUserstories.correct_gender_for_role("WIFE", "M"))
        self.assertFalse(GedcomUserstories.correct_gender_for_role("SON", "F"))
        self.assertFalse(GedcomUserstories.correct_gender_for_role("DAUGHTER", "M"))

    def test_unknown_role(self):
        self.assertFalse(GedcomUserstories.correct_gender_for_role("FATHER", "F"))
        self.assertFalse(GedcomUserstories.correct_gender_for_role("MOTHER", "M"))
        self.assertFalse(GedcomUserstories.correct_gender_for_role("SON", "F"))
        self.assertFalse(GedcomUserstories.correct_gender_for_role("DAUGHTER", "M"))

    def test_generate_unique_id_with_no_prefix(self):
        # Test that function returns unique ID with no prefix
        individuals = [{'INDI': {'ID': 'I1'}}, {'INDI': {'ID': 'I2'}}]
        unique_id = GedcomUserstories.generate_unique_id(individuals)
        self.assertEqual(unique_id, 'I3')

    def test_generate_unique_id_with_prefix(self):
        # Test that function returns unique ID with prefix
        individuals = [{'INDI': {'ID': 'I1'}}, {'INDI': {'ID': 'I2'}}]
        unique_id = GedcomUserstories.generate_unique_id(individuals, prefix='P')
        self.assertEqual(unique_id, 'P1')

    def test_siblings_not_married_to_eachother(self):
        person1 = {'family_id': '@F6000000191180558840@', 'parent_id': '@I6000000191181596839@'}
        person2 = {'family_id': '@F6000000191180558840@', 'parent_id': '@I6000000191181596839@'}
        self.assertFalse(GedcomUserstories.siblings_cannot_marry(person1, person2))

    def test_unique_first_names_in_families(self):
        individuals = self.user_story.get_individuals()
        families = self.user_story.get_families()
        self.assertTrue(self.user_story.is_unique_first_names_in_families(individuals, families),
                        "Not all first names in families are unique")

    def test_corresponding_entries(self):
        individuals = self.user_story.get_individuals()
        families = self.user_story.get_families()
        self.assertTrue(self.user_story.has_corresponding_entries(individuals, families),
                        "Not all entries in families correspond to individuals")

    def test_first_cousin_cannot_marry(self):
        families = {
            'family1': {
                'id': 'family1',
                'husb': 'I1',
                'wife': 'I2',
                'chil': ['I3', 'I4'],
            },
            'family2': {
                'id': 'family2',
                'husb': 'I5',
                'wife': 'I6',
                'chil': ['I7', 'I8'],
            }
        }
        self.assertFalse(GedcomUserstories.first_cousin_cannot_marry('I3', 'I7', 'family1', 'family2', families))

        # US23 by Arun Rao Nayineni

    def test_unique_name_birth_date(self):
        individuals = [
            {'Name': 'John Cena', 'Birth Date': '1980-01-01'},
            {'Name': 'Jane Cena', 'Birth Date': '1985-05-12'}
        ]
        self.assertTrue(GedcomUserstories.is_name_birth_date_unique(individuals))

        # US23 by Arun Rao Nayineni

    def test_duplicate_name_birth_date(self):
        individuals = [
            {'Name': 'John Cena', 'Birth Date': '1980-01-01'},
            {'Name': 'Jane Cena', 'Birth Date': '1985-05-12'},
            {'Name': 'John Cena', 'Birth Date': '1980-01-01'}
        ]
        self.assertFalse(GedcomUserstories.is_name_birth_date_unique(individuals))

    # US24 by Arun Rao Nayineni
    def test_unique_families(self):
        families = [
            {'Husband Name': 'Virat', 'Wife Name': 'Anushka', 'Marriage Date': '1995-06-12'},
            {'Husband Name': 'Bhuvi', 'Wife Name': 'Nupur', 'Marriage Date': '2000-04-25'}
        ]
        self.assertTrue(GedcomUserstories.are_families_unique_by_spouses(families))

    # US24 by Arun Rao Nayineni
    def test_duplicate_families(self):
        families = [
            {'Husband Name': 'Sachin', 'Wife Name': 'Anjali', 'Marriage Date': '1995-06-12'},
            {'Husband Name': 'Michael Smith', 'Wife Name': 'Michelle Smith', 'Marriage Date': '2000-04-25'},
            {'Husband Name': 'Sachin', 'Wife Name': 'Anjali', 'Marriage Date': '1995-06-12'}
        ]
        self.assertFalse(GedcomUserstories.are_families_unique_by_spouses(families))

    #US27 test
    def test_individual_ages(self):
        self.assertEqual(individual_ages(n1,b1), 1)
        self.assertEqual(individual_ages(n2, b2), -1)
        self.assertEqual(individual_ages(n3, b3), -1)
        self.assertEqual(individual_ages(n4, b4), 1)
        self.assertEqual(individual_ages(n5, b5), -1)
        
if __name__ == '__main__':
    unittest.main()
