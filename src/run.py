#!/usr/bin/env python

import matplotlib
matplotlib.use("Agg")
from bids import BIDSLayout
import hddm
import pandas as pd
import os.path as op
import os
import argparse
import json


parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Example BIDS App HDDM script.')
parser.add_argument('bids_dir', help='The directory with the input dataset '
                    'formatted according to the BIDS standard.')
parser.add_argument('output_dir', help='The directory where the output files '
                    'should be stored. If you are running group level analysis '
                    'this folder should be prepopulated with the results of the'
                    'participant level analysis. Defaults to <bids dir>/derivatives/rt')
parser.add_argument('analysis_level', help='Level of the analysis that will be performed. '
                    'Multiple participant level analyses can be run independently '
                    '(in parallel) using the same output_dir.',
                    choices=['participant', 'group'])
parser.add_argument("model",help='json description of model')
parser.add_argument('--participant_label', help='The label(s) of the participant(s) that should be analyzed. The label '
                   'corresponds to sub-<participant_label> from the BIDS spec '
                   '(so it does not include "sub-"). If this parameter is not '
                   'provided all subjects should be analyzed. Multiple '
                   'participants can be specified with a space separated list.',
                   nargs="+")
#parser.add_argument("method",help='estimation method')
args = parser.parse_args()


layout = BIDSLayout(args.bids_dir, validate=False)
derivatives = args.output_dir
#layout = BIDSLayout('data', validate=False)

# load model
with open(args.model) as f:
    model_json = json.load(f)

estimation_method = model_json['HDDMmodel']['estimation']['method']



df = []
for fn in layout.get(suffix='events', return_type='file'):
    df.append(pd.read_table(fn))
    df[-1]['subj_idx'] = layout.get_file(fn).subject

df = pd.concat(df)


# tbd - make function to decode unicode dicts

# TBD - check for both conditions and throw error

if 'depends_on' in model_json['HDDMmodel']['nodes']['HDDM']['arguments']:
    depends_on_fixed = {}
    for d in model_json['HDDMmodel']['nodes']['HDDM']['arguments']['depends_on']:
        depends_on_fixed[d.encode('ascii','ignore')]=model_json['HDDMmodel']['nodes']['HDDM']['arguments']['depends_on'][d].encode('ascii','ignore')
    model = hddm.HDDM(df,
                  depends_on=depends_on_fixed)

elif 'regressors' in model_json['HDDMmodel']['nodes']['HDDM']:
    regressors_fixed = []
    for r in model_json['HDDMmodel']['nodes']['HDDM']['regressors']:
        for k in r:
            regressors_fixed={k.encode('ascii','ignore'):r[k].encode('ascii','ignore'),'link_func':lambda x: x}

    model = hddm.HDDMRegressor(df,regressors_fixed)


if estimation_method == 'mcmc':

    burn = model_json['HDDMmodel']['estimation']['burn']
    n_samples = model_json['HDDMmodel']['estimation']['n_samples']
    model.sample(n_samples,
                 burn=burn)

    if not op.exists(op.join(derivatives, 'hddm_mcmc')):
        os.makedirs(op.join(derivatives, 'hddm_mcmc'))

    for key, row in model.get_group_nodes().iterrows():
        fn = op.join(derivatives, 'hddm_mcmc', 'group_par-{}_traces.tsv'.format(key))
        trace = pd.DataFrame(row.node.trace[:])
        trace.to_csv(fn, sep='\t', header=False, index=False)

    for key, row in model.get_subj_nodes().iterrows():
        subject = row.subj_idx

        d = op.join(derivatives, 'hddm_mcmc', 'sub-{subject}',
                                 'func').format(**locals())

        if not op.exists(d):
            os.makedirs(d)
        
        trace = pd.DataFrame(row.node.trace[:])

        par = row.knode_name
        if len(row.tag) > 0:
            par = par + str(row.tag)
        par = par.replace(',)', ')').replace("'", "")

        fn = op.join(d, 'sub-{subject}_par-{par}_traces.tsv').format(subject=subject,
                                                                     par=par)
        trace.to_csv(fn, sep='\t', header=False, index=False)

elif estimation_method == 'mle':
    model.find_starting_values()


    if not op.exists(op.join(derivatives, 'hddm_mle')):
        os.makedirs(op.join(derivatives, 'hddm_mle'))

    for key, row in model.get_subj_nodes().iterrows():
        subject = row.subj_idx

        d = op.join(derivatives, 'hddm_mle', 'sub-{subject}',
                                 'func').format(**locals())

        if not op.exists(d):
            os.makedirs(d)
        
        par = row.knode_name
        if len(row.tag) > 0:
            par = par + str(row.tag)
        par = par.replace(',)', ')').replace("'", "")

        fn = op.join(d, 'sub-{subject}_par-{par}_estimate.tsv').format(subject=subject,
                                                                     par=par)

        trace = pd.DataFrame([row.node.value])
        trace.to_csv(fn, sep='\t', header=False, index=False)
        model.save('test.pkl')
