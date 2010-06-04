"""
Custom terminal color scheme.
"""

from django.core.management import color
from django.utils import termcolors


def color_style():
	style = color.color_style()
	style.BOLD = termcolors.make_style(opts = ('bold',))
	style.GREEN = termcolors.make_style(fg = 'green', opts = ('bold',))
	style.YELLOW = termcolors.make_style(fg = 'yellow')
	style.BLUE = termcolors.make_style(fg = 'blue', opts = ('bold',))
	style.RED = termcolors.make_style(fg = 'red')
	
	return style

style = color_style()