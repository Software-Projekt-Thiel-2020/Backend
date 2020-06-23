"""Resources of backend."""
# Add new Resources here:
from . import projects
from . import institutions
from . import donations
from . import user
from . import file
from . import voucher

# and here:
BLUEPRINTS = [
    projects.BP,
    institutions.BP,
    donations.BP,
    user.BP,
    file.BP,
    voucher.BP,
]
