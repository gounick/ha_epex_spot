"""pytest configuration for the epex_spot test suite."""

import os
import sys

# Allow imports of custom_components.epex_spot.* from the repository root.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
