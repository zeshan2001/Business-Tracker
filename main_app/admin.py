from django.contrib import admin
from .models import Bank, Business, Income_statement, Balance_sheet, Loan, Request, Profile

# Register your models here.
admin.site.register(Bank)
# models for test
admin.site.register(Business)
admin.site.register(Income_statement)
admin.site.register(Balance_sheet)
admin.site.register(Loan)
admin.site.register(Request)
admin.site.register(Profile)