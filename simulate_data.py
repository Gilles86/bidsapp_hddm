import hddm
import os.path as op
import os
import numpy as np

n_subjects = 10
trials_per_level = 150

easy = {'v':.5, 'a':2, 't':.3, 'sv':0, 'z':.5, 'sz':0, 'st':0}
hard = {'v':.3, 'a':2, 't':.3, 'sv':0, 'z':.5, 'sz':0, 'st':0}

data_a, params_a = hddm.generate.gen_rand_data({'easy': easy,
                                                'hard': hard},
                                                size=trials_per_level,
                                                subjs=n_subjects)

data_a['subj_idx'] += 1

for subject, d in data_a.groupby('subj_idx'):
    sub_dir = op.abspath(op.join('data', 'sub-{subject:02d}', 'func')).format(subject=subject)

    if not op.exists(sub_dir) :
        os.makedirs(sub_dir)
    
    d['onset'] = d.rt.cumsum() + np.arange(len(d))
    d['response'] = d['response'].astype(int)
    d['trial_type'] = d['condition']
    d[['onset', 'trial_type', 'rt', 'response']].to_csv(op.join(sub_dir, 'sub-{subject:02d}_events.tsv').format(subject=subject),
                                          sep='\t',
                                          header=True,
                                          index=False)
