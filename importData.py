import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


#################################################
#                 SET UP DATABASE               #
#################################################

dbname = 'matchmaker.sqlite3'

# Initialize database
try:
    os.remove(f'db/{dbname}')
except OSError:
    pass
engine = create_engine(f'sqlite:///db/{dbname}')
Base = declarative_base()
Base.metadata.create_all(engine)

#################################################
#                   READ IN CSV                 #
#################################################

csvl = os.path.join('raw', 'Speed_Dating_Data_UNIX.csv')

df = pd.read_csv(csvl,
                 index_col='iid')

# Baseline and demographics
df[[
    'id',
    'gender',
    'idg',
    'condtn',
    'wave',
    'age',
    'field',
    'field_cd',
    'undergra',
    'mn_sat',
    'tuition',
    'race',
    'imprace',
    'imprelig',
    'from',
    'zipcode',
    'income',
    'goal',
    'date',
    'go_out',
    'career',
    'career_c',
    'sports',
    'tvsports',
    'exercise',
    'dining',
    'museums',
    'art',
    'hiking',
    'gaming',
    'clubbing',
    'reading',
    'tv',
    'theater',
    'movies',
    'concerts',
    'music',
    'shopping',
    'yoga',
    'exphappy',
    'expnum',
    'match_es',
]]\
    .drop_duplicates()\
    .to_sql('Participant',
            con=engine)

# Baseline
df[[
    'attr1_1',
    'sinc1_1',
    'intel1_1',
    'fun1_1',
    'amb1_1',
    'shar1_1',
    'attr4_1',
    'sinc4_1',
    'intel4_1',
    'fun4_1',
    'amb4_1',
    'shar4_1',
    'attr2_1',
    'sinc2_1',
    'intel2_1',
    'fun2_1',
    'amb2_1',
    'shar2_1',
    'attr3_1',
    'sinc3_1',
    'fun3_1',
    'intel3_1',
    'amb3_1',
    'attr5_1',
    'sinc5_1',
    'intel5_1',
    'fun5_1',
    'amb5_1'
]]\
    .drop_duplicates()\
    .rename(
        columns={
            'attr1_1': 'attr1',
            'sinc1_1': 'sinc1',
            'intel1_1': 'intel1',
            'fun1_1': 'fun1',
            'amb1_1': 'amb1',
            'shar1_1': 'shar1',
            'attr4_1': 'attr4',
            'sinc4_1': 'sinc4',
            'intel4_1': 'intel4',
            'fun4_1': 'fun4',
            'amb4_1': 'amb4',
            'shar4_1': 'shar4',
            'attr2_1': 'attr2',
            'sinc2_1': 'sinc2',
            'intel2_1': 'intel2',
            'fun2_1': 'fun2',
            'amb2_1': 'amb2',
            'shar2_1': 'shar2',
            'attr3_1': 'attr3',
            'sinc3_1': 'sinc3',
            'fun3_1': 'fun3',
            'intel3_1': 'intel3',
            'amb3_1': 'amb3',
            'attr5_1': 'attr5',
            'sinc5_1': 'sinc5',
            'intel5_1': 'intel5',
            'fun5_1': 'fun5',
            'amb5_1': 'amb5'
        }
    )\
    .to_sql('Baseline',
            con=engine)

# Halfway
df[[
    'attr1_s',
    'sinc1_s',
    'intel1_s',
    'fun1_s',
    'amb1_s',
    'shar1_s',
    'attr3_s',
    'sinc3_s',
    'intel3_s',
    'fun3_s',
    'amb3_s'
]]\
    .drop_duplicates()\
    .rename(
        columns={
            'attr1_s': 'attr1',
            'sinc1_s': 'sinc1',
            'intel1_s': 'intel1',
            'fun1_s': 'fun1',
            'amb1_s': 'amb1',
            'shar1_s': 'shar1',
            'attr3_s': 'attr3',
            'sinc3_s': 'sinc3',
            'intel3_s': 'intel3',
            'fun3_s': 'fun3',
            'amb3_s': 'amb3'
        }
    )\
    .to_sql('Midpoint',
            con=engine)

