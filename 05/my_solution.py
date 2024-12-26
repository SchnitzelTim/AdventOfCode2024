#! python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 23:22:09 2024

@author: TimBa
"""

from typing import Tuple, List
import re
import sys

lOrderingRules = set[Tuple[int, int]]()
lUpdates = list[List[int]]()
reOrderingRule = re.compile(r'(?P<PageNum1>\d+)\|(?P<PageNum2>\d+)')
with open('input.txt', 'r') as inF:
	try:
		iState = 0
		for idxLine, sLine in enumerate(inF):
			try:
				sLineS = sLine.strip()
				if iState == 0 or iState == 1:
					m = reOrderingRule.fullmatch(sLineS)
					if m:
						tOrderingRule = (int(m['PageNum1']), int(m['PageNum2']))
						lOrderingRules.add(tOrderingRule)
						iState = 1
					elif len(sLineS) == 0:
						iState = 2
					else:
						raise ValueError('Unexpected line contents')
				elif iState == 2:
					lRawValues = sLineS.split(',')
					lValues = []
					for idxRawValue, sRawValue in enumerate(lRawValues):
						try:
							lValues.append(int(sRawValue))
						except Exception as ex:
							raise type(ex)(f'{ex}\nwhile reading the {idxRawValue + 1}-th value from the line contents').with_traceback(sys.exc_info()[2])
					lUpdates.append(lValues)
				else:
					raise ValueError('Unexpected state')
			except Exception as ex:
				raise type(ex)(f'{ex}\nwhile processing line {idxLine + 1}').with_traceback(sys.exc_info()[2])
		if iState == 0:
			raise ValueError('Missing the definition of any ordering rule')
		elif iState == 1:
			raise ValueError('Missing the definitions of the updates')
	except Exception as ex:
		raise type(ex)(f'{ex}\nwhile reading the input file').with_traceback(sys.exc_info()[2])

iSum = 0
lUpdateIsFine = []
for lUpdate in lUpdates:
	bUpdateIsFine = True
	for tOrderingRule in lOrderingRules:
		if tOrderingRule[0] in lUpdate and tOrderingRule[1] in lUpdate:
			idxFirst = lUpdate.index(tOrderingRule[0])
			idxSecond = lUpdate.index(tOrderingRule[1])
			if idxFirst > idxSecond:
				bUpdateIsFine = False
				break
	lUpdateIsFine.append(bUpdateIsFine)
	if bUpdateIsFine:
		iIdxMid = int((len(lUpdate) - 0.5) // 2)
		iSum += lUpdate[iIdxMid]

print(f'The sum of the central page numbers of all well-formed updates is {iSum}.')

iSum = 0
iMaxReorderTries = 10
for bUpdateIsFine, lUpdate in zip(lUpdateIsFine, lUpdates):
	if not bUpdateIsFine:
		lUpdateNewOrder = list(lUpdate)
		iIdxTry = 0
		while not bUpdateIsFine and iIdxTry < iMaxReorderTries:
			bUpdateIsFine = True
			for tOrderingRule in lOrderingRules:
				if tOrderingRule[0] in lUpdateNewOrder and tOrderingRule[1] in lUpdateNewOrder:
					idxFirst = lUpdateNewOrder.index(tOrderingRule[0])
					idxSecond = lUpdateNewOrder.index(tOrderingRule[1])
					if idxFirst > idxSecond:
						lUpdateNewOrder = lUpdateNewOrder[:idxSecond] + [lUpdateNewOrder[idxFirst]] + lUpdateNewOrder[idxSecond:idxFirst] + lUpdateNewOrder[idxFirst + 1:]
						bUpdateIsFine = False
			iIdxTry += 1
		if bUpdateIsFine:
			iIdxMid = int((len(lUpdateNewOrder) - 0.5) // 2)
			iSum += lUpdateNewOrder[iIdxMid]
		else:
			raise RecursionError('Exhausted the reordering tries')

print(f'The sum of the central page numbers of all reordered badly ordered updates is {iSum}.')