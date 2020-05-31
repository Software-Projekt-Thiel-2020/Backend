"""Resources of backend."""
# Add new Resources here:
from . import projects
from . import institutions
from . import donations

# and here:
BLUEPRINTS = [
    projects.BP,
    institutions.BP,
    donations.BP,
]
