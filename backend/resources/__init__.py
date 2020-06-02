"""Resources of backend."""
# Add new Resources here:
from . import projects
from . import institutions
from . import user

# and here:
BLUEPRINTS = [
    projects.BP,
    institutions.BP,
    user.BP,
]
