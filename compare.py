# "Borrowed" from:
# https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python#13849249

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


dbfile = 'matchmaker.sqlite3'

engine = create_engine(f'sqlite:///db/{dbfile}')
Base = declarative_base()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def getParticipantBaselineVector(iid):
    session = Session()
    bv = session\
        .execute(
            'select distinct attr1, sinc1, intel1, fun1, amb1, shar1 from Baseline where ' + \
            f'iid = "{iid}"'
        )\
        .first()

    if bv: return bv
    else: return None

import numpy as np


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def getScaledDiff(iid1, iid2):
    bv1 = getParticipantBaselineVector(iid1)
    bv2 = getParticipantBaselineVector(iid2)
    ubv1 = unit_vector(bv1)
    ubv2 = unit_vector(bv2)
    diff = angle_between(ubv1, ubv2)

    return scaleAngleDifference(diff)


maxAngle = angle_between((1,0,0,0,0,0), (0,1,0,0,0,0))
def scaleAngleDifference(diff):
    try:
        return diff / maxAngle
    except TypeError:
        return None

bv1 = getParticipantBaselineVector(1)
bv2 = getParticipantBaselineVector(2)
ubv1 = unit_vector(bv1)
ubv2 = unit_vector(bv2)
diff = angle_between(ubv1, ubv2)
scaled_diff = scaleAngleDifference(diff)
print(f'bv1: {bv1}')
print(f'bv2: {bv2}')
print(f'ubv1: {ubv1}')
print(f'ubv2: {ubv2}')
print(f'diff: {diff}')
print(f'scaled_diff: {scaled_diff}')
print()

print(angle_between((1,0,0,0,0,0), (1,0,0,0,0,0)))
print(angle_between((1,0,0,0,0,0), (0,1,0,0,0,0)))
print(angle_between((1,0,0,0,0,0), (0,1,1,1,1,1)))
print()

print(getScaledDiff(1, 2))
print(getScaledDiff(1, 3))
print(getScaledDiff(1, 4))
print(getScaledDiff(1, 5))
print(getScaledDiff(1, 6))
print(getScaledDiff(1, 7))
