from django.utils import unittest, timezone
import datetime
from ss.lib.utils import ssDate


class MonthTestCase(unittest.TestCase):
    def setUp(self):
        self.january = ssDate(year='2011', month='01', day='12', size='month')
        self.february = ssDate(year='2011', month='02', day='12', size='month')
        self.earlymarch = ssDate(year='2011', month='03', day='05', size='month')
        self.latemarch = ssDate(year='2011', month='03', day='31', size='month')
        self.july = ssDate(year='2011', month='07', day='12', size='month')
        self.earlyoctober = ssDate(year='2011', month='10', day='10', size='month')
        self.lateoctober = ssDate(year='2011', month='10', day='31', size='month')
        self.november = ssDate(year='2011', month='11', day='12', size='month')

    def figures(self, date):
        (year, month, day) = (date.year, date.month, date.day)
        return year, month, day

    def test_january_start(self):
        self.assertEqual(self.figures(self.january.startDate()), (2011, 1, 1))

    def test_january_end(self):
        self.assertEqual(self.figures(self.january.endDate()), (2011, 1, 31))

    def test_february_start(self):
        self.assertEqual(self.figures(self.february.startDate()), (2011, 2, 1))

    def test_february_end(self):
        self.assertEqual(self.figures(self.february.endDate()), (2011, 2, 28))

    def test_earlymarch_start(self):
        self.assertEqual(self.figures(self.earlymarch.startDate()), (2011, 3, 1))

    def test_earlymarch_end(self):
        self.assertEqual(self.figures(self.earlymarch.endDate()), (2011, 3, 31))

    def test_latemarch_start(self):
        self.assertEqual(self.figures(self.latemarch.startDate()), (2011, 3, 1))

    def test_latemarch_end(self):
        self.assertEqual(self.figures(self.latemarch.endDate()), (2011, 3, 31))

    def test_july_start(self):
        self.assertEqual(self.figures(self.july.startDate()), (2011, 7, 1))

    def test_july_end(self):
        self.assertEqual(self.figures(self.july.endDate()), (2011, 7, 31))

    def test_earlyoctober_start(self):
        self.assertEqual(self.figures(self.earlyoctober.startDate()), (2011, 10, 1))

    def test_earlyoctober_end(self):
        self.assertEqual(self.figures(self.earlyoctober.endDate()), (2011, 10, 31))

    def test_lateoctober_start(self):
        self.assertEqual(self.figures(self.lateoctober.startDate()), (2011, 10, 1))

    def test_lateoctober_end(self):
        self.assertEqual(self.figures(self.lateoctober.endDate()), (2011, 10, 31))

    def test_november_start(self):
        self.assertEqual(self.figures(self.november.startDate()), (2011, 11, 1))

    def test_november_end(self):
        self.assertEqual(self.figures(self.november.endDate()), (2011, 11, 30))

    def test_month_lengths(self):
        self.assertEqual(len(self.january.days()), 31)
        self.assertEqual(len(self.february.days()), 28)
        self.assertEqual(len(self.earlymarch.days()), 31)
        self.assertEqual(len(self.latemarch.days()), 31)
        self.assertEqual(len(self.july.days()), 31)
        self.assertEqual(len(self.earlyoctober.days()), 31)
        self.assertEqual(len(self.lateoctober.days()), 31)
        self.assertEqual(len(self.november.days()), 30)


class MonthDatetimeTestCase(MonthTestCase):
    def setUp(self):
        self.january = ssDate(datetime.datetime(2011, 01, 12, 14, 23, 01, 50))# year='2011', month='01', day='12', size='month')
        self.february = ssDate(datetime.datetime(2011, 02, 12, 14, 23, 01, 50))# year='2011', month='02', day='12', size='month')
        self.earlymarch = ssDate(datetime.datetime(2011, 03, 05, 14, 23, 01, 50))# year='2011', month='03', day='05', size='month')
        self.latemarch = ssDate(datetime.datetime(2011, 03, 31, 14, 23, 01, 50))# year='2011', month='03', day='31', size='month')
        self.july = ssDate(datetime.datetime(2011, 07, 12, 14, 23, 01, 50))# year='2011', month='07', day='12', size='month')
        self.earlyoctober = ssDate(datetime.datetime(2011, 10, 10, 14, 23, 01, 50))# year='2011', month='10', day='10', size='month')
        self.lateoctober = ssDate(datetime.datetime(2011, 10, 31, 14, 23, 01, 50))# year='2011', month='10', day='31', size='month')
        self.november = ssDate(datetime.datetime(2011, 11, 12, 14, 23, 01, 50))# year='2011', month='11', day='12', size='month')


