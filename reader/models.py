from __future__ import unicode_literals

import sys
from django.db import models

class Person(models.Model):
	name=models.CharField(max_length=100)

class Transaction(models.Model):
	pid = models.ForeignKey(Person)
	txn_date = models.CharField(max_length=100)
	value_date = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	ref = models.CharField(max_length=100)
	debit = models.CharField(max_length=100)
	credit = models.CharField(max_length=100)
	balance = models.CharField(max_length=100)

	def __unicode__(self):
		return self.ref