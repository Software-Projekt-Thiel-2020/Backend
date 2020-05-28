"""Resources of backend."""
# Add new Resources here:
from . import projects
from . import institutions

# and here:
BLUEPRINTS = [
    projects.BP,
    institutions.BP,
]