class WeekTestCase(unittest.TestCase):
    def setUp(self):
        self.january = ssDate(year='2011', month='01', day='12', size='week')
        self.february = ssDate(year='2011', month='02', day='12', size='week')
        self.earlymarch = ssDate(year='2011', month='03', day='05', size='week')
        self.latemarch = ssDate(year='2011', month='03', day='23', size='week')
        self.july = ssDate(year='2011', month='07', day='12', size='week')
        self.earlyoctober = ssDate(year='2011', month='10', day='10', size='week')
        self.lateoctober = ssDate(year='2011', month='10', day='26', size='week')
        self.november = ssDate(year='2011', month='11', day='12', size='week')

    def figures(self, date):
        (year, month, day) = (date.year, date.month, date.day)
        return year, month, day

    def test_january_start(self):
        self.assertEqual(self.figures(self.january.startDate()), (2011, 1, 10))

    def test_january_end(self):
        self.assertEqual(self.figures(self.january.endDate()), (2011, 1, 16))

    def test_february_start(self):
        self.assertEqual(self.figures(self.february.startDate()), (2011, 2, 7))

    def test_february_end(self):
        self.assertEqual(self.figures(self.february.endDate()), (2011, 2, 13))

    def test_earlymarch_start(self):
        self.assertEqual(self.figures(self.earlymarch.startDate()), (2011, 2, 28))

    def test_earlymarch_end(self):
        self.assertEqual(self.figures(self.earlymarch.endDate()), (2011, 3, 6))

    def test_latemarch_start(self):
        self.assertEqual(self.figures(self.latemarch.startDate()), (2011, 3, 21))

    def test_latemarch_end(self):
        self.assertEqual(self.figures(self.latemarch.endDate()), (2011, 3, 27))

    def test_july_start(self):
        self.assertEqual(self.figures(self.july.startDate()), (2011, 7, 11))

    def test_july_end(self):
        self.assertEqual(self.figures(self.july.endDate()), (2011, 7, 17))

    def test_earlyoctober_start(self):
        self.assertEqual(self.figures(self.earlyoctober.startDate()), (2011, 10, 10))

    def test_earlyoctober_end(self):
        self.assertEqual(self.figures(self.earlyoctober.endDate()), (2011, 10, 16))

    def test_lateoctober_start(self):
        self.assertEqual(self.figures(self.lateoctober.startDate()), (2011, 10, 24))

    def test_lateoctober_end(self):
        self.assertEqual(self.figures(self.lateoctober.endDate()), (2011, 10, 30))

    def test_november_start(self):
        self.assertEqual(self.figures(self.november.startDate()), (2011, 11, 7))

    def test_november_end(self):
        self.assertEqual(self.figures(self.november.endDate()), (2011, 11, 13))


    def test_week_lengths_a(self):
        self.assertEqual(len(self.january.days()), 7)

    def test_week_lengths_b(self):
        self.assertEqual(len(self.february.days()), 7)

    def test_week_lengths_c(self):
        self.assertEqual(len(self.earlymarch.days()), 7)

    def test_week_lengths_d(self):
        self.assertEqual(len(self.latemarch.days()), 7)

    def test_week_lengths_e(self):
        self.assertEqual(len(self.july.days()), 7)

    def test_week_lengths_f(self):
        self.assertEqual(len(self.earlyoctober.days()), 7)

    def test_week_lengths_g(self):
        self.assertEqual(len(self.lateoctober.days()), 7)

    def test_week_lengths_h(self):
        self.assertEqual(len(self.november.days()), 7)


class WeekByWeekTestCase(WeekTestCase):
    def setUp(self):
        self.january = ssDate(year='2011', week='02')
        self.february = ssDate(year='2011', week='06')
        self.earlymarch = ssDate(year='2011', week='09')
        self.latemarch = ssDate(year='2011', week='12')
        self.july = ssDate(year='2011', week='28')
        self.earlyoctober = ssDate(year='2011', week='41')
        self.lateoctober = ssDate(year='2011', week='43')
        self.november = ssDate(year='2011', week='45')


