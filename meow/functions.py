from collections import defaultdict
from django.db.models import Q

from .models import JournalLine, Account


def get_balance_by_date_by_account_ids_for_journal_lines(journal_lines, dates):
    sorted_dates = sorted(dates)

    balance_by_date_by_account_id = defaultdict(dict)
    journal_lines_iter = iter(journal_lines)
    journal_line = next(journal_lines, None)

    for date in sorted_dates:
        while journal_line and journal_line.journal_entry.transaction_date <= date:
            balance = balance_by_date_by_account_id[journal_line.account_id].get(date, 0) + journal_line.amount
            balance_by_date_by_account_id[journal_line.account_id][date] = balance
            journal_line = next(journal_lines_iter, None)

    return balance_by_date_by_account_id


def get_balance_by_date_by_account_ids_for_account_ids(account_ids, dates):
    journal_lines = (
        JournalLine.objects
        .filter(account_id__in=account_ids)
        .order_by('journal_entry__transaction_date')
    )

    return get_balance_by_date_by_account_ids_for_journal_lines(journal_lines, dates)


def get_aggregate_balance_by_date_by_account_ids_for_account_ids(account_ids, dates):
    ranges = Account.objects.filter(id__in=account_ids).values_list('left', 'right')

    q_objects = Q()
    for left, right in ranges:
        q_objects |= Q(node__left__gte=left, node__right__lte=right)

    aggregate_account_ids = Account.objects.filter(q_objects).values_list('id', flat=True)

    return get_balance_by_date_by_account_ids_for_account_ids(aggregate_account_ids, dates)


def get_account_balance_as_of_date(account_id, date):
    balance_by_date_by_account_id = get_balance_by_date_by_account_ids_for_account_ids([account_id], [date])

    return balance_by_date_by_account_id[account_id][date]


def get_aggregate_account_balance_as_of_date(account_id, date):
    balance_by_date_by_account_id = get_aggregate_balance_by_date_by_account_ids_for_account_ids([account_id], [date])

    return balance_by_date_by_account_id[account_id][date]
