#! python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 22:33:59 2024

@author: TimBa
"""

with open('input.txt', 'r') as inF:
	lInputLines = inF.readlines()

iWidth = None
for sLine in lInputLines:
	iLen = len(sLine.strip())
	if iLen > 0:
		if iWidth is None or iLen < iWidth:
			iWidth = iLen
print(f'The input consists of {len(lInputLines)} lines and {iWidth} columns.')

sSearchWord = 'XMAS'
iTimesFound = 0
lAllowedDirections = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
for idxLine in range(len(lInputLines)):
	for idxColumn in range(iWidth):
		bOtherDirectionsPossible = True
		for tDirection in lAllowedDirections:
			bFound = True
			for idxChar, ch in enumerate(sSearchWord):
				idxLineToCheck = idxLine + tDirection[0] * idxChar
				idxColumnToCheck = idxColumn + tDirection[1] * idxChar
				if idxLineToCheck < 0 or idxLineToCheck >= len(lInputLines):
					bFound = False
					break
				if idxColumnToCheck < 0 or idxColumnToCheck >= iWidth:
					bFound = False
					break
				chToCheck = lInputLines[idxLineToCheck][idxColumnToCheck]
				if chToCheck != ch:
					bFound = False
					if idxChar == 0:
						bOtherDirectionsPossible = False
					break
			if bFound:
				iTimesFound += 1
			elif not bOtherDirectionsPossible:
				break

print(f'Found the search word "{sSearchWord}" {iTimesFound} times in the input.')

sSearchWord = 'MAS'
iTimesFound = 0
lDirections = [[(1, 1), (-1, -1)], [(1, -1), (-1, 1)]]
for idxLine in range(len(lInputLines)):
	for idxColumn in range(iWidth):
		bPatternFound = False
		for lThisDirections in lDirections:
			bThisPartFound = False
			for tDirection in lThisDirections:
				bPatternMatched = True
				for idxCh, ch in enumerate(sSearchWord):
					idxLineToCheck = idxLine + tDirection[0] * (idxCh - len(sSearchWord) // 2)
					idxColumnToCheck = idxColumn + tDirection[1] * (idxCh - len(sSearchWord) // 2)
					if idxLineToCheck < 0 or idxLineToCheck >= len(lInputLines):
						bPatternMatched = False
						break
					if idxColumnToCheck < 0 or idxColumnToCheck >= iWidth:
						bPatternMatched = False
						break
					chToCheck = lInputLines[idxLineToCheck][idxColumnToCheck]
					if chToCheck != ch:
						bPatternMatched = False
						break
				if bPatternMatched:
					bThisPartFound = True
					break
			if bThisPartFound:
				bPatternFound = True
			else:
				bPatternFound = False
				break
		if bPatternFound:
			iTimesFound += 1

print(f'Found the X-MAS pattern {iTimesFound} times in the input.')
