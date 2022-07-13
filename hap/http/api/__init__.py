from .accessories import index
from .pairing import pairing_setup

HANDLERS = {
    ("GET", "/"): index,
    ("POST", "/pair-setup"): pairing_setup,
}
