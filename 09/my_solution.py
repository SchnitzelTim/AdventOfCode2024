#! python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 06:54:16 2024

@author: TimBa
"""

with open('input.txt', 'r') as inF:
	sInput = inF.read().strip()

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])

lDiskLayout = []
iState = 1
iNextFileID = 0
for idxCh, ch in enumerate(sInput):
	if not ch.isnumeric():
		raise ValueError(f'The {ordinal(idxCh + 1)} character in the input must be numeric character')
	iLength = int(ch)
	if iState == 0:
		lDiskLayout.extend([None] * iLength)
		iState = 1
	elif iState == 1:
		lDiskLayout.extend([iNextFileID] * iLength)
		iNextFileID += 1
		iState = 0
	else:
		raise ValueError('Unexpected state')

lRearrangedDiskLayout = list(lDiskLayout)
idxFront = 0
idxBack = len(lDiskLayout) - 1
iState = 0
while idxFront < idxBack:
	if iState == 0:
		if lRearrangedDiskLayout[idxFront] is None:
			iState = 1
		else:
			idxFront += 1
			iState = 0
	elif iState == 1:

