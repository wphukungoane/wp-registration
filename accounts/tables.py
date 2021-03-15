
from .models import User, Profile
import django_tables2 as tables

import itertools


class AccountsTable(tables.Table):
    first_name = tables.Column()

    class Meta:
        model = Profile
        attrs = {"class": "table"}
