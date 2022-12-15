from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class StatesChoices(TextChoices):
    IN_STOCK = _('In stock')
    ON_ORDER = _('On order')
    EXPECTED_TO_ARRIVE = _('Expected to arrive')
    NOT_AVAILABLE = _('Not available')
    NOT_PRODUCED = _('Not produced')
