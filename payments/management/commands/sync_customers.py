from django.core.management.base import BaseCommand

from django.contrib.auth.models import User


class Command(BaseCommand):
    
    help = "Sync customer data"
    
    def handle(self, *args, **options):
        qs = User.objects.exclude(customer__isnull=True)
        count = 0
        total = qs.count()
        for user in qs:
            count += 1
            perc = int(round(100 * (float(count) / float(total))))
            print "[{}/{} {}%] Syncing {} [{}]".format(count, total, perc, user.username, user.pk)
            customer = user.customer
            cu = customer.stripe_customer
            customer.sync(cu=cu)
            customer.sync_current_subscription(cu=cu)
            customer.sync_invoices(cu=cu)
            customer.sync_charges(cu=cu)
