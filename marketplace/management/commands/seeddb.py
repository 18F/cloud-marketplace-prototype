import random
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth.models import User

from marketplace.models import Product, LicenseRequest
from marketplace.tests import factories

PRODUCTS = [
    factories.FavroFactory.build(),
    factories.MuralFactory.build(),
    factories.TrelloFactory.build(),
    factories.ZoomFactory.build(),
]


def create_admin_user(stdout, email='admin@gsa.gov'):
    user = User.objects.filter(email=email).first()
    if user:
        stdout.write(f'Ensuring {email} is a superuser.')
    if not user:
        stdout.write(f'Creating superuser {email}.')
        user = factories.UserFactory.build(
            username=email,
            email=email,
        )
    user.is_staff = True
    user.is_superuser = True
    user.save()


def create_products(products, stdout):
    created_products = []
    for product in products:
        existing = Product.objects.filter(slug=product.slug).first()
        if existing:
            stdout.write(f'{product.name} already exists.')
        else:
            product.save()
            existing = product
            stdout.write(f'Created {product.name}.')
        created_products.append(existing)
    return created_products


def create_license_types(products, stdout, count=3):
    lts = []
    for product in products:
        lts.extend(factories.LicenseTypeFactory.create_batch(
            count,
            product=product,
        ))
    for lt in lts:
        stdout.write(f'Created license type "{lt}".')
    return lts


def create_teams(stdout, count=3, team_size=5):
    teams = factories.TeamFactory.create_batch(count)
    users = []
    for team in teams:
        stdout.write(f'Created team "{team}".')
        members = factories.UserFactory.create_batch(team_size)
        users.extend(members)
        team.users.set(members)
        team.save()
        for member in members:
            stdout.write(f'Added "{member.email}" to team "{team}".')
    return (teams, users)


def create_purchases(license_types, teams, stdout, license_count=2):
    purchases = []
    for lt in license_types:
        p = factories.PurchaseFactory.create(
            license_count=license_count,
            license_type=lt,
            team=random.choice(teams),
        )
        stdout.write(
            f'Created a purchase of {p.license_count} licenses of '
            f'"{p.license_type}" for team "{p.team}".'
        )
        purchases.append(p)
    return purchases


def create_license_requests(users, purchases, stdout, min_waitlisted=1):
    waitlisted = 0
    while waitlisted < min_waitlisted:
        for user in users:
            team = user.teams.all().order_by('?').first()
            purchase = team.purchases.all().order_by('?').first()
            status = random.choice([
                LicenseRequest.REQUESTED,
                LicenseRequest.GRANTED,
                LicenseRequest.DENIED,
                LicenseRequest.RELINQUISHED,
            ])
            lt = purchase.license_type
            if (status == LicenseRequest.GRANTED and
                    lt.get_stats_for_team(team).available == 0):
                status = LicenseRequest.WAITLISTED
                waitlisted += 1
            req = factories.LicenseRequestFactory.create(
                team=team,
                user=user,
                license_type=lt,
                status=status,
            )
            stdout.write(
                f'Created a license request on behalf of {user.email} '
                f'for "{lt}" with status "{status}".'
            )


class Command(BaseCommand):
    help = 'Seeds the marketplace with initial development data'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--reset', action='store_true', dest='full_reset',
            default=False,
            help='Destroy everything currently in the database first.',
        )

    def handle(self, *args, **options):
        if options.get('full_reset'):
            call_command('reset_db')
            call_command('migrate')

        products = create_products(PRODUCTS, self.stdout)
        lts = create_license_types(products, self.stdout)
        teams, users = create_teams(self.stdout)
        purchases = create_purchases(lts, teams, self.stdout)
        create_license_requests(users, purchases, self.stdout)
        create_admin_user(self.stdout)
