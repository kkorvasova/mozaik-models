# -*- coding: utf-8 -*-
"""
"""
# import matplotlib
# matplotlib.use('Agg')

from mozaik.storage.datastore import Hdf5DataStore, PickledDataStore
from mozaik.controller import Global
from parameters import ParameterSet
import mozaik
from mozaik.controller import setup_logging
import sys

import analyze_and_visualize_spectrum as avs

Global.root_directory = sys.argv[1]+'/'

setup_logging()
data_store = PickledDataStore(load=True, parameters=ParameterSet(
    {'root_directory': sys.argv[1], 'store_stimuli': False}), replace=True)

avs.perform_analysis_and_visualization(data_store)
# data_store.save()
