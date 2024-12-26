#! python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 20:49:48 2024

@author: TimBa
"""

import sys
import math

with open('input.txt', 'r') as inF:
	lEquations = []
	for idxLine, sLine in enumerate(inF):
		try:
			iState = 0
			lParts = []
			lValueParts = []
			for idxCh, ch in enumerate(sLine):
				ch : str
				try:
					if iState == 0:
						if ch.isnumeric():
							lValueParts.append(ch)
							iState = 1
						elif ch == '\n':
							iState = 7
							break
						else:
							raise ValueError('Unexpected character')
					elif iState == 1:
						if ch.isnumeric():
							lValueParts.append(ch)
							iState = 1
						elif ch == ':':
							lParts.append(int(''.join(lValueParts)))
							lValueParts = []
							iState = 2
						else:
							raise ValueError('Unexpected character')
					elif iState == 2:
						if ch == ' ':
							iState = 2
						elif ch.isnumeric():
							lValueParts.append(ch)
							iState = 3
						else:
							raise ValueError('Unexpected character')
					elif iState == 3:
						if ch == ' ':
							lParts.append(int(''.join(lValueParts)))
							lValueParts = []
							iState = 4
						elif ch.isnumeric():
							lValueParts.append(ch)
							iState = 3
						elif ch == '\n':
							lParts.append(int(''.join(lValueParts)))
							iState = 6
						else:
							raise ValueError('Unexpected character')
					elif iState == 4:
						if ch == ' ':
							iState = 4
						elif ch.isnumeric():
							lValueParts.append(ch)
							iState = 5
						elif ch == '\n':
							iState = 6
						else:
							raise ValueError('Unexpected character')
					elif iState == 5:
						if ch == ' ':
							lParts.append(int(''.join(lValueParts)))
							lValueParts = []
							iState = 4
						elif ch.isnumeric():
							lValueParts.append(ch)
							iState = 5
						elif ch == '\n':
							lParts.append(int(''.join(lValueParts)))
							iState = 6
						else:
							raise ValueError('Unexpected character')
					else:
						raise ValueError('Unexpected state')
					if iState == 6:
						lEquations.append(lParts)
						break
					elif iState == 7:
						break
				except Exception as ex:
					raise type(ex)(f'{ex}\nwhile reading character {idxLine + 1} from the current line').with_traceback(sys.exc_info()[2])
			if iState in [0, 7]:
				break
			elif iState == 1:
				raise ValueError('Missing the colon after the test value')
			elif iState == 2:
				raise ValueError('Missing the 1st calibration value')
			elif iState in [3, 5]:
				lParts.append(int(''.join(lValueParts)))
				lEquations.append(lParts)
			elif iState == 4:
				lEquations.append(lParts)
			elif iState == 6:
				continue
			else:
				raise ValueError('Unexpected state')
		except Exception as ex:
			raise type(ex)(f'{ex}\nwhile reading line {idxLine + 1}').with_traceback(sys.exc_info()[2])

iSumTestValues = 0
for lEquation in lEquations:
	iTestValue = lEquation[0]
	iNumPossibilities = 1 << (len(lEquation) - 2)
	for idxPossibility in range(iNumPossibilities):
		iCalibrationValue = lEquation[1]
		for idxOperator in range(len(lEquation) - 2):
			iOperatorSelection = (idxPossibility >> idxOperator) & 1
			if iOperatorSelection == 0:
				iCalibrationValue += lEquation[2 + idxOperator]
			else:
				iCalibrationValue *= lEquation[2 + idxOperator]
		if iTestValue == iCalibrationValue:
			iSumTestValues += iTestValue
			break

print(f'The sum of the test values of the equations that could possibly true is {iSumTestValues}.')

iSumTestValues = 0
for idxEquation, lEquation in enumerate(lEquations):
	print(f'Testing equation {idxEquation + 1} / {len(lEquations)} equations...')
	iTestValue = lEquation[0]
	iNumPossibilities = 3**(len(lEquation) - 2)
	for idxPossibility in range(iNumPossibilities):
		iCalibrationValue = lEquation[1]
		for idxOperator in range(len(lEquation) - 2):
			iOperatorSelection = int(idxPossibility / 3**idxOperator) % 3
			if iOperatorSelection == 0:
				iCalibrationValue += lEquation[2 + idxOperator]
			elif iOperatorSelection == 1:
				iCalibrationValue *= lEquation[2 + idxOperator]
			elif iOperatorSelection == 2:
				iCalibrationValue = iCalibrationValue * 10**int(math.log10(lEquation[2 + idxOperator]) + 1) + lEquation[2 + idxOperator]
			else:
				raise ValueError('Invalid operator selection')
		if iTestValue == iCalibrationValue:
			iSumTestValues += iTestValue
			break

print(f'The sum of the test values of the equations that could possibly true is {iSumTestValues}.')