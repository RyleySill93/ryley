from datetime import date
from django.db import models
from django.db.models import F


class NodeFamily(models.Model):
    name = models.CharField(null=True, blank=True, max_length=10000)


class Node(models.Model):
    name = models.CharField(null=True, blank=True, max_length=10000)  # probably dont need this
    node_family = models.ForeignKey(NodeFamily, on_delete=models.CASCADE)
    left = models.IntegerField()
    right = models.IntegerField()

    def insert_sibling(self, name):
        return self.insert_node(self.right, name)

    def insert_child(self, name):
        return self.insert_node(self.left, name)

    @staticmethod
    def insert_node(node_left, name):
        # move all nodes less or equal to new left down by 1
        Node.objects.filter(left__lte=node_left).update(left=F('left') - 1)
        Node.objects.filter(right__lte=node_left).update(right=F('right') - 1)

        # move all nodes greater than or equal to new left up one
        Node.objects.filter(left__gte=node_left).update(left=F('left') + 1)
        Node.objects.filter(right__gte=node_left).update(right=F('right') + 1)

        return Node.objects.create(left=node_left, right=node_left + 1, name=name)


class JournalEntry(models.Model):
    transaction_date = models.DateTimeField(null=True, blank=True)


class Account(models.Model):
    DEBIT = 'DEBIT'
    CREDIT = 'CREDIT'
    NORMAL_BALANCE_CHOICES = (
        (DEBIT, DEBIT),
        (CREDIT, CREDIT),
    )
    normal_balance = models.CharField(choices=NORMAL_BALANCE_CHOICES, default=DEBIT, max_length=10000)
    name = models.CharField(null=True, blank=True, max_length=10000)
    node = models.OneToOneField(Node, on_delete=models.CASCADE)

    def get_account_balance(self, as_of_date=None):
        from .functions import get_account_balance_as_of_date

        if as_of_date is None:
            as_of_date = date.today()

        return get_account_balance_as_of_date(self.id, as_of_date)

    def get_aggregate_account_balance(self, as_of_date=None):
        from .functions import get_aggregate_account_balance_as_of_date
        if as_of_date is None:
            as_of_date = date.today()

        return get_aggregate_account_balance_as_of_date(self.id, as_of_date)


class JournalLine(models.Model):
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=22, decimal_places=2)
