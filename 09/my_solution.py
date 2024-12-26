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
		if lRearrangedDiskLayout[idxBack] is None:
			idxBack -= 1
			iState = 1
		else:
			if lRearrangedDiskLayout[idxFront] is None:
				lRearrangedDiskLayout[idxFront] = lRearrangedDiskLayout[idxBack]
				lRearrangedDiskLayout[idxBack] = None
				idxBack -= 1
				idxFront += 1
				iState = 0
			else:
				raise ValueError('The front block must be None at this point')
	else:
		raise ValueError('Unexpected state')

iChecksum = 0
for idxBlock, iBlockValue in enumerate(lRearrangedDiskLayout):
	if isinstance(iBlockValue, int):
		iChecksum += idxBlock * iBlockValue

print(f'The checksum after rearranging the disk layout is {iChecksum}.')

lRearrangedDiskLayout = list(lDiskLayout)
idxBack = len(lRearrangedDiskLayout) - 1
iFileID = None
idxFileEnd = None
idxFileStart = None
idxFront = 0
idxFreeSectionStart = None
idxFreeSectionEnd = None
iState = 0
lWasMoved = [False] * len(lRearrangedDiskLayout)
while idxBack > 0:
	if iState == 0: # Find the end of a file that was not moved yet
		if lRearrangedDiskLayout[idxBack] is None or lWasMoved[idxBack]:
			idxBack -= 1
			print('Back', idxBack)
			iState = 0
		else:
			iFileID = lRearrangedDiskLayout[idxBack]
			idxFileEnd = idxBack
			iState = 1
	elif iState == 1: # Find the start of the file
		if lRearrangedDiskLayout[idxBack] == iFileID:
			idxFileStart = idxBack
			idxBack -= 1
			print('Back', idxBack)
			iState = 1
		else:
			idxFront = 0
			iState = 2
	elif iState == 2: # Find next free block
		if lRearrangedDiskLayout[idxFront] is None:
			idxFreeSectionStart = idxFront
			iState = 3
		else:
			idxFront += 1
			if idxFront < idxFileStart:
				iState = 2
			else:
				iState = 0
	elif iState == 3: # Find the end of the free block
		if lRearrangedDiskLayout[idxFront] is None:
			idxFreeSectionEnd = idxFront
			idxFront += 1
			iState = 3
		else:
			if idxFreeSectionEnd - idxFreeSectionStart + 1 >= idxFileEnd - idxFileStart + 1:
				for idxFront in range(idxFileEnd - idxFileStart + 1):
					lRearrangedDiskLayout[idxFreeSectionStart + idxFront] = iFileID
					lWasMoved[idxFreeSectionStart + idxFront] = True
					lRearrangedDiskLayout[idxFileStart + idxFront] = None
				iState = 0
			else:
				iState = 2
	else:
		raise ValueError('Invalid state')

iChecksum = 0
for idxBlock, iBlockValue in enumerate(lRearrangedDiskLayout):
	if isinstance(iBlockValue, int):
		iChecksum += idxBlock * iBlockValue

print(f'The checksum after rearranging the disk layout is {iChecksum}.')