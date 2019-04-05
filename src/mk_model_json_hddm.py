"""
build model for hddm
"""
import json
import os

model_dict_simple= {
    'HDDMmodel':{
        'nodes':{
             'HDDM':{
                'arguments':{
                    'depends_on':{'v':'trial_type'}
                 }
            }
        },
        'estimation':{
            'n_samples':10000,
            'burn':1000,
            'method':'mle'
        }
    }
}


model_dict= {
    'HDDMmodel':{
        'nodes':{
             'HDDM':{
                'regressors':[{'model':'v ~ 1 + C(trial_type)'}], # TBD: add link_function
                'arguments':{
                    'include':[]
                 }
            }
        },
        'estimation':{
            'n_samples':10000,
            'burn':1000,
            'method':'mle'
        }
    }
}

if not os.path.exists('../models'):
    os.mkdir('../models')

with open('../models/hddm_model.json','w') as f:

    json.dump(model_dict,f,indent = 4)
