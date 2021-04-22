import os

import matplotlib
if 'DISPLAY' not in os.environ:
    matplotlib.use('Agg')

import psutil
import sys
import mozaik
import mozaik.visualization.plotting as plotting
import mozaik.analysis.analysis as analysis
from mozaik.analysis.technical import NeuronAnnotationsToPerNeuronValues
from mozaik.analysis.vision import *
from mozaik.storage.queries import *
from mozaik.storage.datastore import PickledDataStore
from mozaik.controller import Global

import ast

import numpy as np

logger = mozaik.getMozaikLogger()

process = psutil.Process(os.getpid())



def perform_analysis_and_visualization(data_store):

    minfreq = 2. #(Hz)
    binsize = 2. #(ms)

    sheets = list(set(data_store.sheets()) & set(
        ['V1_Exc_L4', 'V1_Inh_L4', 'V1_Exc_L2/3', 'V1_Inh_L2/3']))
    # exc_sheets = list(set(data_store.sheets()) &
    #                           set(['V1_Exc_L4', 'V1_Exc_L2/3']))
    # inh_sheets = list(set(data_store.sheets()) &
    #                 set(['V1_Inh_L4', 'V1_Inh_L2/3']))

    NeuronAnnotationsToPerNeuronValues(data_store, ParameterSet({})).analyse()

    analysis.PSTH(data_store, ParameterSet({'bin_length': binsize})).analyse()

    segs = param_filter_query(data_store, sheet_name="V1_Exc_L2/3", ).get_segments()
    print 'Loaded altogether {} experiments'.format(len(segs))

    # specs = {'grating_duration': None,
    #         'sheets': list(set(data_store.sheets()) & set(
    #             ['V1_Exc_L4', 'V1_Inh_L4', 'V1_Exc_L2/3', 'V1_Inh_L2/3']))
    #         'st_name': 'InternalStimulus'}


    print 'Starting to analyze spontaneous activity.'
    dsv = param_filter_query(data_store, st_name='InternalStimulus')

    analysis.PopulationActivitySpectrum(dsv,
                        ParameterSet({'bin_length': binsize,
                                    'min_freq': minfreq,
                                    'zscore':False,
                                    'stimulus_id': 'spontaneous',
                                    'sheet_names': sheets})).analyse()

    for sheet in sheets:
        plotting.SpectrumPlot(dsv, ParameterSet({'sheet_name': sheet,
                                                'min_freq': minfreq})).plot()


    print 'Starting to analyze FullfieldDriftingSinusoidalGrating.'


    stimuli = param_filter_query(data_store, sheet_name="V1_Exc_L2/3",
                    st_name='FullfieldDriftingSinusoidalGrating').get_stimuli()

    stimuli_dict=[ast.literal_eval(stimulus) for stimulus in stimuli]
    orientations=np.unique(np.array(
                    [stimulus['orientation'] for stimulus in stimuli_dict
                                    if 'orientation' in stimulus]))
    print 'Orientations:', orientations

    trials = np.unique(np.array(
                    [stimulus['trial'] for stimulus in stimuli_dict
                                    if 'trial' in stimulus]))
    print 'Number of trials:', len(trials)

    for orientation in orientations:
        dsv = param_filter_query(data_store,
                                st_name='FullfieldDriftingSinusoidalGrating',
                                st_orientation=orientation)

        analysis.PopulationActivitySpectrum(dsv,
                        ParameterSet({'bin_length': binsize,
                                    'min_freq': minfreq,
                                    'zscore':False,
                                    'stimulus_id': str(orientation),
                                    'sheet_names': sheets})).analyse()

    for sheet in sheets:
        plotting.SpectrumPlot(dsv, ParameterSet({'sheet_name': sheet,
                                                'min_freq': minfreq})).plot()
