from re import findall
import pandas as pd
from sqlalchemy.ext.automap import automap_base
#from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from config import pguser, pgpassword, pghost, pgport, pgdatabase

engine = create_engine(
    f"postgresql+psycopg2://{pguser}:{pgpassword}" + \
    f"@{pghost}:{pgport}/{pgdatabase}"
)

Base = automap_base()

# reflect the tables
Base.prepare(engine,
             reflect=True)

sample = pd.read_sql('matchdata',
                       engine)\
    [:50]

def getIID(couple_id, gender):
    if gender: sex='m'
    else: sex='f'
    fa = findall(sex + r'(\d+)', couple_id)
    if fa: return fa[0]
    else: return None

sample_f = sample[[
    'couple_id',
    'f_age',
    'f_imprace',
    'f_attr',
    'f_sinc',
    'f_intel',
    'f_fun',
    'f_amb',
    'f_race',
    'f_intrace'
]].rename(
    columns={
        'f_age':     'age',
        'f_imprace': 'imprace',
        'f_attr':    'attr',
        'f_sinc':    'sinc',
        'f_intel':   'intel',
        'f_fun':     'fun',
        'f_amb':     'amb',
        'f_race':    'race',
        'f_intrace': 'intrace'
    }
)

sample_f['gender'] = 0
sample_f['iid'] = sample_f.apply(lambda row: getIID(row.couple_id, row.gender),
                                 axis=1)

sample_m = sample[[
    'couple_id',
    'm_age',
    'm_imprace',
    'm_attr',
    'm_sinc',
    'm_intel',
    'm_fun',
    'm_amb',
    'm_race',
    'm_intrace'
]].rename(
    columns={
        'm_age':     'age',
        'm_imprace': 'imprace',
        'm_attr':    'attr',
        'm_sinc':    'sinc',
        'm_intel':   'intel',
        'm_fun':     'fun',
        'm_amb':     'amb',
        'm_race':    'race',
        'm_intrace': 'intrace'
    }
)

sample_m['gender'] = 1
sample_m['iid'] = sample_m.apply(lambda row: getIID(row.couple_id, row.gender),
                                 axis=1)

sample_f = sample_f\
    .drop(columns = ['couple_id'])\
    .drop_duplicates(subset='iid')\
    [:5]

sample_m = sample_m\
    .drop(columns = ['couple_id'])\
    .drop_duplicates(subset='iid')\
    [:5]

females = sample_f['iid'].to_list()
males = sample_m['iid'].to_list()

f_fnames = ['Anne',
            'Beth',
            'Catie',
            'Drew',
            'Erica']

f_snames = ['fa100',
            'fa200',
            'fa300',
            'fa400',
            'fa500']

f_emails = ['fa100@matchmaker.com',
            'fa200@matchmaker.com',
            'fa300@matchmaker.com',
            'fa400@matchmaker.com',
            'fa500@matchmaker.com']

f_photos = ['fa100headshot.com',
            'fa200headshot.com',
            'fa300headshot.com',
            'fa400headshot.com',
            'fa500headshot.com']

m_fnames = ['Adam',
            'Bill',
            'Chad',
            'Doug',
            'Eric']

m_snames = ['ma100',
            'ma200',
            'ma300',
            'ma400',
            'ma500']

m_emails = ['ma100@matchmaker.com',
            'ma200@matchmaker.com',
            'ma300@matchmaker.com',
            'ma400@matchmaker.com',
            'ma500@matchmaker.com']

m_photos = ['ma100headshot.com',
            'ma200headshot.com',
            'ma300headshot.com',
            'ma400headshot.com',
            'ma500headshot.com']

female_user_df = pd.DataFrame(data={
    'iid':   females,
    'fname': f_fnames,
    'sname': f_snames,
    'email': f_emails,
    'photo': f_photos
})

male_user_df = pd.DataFrame(data={
    'iid':   males,
    'fname': m_fnames,
    'sname': m_snames,
    'email': m_emails,
    'photo': m_photos
})


sample_f = sample_f.merge(female_user_df, on='iid', how='outer')
sample_m = sample_m.merge(male_user_df,   on='iid', how='outer')

sample_all = pd.concat([sample_f, sample_m])

sample_all\
    .to_sql('Users',
            con=engine)
