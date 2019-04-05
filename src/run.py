import matplotlib
matplotlib.use("Agg")
from bids import BIDSLayout
import hddm
import pandas as pd
import os.path as op
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("method", default='mcmc')
args = parser.parse_args()

layout = BIDSLayout('/sourcedata', validate=False)
derivatives = '/derivatives'
#layout = BIDSLayout('data', validate=False)

df = []
for fn in layout.get(suffix='events', return_type='file'):
    df.append(pd.read_table(fn))
    df[-1]['subj_idx'] = layout.get_file(fn).subject

df = pd.concat(df)

model = hddm.HDDM(df,
                  depends_on={'v':'trial_type'})

if args.method == 'mcmc':
    model.sample(500)

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

elif args.method == 'mle':
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
