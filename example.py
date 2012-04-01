import os

from whitenoise import Site
from whitenoise.configurators import *

this_dir = os.path.dirname(os.path.abspath(__file__))

site = Site(
        os.path.join(this_dir, 'example')
        )

site.generate(os.path.join(this_dir, '_example'))
