#! python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 23:59:06 2024

@author: TimBa
"""

import sys

with open('input.txt', 'r') as inF:
	lInputLines = inF.readlines()

lReports = []
for idxLine, sLine in enumerate(lInputLines):
	try:
		sLineS = sLine.strip()
		if len(sLineS) > 0:
			lEntries = sLineS.split(' ')
			lValues = []
			for idxE, sEntry in enumerate(lEntries):
				try:
					lValues.append(int(sEntry))
				except Exception as ex:
					raise type(ex)(f'{ex}\nwhile processing the {idxE + 1}-th value').with_traceback(sys.exc_info()[2])
			lReports.append(lValues)
	except Exception as ex:
		raise type(ex)(f'{ex}\nwhile processing the {idxLine + 1}-th line from file input.txt').with_traceback(sys.exc_info()[2])

lSafeReports = []
iMinAbsDiff = 1
iMaxAbsDiff = 3
for idxReport, lReport in enumerate(lReports):
	bIsSafe = True
	iReportDirection = None
	for idxValue in range(len(lReport) - 1):
		# Test the direction
		iDiff = lReport[idxValue + 1] - lReport[idxValue]
		if iDiff < 0:
			iDirection = -1
		elif iDiff == 0:
			iDirection = 0
		else:
			iDirection = 1
		if iReportDirection is None:
			iReportDirection = iDirection
		if iDirection == 0 or iReportDirection != iDirection:
			bIsSafe = False
			break
		# Test the step size
		if not (iMinAbsDiff <= abs(iDiff) <= iMaxAbsDiff):
			bIsSafe = False
			break
	if bIsSafe:
		lSafeReports.append((idxReport, lReport))

print(f'There are {len(lSafeReports)} safe reports found.')

lSafeReportsWithDampener = []
for idxReport, lReport in enumerate(lReports):
	for iVariant in range(len(lReport) + 1):
		if iVariant == 0:
			lReportToTest = lReport
		else:
			lReportToTest = lReport[:iVariant - 1] + lReport[iVariant:]
		bIsSafe = True
		iReportDirection = None
		for idxValue in range(len(lReportToTest) - 1):
			# Test the direction
			iDiff = lReportToTest[idxValue + 1] - lReportToTest[idxValue]
			if iDiff < 0:
				iDirection = -1
			elif iDiff == 0:
				iDirection = 0
			else:
				iDirection = 1
			if iReportDirection is None:
				iReportDirection = iDirection
			if iDirection == 0 or iReportDirection != iDirection:
				bIsSafe = False
				break
			# Test the step size
			if not (iMinAbsDiff <= abs(iDiff) <= iMaxAbsDiff):
				bIsSafe = False
				break
		if bIsSafe:
			lSafeReportsWithDampener.append((idxReport, lReportToTest))
			break


print(f'There are {len(lSafeReportsWithDampener)} safe reports with dampener found.')