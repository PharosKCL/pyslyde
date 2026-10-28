"""PySlyde: A Python package for whole slide image processing and annotation."""

from pyslyde.slide import Slide, Annotations
from pyslyde.slide_parser import WSIParser, Stitching

__version__ = "0.2.1"
__author__ = (
    "Chima Eke, Anthony Baptista, Holly Rafique, Elizabeth Ing-Simmons, "
    "Enrico Parisini, Mengyuan Li, Fathima Mohamed, Ananya Bhalla, Lucy Ryan, "
    "Michael Pitcher, Concetta Piazzese, James Graham, Dinis Pedro Calado, "
    "Christopher R.S. Banerji, Anita Grigoriadis, Gregory Verghese"
)
__email__ = "gregory.verghese@gmail.com"

__all__ = ["Slide", "Annotations", "WSIParser", "Stitching"]



