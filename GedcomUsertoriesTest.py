import unittest
import GedcomUserstories

from datetime import datetime, timedelta
class TestDates(unittest.TestCase):

    def test_birth_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_date_before_current_date(futuredate_string), False, "Birth date should not be after current date")

    def test_marriage_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_date_before_current_date(futuredate_string), False, "Marriage date should not be after current date")

    def test_divorce_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_date_before_current_date(futuredate_string), False, "Divorce date should not be after current date")

    def test_death_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_date_before_current_date(futuredate_string), False, "Death date should not be after current date")
                
    def test_birthdate_after_marrdate(self):
        futuredate = datetime.now()
        futuredate_str = futuredate.strftime('%d %b %Y')
        birthdate = datetime.now() + timedelta(days=10)
        birthday_string = birthdate.strftime('%d %b %Y')
        self.assertEqual(GedcomUserstories.is_birthdate_before_marrdate(birthday_string,futuredate_str), False, "Birth date should not be after marriage date")

    def test_birthdate_before_marrdate(self):
        birthdate = datetime.now()
        birthday_string = birthdate.strftime('%d %b %Y')
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_str =futuredate.strftime('%d %b %Y')
        self.assertNotEqual(GedcomUserstories.is_birthdate_before_marrdate(birthday_string,futuredate_str), False, "Birth date is before marriage date")

    def test_marriage_before_death(self):
        marr_date_str = '01 Jan 2020'
        death_date_str = '01 Jan 2021'
        self.assertTrue(GedcomUserstories.is_marriage_before_death(marr_date_str, death_date_str))

    def test_divorce_before_death(self):
        # Test when divorce is before death
        divday = "1 JAN 2022"
        deatday = "12 JAN 2022"
        self.assertEqual(GedcomUserstories.is_divorce_before_death(divday, deatday), True, "Divorce before death test failed.")

        # Test when divorce is after death
        divday = "12 JAN 2022"
        deatday = "1 JAN 2022"
        self.assertEqual(GedcomUserstories.is_divorce_before_death(divday, deatday), False, "Divorce after death test failed.")

        # Test when either divorce or death date is missing
        divday = "10 MAR 2000"
        deatday = ""
        self.assertEqual(GedcomUserstories.is_divorce_before_death(divday, deatday), False, "Missing death date test failed.")
    
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
        self.assertFalse(GedcomUserstories.no_bigamy(marr_list))

    def test_parents_not_too_old(self):
        # Test case where parents are not too old
        mom_birthdate = '01 Jan 1960'
        dad_birthdate = '01 Jan 1950'
        child_birthdate = '01 Jan 2000'
        self.assertTrue(GedcomUserstories.parents_not_too_old(mom_birthdate, dad_birthdate, child_birthdate))
        
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
       self.assertTrue(GedcomUserstories.is_marriage_before_divorce("01 Jan 2000", "01 Jan 2001"))

    def test_missing_marriage_date(self):
        self.assertFalse(GedcomUserstories.is_marriage_before_divorce("", "01 Jan 2000"))

    def test_missing_both_dates(self):
        self.assertFalse(GedcomUserstories.is_marriage_before_divorce("", ""))

if __name__ == '__main__':
    unittest.main()
    