"""Resources of backend."""
# Add new Resources here:
from . import sample
from . import projects
from . import institutions
from . import user

# and here:
BLUEPRINTS = [
    sample.BP,
    projects.BP,
    institutions.BP,
    user.BP,
]
