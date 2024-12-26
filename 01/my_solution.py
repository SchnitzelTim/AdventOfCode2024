#! python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 23:27:57 2024

@author: TimBa
"""

import re
import sys

with open('input.txt', 'r') as inF:
	lInputLines = inF.readlines()

reLine = re.compile(r'(?P<Left>\d+)\s+(?P<Right>\d+)\n*')

lLeft = []
lRight = []
for idxLine, sLine in enumerate(lInputLines):
	try:
		if len(sLine) > 0:
			m = reLine.fullmatch(sLine)
			if m:
				lLeft.append(int(m['Left']))
				lRight.append(int(m['Right']))
			else:
				raise ValueError('The line must match the expected format when it is not empty')
	except Exception as ex:
		raise type(ex)(f'{ex}while processing the contents of line {idxLine + 1} from file input.txt').with_traceback(sys.exc_info()[2])

lLeftSorted = sorted(lLeft)
lRightSorted = sorted(lRight)
iDistance = 0
for idx in range(len(lLeftSorted)):
	iDistance += abs(lLeftSorted[idx] - lRightSorted[idx])

print(f'The total distance is {iDistance}.')

iSimilarityScore = 0
for idx in range(len(lLeft)):
	iValue = lLeft[idx]
	iCount = lRight.count(iValue)
	iSimilarityScore += iCount * iValue

print(f'The total similarity score is {iSimilarityScore}.')