# -*- coding: utf-8 -*-

from .models import MO


def calculate(objects):
    for mo in objects:
        agreements = mo.departamentagreement_set.all()
        amount = sum([int(dep.subvention.amount) for dep in agreements if dep.subvention.amount])
        spent = sum([int(contract.summa) for contract in mo.contract_set.all() if contract.summa])
        mo.common_amount = amount
        mo.common_spent = spent
        mo.common_percentage = round(((float(spent)/amount) * 100), 3)
        mo.common_economy = sum([int(auction.start_price) for auction in
                                 mo.auction_set.all() if auction.start_price]) - spent
        mo.save(update_fields=['common_amount', 'common_spent', 'common_percentage', 'common_economy'])


def calculate_accounting(pk=None):
    if pk:
        calculate(MO.objects.filter(pk=pk))
    else:
        calculate(MO.objects.all())