# class DayTestCase(unittest.TestCase):
#     def setUp(self):
#         self.january = ssDate(year='2011', month='01', day='12', size='day')
#         self.february = ssDate(year='2011', month='02', day='12', size='day')
#         self.earlymarch = ssDate(year='2011', month='03', day='05', size='day')
#         self.latemarch = ssDate(year='2011', month='03', day='27', size='day')
#         self.july = ssDate(year='2011', month='07', day='12', size='day')
#         self.earlyoctober = ssDate(year='2011', month='10', day='10', size='day')
#         self.lateoctober = ssDate(year='2011', month='10', day='30', size='day')
#         self.november = ssDate(year='2011', month='11', day='12', size='day')
#
#     def figures(self, date):
#         (year, month, day, hour, minute, second, utcoffset) = (date.year, date.month, date.day, date.hour, date.minute, date.second, date.utcoffset().seconds)
#         return year, month, day, hour, minute, second, utcoffset
#
#     def test_january_start(self):
#         self.assertEqual(self.figures(self.january.startDate()), (2011, 1, 12))
#
#     def test_january_end(self):
#         self.assertEqual(self.figures(self.january.endDate()), (2011, 1, 12))
#
#     def test_february_start(self):
#         self.assertEqual(self.figures(self.february.startDate()), (2011, 2, 12))
#
#     def test_february_end(self):
#         self.assertEqual(self.figures(self.february.endDate()), (2011, 2, 12))
#
#     def test_earlymarch_start(self):
#         self.assertEqual(self.figures(self.earlymarch.startDate()), (2011, 3, 5))
#
#     def test_earlymarch_end(self):
#         self.assertEqual(self.figures(self.earlymarch.endDate()), (2011, 3, 5))
#
#     def test_latemarch_start(self):
#         self.assertEqual(self.figures(self.latemarch.startDate()), (2011, 3, 27))
#
#     def test_latemarch_end(self):
#         self.assertEqual(self.figures(self.latemarch.endDate()), (2011, 3, 27))
#
#     def test_july_start(self):
#         self.assertEqual(self.figures(self.july.startDate()), (2011, 7, 12))
#
#     def test_july_end(self):
#         self.assertEqual(self.figures(self.july.endDate()), (2011, 7, 12))
#
#     def test_earlyoctober_start(self):
#         self.assertEqual(self.figures(self.earlyoctober.startDate()), (2011, 10, 10))
#
#     def test_earlyoctober_end(self):
#         self.assertEqual(self.figures(self.earlyoctober.endDate()), (2011, 10, 10))
#
#     def test_lateoctober_start(self):
#         self.assertEqual(self.figures(self.lateoctober.startDate()), (2011, 10, 30))
#
#     def test_lateoctober_end(self):
#         self.assertEqual(self.figures(self.lateoctober.endDate()), (2011, 10, 30))
#
#     def test_november_start(self):
#         self.assertEqual(self.figures(self.november.startDate()), (2011, 11, 12))
#
#     def test_november_end(self):
#         self.assertEqual(self.figures(self.november.endDate()), (2011, 11, 12))
#
#     def test_day_lengths_a(self):
#         self.assertEqual(len(self.january.days()), 1)
#
#     def test_day_lengths_b(self):
#         self.assertEqual(len(self.february.days()), 1)
#
#     def test_day_lengths_c(self):
#         self.assertEqual(len(self.earlymarch.days()), 1)
#
#     def test_day_lengths_d(self):
#         self.assertEqual(len(self.latemarch.days()), 1)
#
#     def test_day_lengths_e(self):
#         self.assertEqual(len(self.july.days()), 1)
#
#     def test_day_lengths_f(self):
#         self.assertEqual(len(self.earlyoctober.days()), 1)
#
#     def test_day_lengths_g(self):
#         self.assertEqual(len(self.lateoctober.days()), 1)
#
#     def test_day_lengths_h(self):
#         self.assertEqual(len(self.november.days()), 1)


class YearTestCase(unittest.TestCase):
    def setUp(self):
        self.year = ssDate(year='2011', size='year')

    def figures(self, date):
        (year, month, day) = (date.year, date.month, date.day)
        return year, month, day

    def test_start(self):
        self.assertEqual(self.figures(self.year.startDate()), (2011, 1, 1))

    def test_end(self):
        self.assertEqual(self.figures(self.year.endDate()), (2011, 12, 31))

    def test_lengths(self):
        self.assertEqual(len(self.year.days()), 365)