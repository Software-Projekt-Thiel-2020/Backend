"""Resources of backend."""
# Add new Resources here:
from . import sample
from . import projects
from . import institutions

# and here:
BLUEPRINTS = [
    sample.BP,
    projects.BP,
    institutions.BP,
]
