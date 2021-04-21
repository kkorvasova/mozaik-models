import os
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

# def spontaneous(data_store, params):
#     '''
#     Analyze spectrum during spontaneous activity.
#     '''
#
#     print '\n Starting to analyze spontaneous activity.'
#
#     segs = param_filter_query(data_store, sheet_name="V1_Exc_L2/3", ).get_segments()
#     print 'Loaded altogether {} experiments'.format(len(segs))
#
#     specs = {'grating_duration': None,
#             'sheets': list(set(data_store.sheets()) & set(
#                 ['V1_Exc_L4', 'V1_Inh_L4', 'V1_Exc_L2/3', 'V1_Inh_L2/3']))
#             'st_name': 'InternalStimulus'}
#     segs = param_filter_query(data_store,
#                     sheet_name="V1_Exc_L2/3",
#                     st_name=specs['st_name']).get_segments()
#     print 'Specified {} experiments'. format(len(segs))
#
#
#     popsigs = {}
#     bs = params['binsize']
#
#     for layer in specs['sheets']:
#
#         spids = param_filter_query(
#                                 data_store,
#                                 sheet_name=layer,
#                                 st_name=specs['st_name']
#                                 ).get_segments()[0].get_stored_spike_train_ids()
#
#         hists = param_filter_query(data_store,analysis_algorithm='PSTH',
#                                   y_axis_name='psth (bin={})'.format(bs),
#                                   sheet_name=layer,
#                                   st_name=specs['st_name']
#                                   ).get_analysis_result()
#         assert len(hists)==1
#
#         hist = hists[0]
#
#         hist_array = hist.get_asl_by_id(spids)
#         spar = []
#         for itm in hist_array:
#             spar.append(itm.magnitude)
#
#         spar = np.squeeze(np.array(spar))
#
#         popsigs[layer] = [np.mean(spar, axis=0)]
#
#
#     psds = analysis.calc_psds(popsigs, params)
#     vs.plot_psds(psds, specs, params)
#
#     # # PSDs of neurons, too little spikes
#     # psds = analysis.calc_unit_psds(data_store, specs, params)
#     # plotting.plot_psds(psds, specs, params, su=True)
#
# def orientations(data_store, params):
#     '''
#     Analyze spectrum for different orientations of a full-field grating.
#     '''
#
#     print '\n Starting to analyze FullfieldDriftingSinusoidalGrating.'
#
#     specs = {'grating_duration': None,
#             'sheets':  list(set(data_store.sheets()) & set(
#                 ['V1_Exc_L4', 'V1_Inh_L4', 'V1_Exc_L2/3', 'V1_Inh_L2/3']))
#             'st_name': 'FullfieldDriftingSinusoidalGrating'}
#
#     segs = param_filter_query(data_store, sheet_name="V1_Exc_L2/3",
#                                     st_name=specs['st_name']).get_segments()
#     print 'Specified {} experiments'.format(len(segs))
#
#
#     stimuli = param_filter_query(data_store, sheet_name="V1_Exc_L2/3",
#                                     st_name=specs['st_name']).get_stimuli()
#
#     stimuli_dict=[ast.literal_eval(stimulus) for stimulus in stimuli]
#     orientations=np.unique(np.array(
#                     [stimulus['orientation'] for stimulus in stimuli_dict
#                                     if 'orientation' in stimulus]))
#     print 'Orientations:', orientations
#
#     specs['orientations'] = orientations
#
#     popsigs = {}
#     bs = params['binsize']
#
#     for layer in specs['sheets']:
#
#         popsigs[layer] = []
#
#         for ornr, orientation in enumerate(orientations):
#             spids = param_filter_query(
#                                     data_store,
#                                     sheet_name=layer,
#                                     st_name=specs['st_name'],
#                                     st_orientation=specs['orientations'][ornr]
#                                     ).get_segments()[0].get_stored_spike_train_ids()
#
#             hists = param_filter_query(data_store,analysis_algorithm='PSTH',
#                                       y_axis_name='psth (bin={})'.format(bs),
#                                       sheet_name=layer,
#                                       st_name=specs['st_name'],
#                                       st_orientation=specs['orientations'][ornr]
#                                       ).get_analysis_result()
#
#             ps_orient = []
#             for hist in hists: # each trial
#                 hist_array = hist.get_asl_by_id(spids)
#                 spar = []
#                 for itm in hist_array: # each neuron
#                     spar.append(itm.magnitude)
#
#                 spar = np.squeeze(np.array(spar))
#
#                 ps_orient.append(np.mean(spar, axis=0))
#
#             ps_orient = np.array(ps_orient)
#
#             popsigs[layer].append(np.mean(ps_orient, axis=0))
#
#     psds = analysis.calc_psds(popsigs, params)
#
#     vs.plot_psds(psds, specs, params, row_labels=orientations)


def perform_analysis_and_visualization(data_store):

    sheets = list(set(data_store.sheets()) & set(
        ['V1_Exc_L4', 'V1_Inh_L4', 'V1_Exc_L2/3', 'V1_Inh_L2/3']))
    # exc_sheets = list(set(data_store.sheets()) &
    #                           set(['V1_Exc_L4', 'V1_Exc_L2/3']))
    # inh_sheets = list(set(data_store.sheets()) &
    #                 set(['V1_Inh_L4', 'V1_Inh_L2/3']))

    NeuronAnnotationsToPerNeuronValues(data_store, ParameterSet({})).analyse()

    segs = param_filter_query(data_store, sheet_name="V1_Exc_L2/3", ).get_segments()
    print 'Loaded altogether {} experiments'.format(len(segs))

    # specs = {'grating_duration': None,
    #         'sheets': list(set(data_store.sheets()) & set(
    #             ['V1_Exc_L4', 'V1_Inh_L4', 'V1_Exc_L2/3', 'V1_Inh_L2/3']))
    #         'st_name': 'InternalStimulus'}



    print 'Starting to analyze spontaneous activity.'
    dsv = param_filter_query(data_store, st_name='InternalStimulus')

    analysis.PopulationActivitySpectrum(dsv,
                        ParameterSet({'bin_length': 2.,
                                    'min_freq': 2.,
                                    'zscore':False,
                                    'stimulus_id': 'spontaneous'}))


#    plotting.SpectrumPlot(dsv, ParameterSet({'sheet_names': sheets}))


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
                        ParameterSet({'bin_length': 2.,
                                    'min_freq': 2.,
                                    'zscore':False,
                                    'stimulus_id': orientation}))

    #    plotting.SpectrumPlot(dsv, ParameterSet({'binsize': 2.,
    #                                'sheet_names': sheets}))
