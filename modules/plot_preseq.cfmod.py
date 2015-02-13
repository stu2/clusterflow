#!/usr/bin/env python
"""
plot_preseq.cfmod
Takes results from preseq and plots nice colourful complexity curves
using the plot_complexity_curves() function in the ngi_visualizations
Python package. This package is available here:
https://github.com/ewels/ngi_visualizations
"""

##########################################################################
# Copyright 2014, Philip Ewels (phil.ewels@scilifelab.se)                #
#                                                                        #
# This file is part of Cluster Flow.                                     #
#                                                                        #
# Cluster Flow is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# Cluster Flow is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with Cluster Flow.  If not, see <http://www.gnu.org/licenses/>.  #
##########################################################################

from __future__ import print_function
from ..source.CF import Helpers
from ngi_visualizations.plot_complexity_curves import plot_complexity_curves

import argparse
import os
import sys

def make_preseq_plots(parameters, required_cores=False, required_mem=False, required_modules=False, runfn=None, print_help=False):
    """
    -----------------------
    Preseq Plotting Module
    -----------------------
    Takes results from preseq and plots nice colourful complexity curves
    using the plot_complexity_curves() function in the ngi_visualizations
    Python package. This package is available here:
    https://github.com/ewels/ngi_visualizations
    """
    
    # QSUB SETUP
    # --cores i = offered cores. Return number of required cores.
    if required_cores:
        print ('1', file=sys.stdout)
        sys.exit(0)

    # --mem. Return the required memory allocation.
    if required_mem:
        print ('3G', file=sys.stdout)
        sys.exit(0)

    # --modules. Return csv names of any modules which should be loaded.
    if required_modules:
        sys.exit(0)

    # --help. Print help.
    if print_help:
        print (make_preseq_plots.__doc__, file=sys.stdout)
        sys.exit(0)
    
    # Running the module properly now. Parse everything that we're given
    # This includes reading the run file to get input filenames
    p = Helpers.load_runfile_params(parameters)
    timestart = datetime.datetime.now().total_seconds()
    
    # Make the plots!
    plot_complexity_curves(p['files'], output_name = p['runfile'])
    
    # Print success message if we got this far
    duration = str(datetime.datetime.now().total_seconds() - timestart)
    print("###CF Preseq plots successfully exited, took {}..\n".format(duration), file=sys.stderr)
    
    
    

if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Make a scatter plot of FPKM counts between conditions")
    parser.add_argument('--cores', dest='required_cores', action='store_true',
                        help="Request the number of cores needed by the module.")
    parser.add_argument('--mem', dest='required_mem', action='store_true',
                        help="Request the amount of memory needed by the module.")
    parser.add_argument('--modules', dest='required_modules', action='store_true',
                        help="Request the names of environment modules needed by the module.")
    parser.add_argument('--runfn', dest='runfn', type=str, default=None,
                        help="Path to the Cluster Flow run file for this pipeline")
    parser.add_argument('--help', dest='print_help', action='store_true',
                        help="Show module help")
    parser.add_argument('parameters', nargs='*', help="List of parameters.")
    kwargs = vars(parser.parse_args())
    
    # Call plot_observed_genes()
    make_preseq_plots(**kwargs)