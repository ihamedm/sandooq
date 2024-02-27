import datetime

import jdatetime


def admin_display_jdatetime(value):
    return '%s' % (
        jdatetime.date.fromgregorian(date=value, locale='fa_IR').strftime('%d %B %Y'))


def display_jdatetime_no_day(value):
    return '%s' % (
        jdatetime.date.fromgregorian(date=value, locale='fa_IR').strftime('%B %Y'))