#!/usr/bin/env python3

import os
import libfc as fc
#try:
#    f = open(".config")
#except FileNotFoundError:

ud = fc.get_data('user_data', 0)

#    для мужчин: (10 * ud['weight'] + 6.25 * ud['height'] – 5 * ud['age'] + 5) * ud['activity'];

# для женщин: (10 * ud['weight'] + 6.25 * ud['height'] – 5 * ud['age'] - 161) * ud['activity'];


