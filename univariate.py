import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from scipy.stats import chisquare, linregress


dbfile = 'matchmaker.sqlite3'

engine = create_engine(f'sqlite:///db/{dbfile}')
Base = declarative_base()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# Check if wave impacts matches
session = Session()
waves = session\
    .execute(
        """
        select distinct a.wave,
                        count(*) as wavetot,
                        sum(b.dec) as decct
        from Participant as a
        inner join Date as b
        on a.iid = b.iid
        group by a.wave
        """
    )\
    .fetchall()

observed = [wave[2] for wave in waves]
tot_match = sum(observed)
tot_tot = sum([wave[1] for wave in waves])
expected = [tot_match * (wave[1] / tot_tot) for wave in waves]

for i in range(len(waves)):
    pass
    """
    print(f"Wave: {waves[i][0]}")
    print(f"Observed: {observed[i]}")
    print(f"Expected: {expected[i]}")
    print()
    """

print("Evaluation of waves")
print(chisquare(observed, expected))

# Check if size of wave impacts matches
session = Session()
waves = session\
    .execute(
        """
        select distinct round,
                        count(*) as wavetot,
                        sum(dec) as decct
        from Date
        group by round
        """
    )\
    .fetchall()

sizes = [wave[0] for wave in waves]
totals = [wave[1] for wave in waves]
yeses = [wave[2] for wave in waves]
pcts = [yeses[i] / totals[i] for i in range(len(sizes))]

print()
print("Evaluation of size")
print(linregress(x=sizes, y=pcts))

# Check if position impacts matches
session = Session()
waves = session\
    .execute(
        """
        select distinct position,
                        count(*) as wavetot,
                        sum(dec) as decct
        from Date
        group by position
        """
    )\
    .fetchall()

observed = [wave[2] for wave in waves]
tot_match = sum(observed)
tot_tot = sum([wave[1] for wave in waves])
expected = [tot_match * (wave[1] / tot_tot) for wave in waves]

for i in range(len(waves)):
    pass
    """
    print(f"Position: {waves[i][0]}")
    print(f"Observed: {observed[i]}")
    print(f"Expected: {expected[i]}")
    print()
    """

print()
print("Evaluation of position")
print(chisquare(observed, expected))

# Check if int_corr impacts matches
session = Session()
waves = session\
    .execute(
        """
        select distinct int_corr,
                        count(*) as wavetot,
                        sum(dec) as decct
        from Date
        group by round
        """
    )\
    .fetchall()

# This is the wrong analysis.  Need logistic regression.
"""
int_corrs = [wave[0] for wave in waves]
totals = [wave[1] for wave in waves]
yeses = [wave[2] for wave in waves]
pcts = [yeses[i] / totals[i] for i in range(len(int_corrs))]

print()
print("Evaluation of int_corr")
print(linregress(x=int_corrs, y=pcts))
"""


# Check if position impacts matches
session = Session()
waves = session\
    .execute(
        """
        select distinct a.gender,
                        count(*) as wavetot,
                        sum(b.dec) as decct
        from Participant as a
        inner join Date as b
        on a.iid = b.iid
        group by a.gender
        """
    )\
    .fetchall()

observed = [wave[2] for wave in waves]
tot_match = sum(observed)
tot_tot = sum([wave[1] for wave in waves])
expected = [tot_match * (wave[1] / tot_tot) for wave in waves]

for i in range(len(waves)):
    pass
    """
    print(f"Position: {waves[i][0]}")
    print(f"Observed: {observed[i]}")
    print(f"Expected: {expected[i]}")
    print()
    """

print()
print("Evaluation of gender")
print(chisquare(observed, expected))

# Age difference (Note: this almost certainly varies by gender)
session = Session()
waves = session\
    .execute(
        """
        select distinct abs(a.age - b.age_o) as agediff,
                        count(*) as wavetot_,
                        sum(b.dec) as decct_
        from Participant as a
        inner join Date as b
        on a.iid=b.iid
        where a.age is not null and b.age_o is not null
        group by abs(a.age - b.age_o)
        """
    )\
    .fetchall()

# Note: this is the wrong analysis.  Need logistic regression.
"""
agediff = [wave[0] for wave in waves]
totals = [wave[1] for wave in waves]
yeses = [wave[2] for wave in waves]
pcts = [yeses[i] / totals[i] for i in range(len(agediff))]

print()
print("Evaluation of agediff")
print(linregress(x=agediff, y=pcts))
"""

# Check if position impacts matches
session = Session()
waves = session\
    .execute(
        """
        select distinct b.samerace,
                        count(*) as wavetot,
                        sum(b.dec) as decct
        from Participant as a
        inner join Date as b
        on a.iid = b.iid
        group by b.samerace
        """
    )\
    .fetchall()

observed = [wave[2] for wave in waves]
tot_match = sum(observed)
tot_tot = sum([wave[1] for wave in waves])
expected = [tot_match * (wave[1] / tot_tot) for wave in waves]

for i in range(len(waves)):
    pass
    """
    print(f"Position: {waves[i][0]}")
    print(f"Observed: {observed[i]}")
    print(f"Expected: {expected[i]}")
    print()
    """

print()
print("Evaluation of samerace")
print(chisquare(observed, expected))