# Follow-Up 2
df[[
    'satis_2',
    'length',
    'numdat_2',
    'attr7_2',
    'sinc7_2',
    'intel7_2',
    'fun7_2',
    'amb7_2',
    'shar7_2',
    'attr1_2',
    'sinc1_2',
    'intel1_2',
    'fun1_2',
    'amb1_2',
    'shar1_2',
    'attr4_2',
    'sinc4_2',
    'intel4_2',
    'fun4_2',
    'amb4_2',
    'shar4_2',
    'attr2_2',
    'sinc2_2',
    'intel2_2',
    'fun2_2',
    'amb2_2',
    'shar2_2',
    'attr3_2',
    'sinc3_2',
    'intel3_2',
    'fun3_2',
    'amb3_2',
    'attr5_2',
    'sinc5_2',
    'intel5_2',
    'fun5_2',
    'amb5_2',
    'you_call',
    'them_cal'
]]\
    .drop_duplicates()\
    .rename(
        columns={
            'satis_2':  'satis',
            'numdat_2': 'numdat',
            'attr7_2':  'attr7',
            'sinc7_2':  'sinc7',
            'intel7_2': 'intel7',
            'fun7_2':   'fun7',
            'amb7_2':   'amb7',
            'shar7_2':  'shar7',
            'attr1_2':  'attr1',
            'sinc1_2':  'sinc1',
            'intel1_2': 'intel1',
            'fun1_2':   'fun1',
            'amb1_2':   'amb1',
            'shar1_2':  'shar1',
            'attr4_2':  'attr4',
            'sinc4_2':  'sinc4',
            'intel4_2': 'intel4',
            'fun4_2':   'fun4',
            'amb4_2':   'amb4',
            'shar4_2':  'shar4',
            'attr2_2':  'attr2',
            'sinc2_2':  'sinc2',
            'intel2_2': 'intel2',
            'fun2_2':   'fun2',
            'amb2_2':   'amb2',
            'shar2_2':  'shar2',
            'attr3_2':  'attr3',
            'sinc3_2':  'sinc3',
            'intel3_2': 'intel3',
            'fun3_2':   'fun3',
            'amb3_2':   'amb3',
            'attr5_2':  'attr5',
            'sinc5_2':  'sinc5',
            'intel5_2': 'intel5',
            'fun5_2':   'fun5',
            'amb5_2':   'amb5'
        }
    )\
    .to_sql('FollowUp1',
            con=engine)





# Survey 3
df[[
    'date_3',
    'numdat_3',
    'num_in_3',
    'attr1_3',
    'sinc1_3',
    'intel1_3',
    'fun1_3',
    'amb1_3',
    'shar1_3',
    'attr7_3',
    'sinc7_3',
    'intel7_3',
    'fun7_3',
    'amb7_3',
    'shar7_3',
    'attr4_3',
    'sinc4_3',
    'intel4_3',
    'fun4_3',
    'amb4_3',
    'shar4_3',
    'attr2_3',
    'sinc2_3',
    'intel2_3',
    'fun2_3',
    'amb2_3',
    'shar2_3',
    'attr3_3',
    'sinc3_3',
    'intel3_3',
    'fun3_3',
    'amb3_3',
    'attr5_3',
    'sinc5_3',
    'intel5_3',
    'fun5_3',
    'amb5_3'
]]\
    .drop_duplicates()\
    .rename(
        columns={
            'date_3': 'date',
            'numdat_3': 'numdat',
            'num_in_3': 'num_in',
            'attr1_3': 'attr1',
            'sinc1_3': 'sinc1',
            'intel1_3': 'intel1',
            'fun1_3': 'fun1',
            'amb1_3': 'amb1',
            'shar1_3': 'shar1',
            'attr7_3': 'attr7',
            'sinc7_3': 'sinc7',
            'intel7_3': 'intel7',
            'fun7_3': 'fun7',
            'amb7_3': 'amb7',
            'shar7_3': 'shar7',
            'attr4_3': 'attr4',
            'sinc4_3': 'sinc4',
            'intel4_3': 'intel4',
            'fun4_3': 'fun4',
            'amb4_3': 'amb4',
            'shar4_3': 'shar4',
            'attr2_3': 'attr2',
            'sinc2_3': 'sinc2',
            'intel2_3': 'intel2',
            'fun2_3': 'fun2',
            'amb2_3': 'amb2',
            'shar2_3': 'shar2',
            'attr3_3': 'attr3',
            'sinc3_3': 'sinc3',
            'intel3_3': 'intel3',
            'fun3_3': 'fun3',
            'amb3_3': 'amb3',
            'attr5_3': 'attr5',
            'sinc5_3': 'sinc5',
            'intel5_3': 'intel5',
            'fun5_3': 'fun5',
            'amb5_3': 'amb5'

        }
    )\
    .to_sql('FollowUp2',
            con=engine)

# Date-related
df[[
    'round',
    'position',
    'positin1',
    'order',
    'partner',
    'pid',
    'match',
    'int_corr',
    'samerace',
    'age_o',
    'race_o',
    'pf_o_att',
    'pf_o_sin',
    'pf_o_int',
    'pf_o_fun',
    'pf_o_amb',
    'pf_o_sha',
    'dec_o',
    'attr_o',
    'sinc_o',
    'intel_o',
    'fun_o',
    'amb_o',
    'shar_o',
    'like_o',
    'prob_o',
    'met_o',
    'dec',
    'attr',
    'sinc',
    'intel',
    'fun',
    'amb',
    'shar',
    'like',
    'prob',
    'met'
]]\
    .to_sql('Date',
            con=engine)
