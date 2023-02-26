import unittest
import Sprint1

from datetime import datetime, timedelta
class TestDates(unittest.TestCase):

    def test_birth_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(Sprint1.is_date_before_current_date(futuredate_string), False, "Birth date should not be after current date")

    def test_marriage_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(Sprint1.is_date_before_current_date(futuredate_string), False, "Marriage date should not be after current date")

    def test_divorce_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(Sprint1.is_date_before_current_date(futuredate_string), False, "Divorce date should not be after current date")

    def test_death_date(self):
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_string = futuredate.strftime('%d %b %Y')
        self.assertEqual(Sprint1.is_date_before_current_date(futuredate_string), False, "Death date should not be after current date")
                
    def test_birthdate_after_marrdate(self):
        futuredate = datetime.now()
        futuredate_str = futuredate.strftime('%d %b %Y')
        birthdate = datetime.now() + timedelta(days=10)
        birthday_string = birthdate.strftime('%d %b %Y')
        self.assertEqual(Sprint1.is_birthdate_before_marrdate(birthday_string,futuredate_str), False, "Birth date should not be after marriage date")

    def test_birthdate_before_marrdate(self):
        birthdate = datetime.now()
        birthday_string = birthdate.strftime('%d %b %Y')
        futuredate = datetime.now() + timedelta(days=10)
        futuredate_str =futuredate.strftime('%d %b %Y')
        self.assertNotEqual(Sprint1.is_birthdate_before_marrdate(birthday_string,futuredate_str), False, "Birth date is before marriage date")

if __name__ == '__main__':
    unittest.main()
    