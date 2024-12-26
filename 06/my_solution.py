#! python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 15:03:38 2024

@author: TimBa
"""

import sys
from typing import Tuple
import copy

class TRobotState:
	_rowIndex : int
	_columnIndex : int
	_orientation : int

	def __init__(self, rowIndex : int = 0, columnIndex : int = 0, orientation : int = 0):
		# Parameter rowIndex
		try:
			self.rowIndex = rowIndex
		except Exception as ex:
			raise type(ex)(f'{ex}\nwhile setting property rowIndex to the value in parameter rowIndex').with_traceback(sys.exc_info()[2])
		# Parameter columnIndex
		try:
			self.columnIndex = columnIndex
		except Exception as ex:
			raise type(ex)(f'{ex}\nwhile setting property columnIndex to the value in parameter columnIndex').with_traceback(sys.exc_info()[2])
		# Parameter orientation
		try:
			self.orientation = orientation
		except Exception as ex:
			raise type(ex)(f'{ex}\nwhile setting property orientation to the value in parameter orientation').with_traceback(sys.exc_info()[2])

	@property
	def rowIndex(self) -> int:
		return self._rowIndex

	@rowIndex.setter
	def rowIndex(self, newValue : int):
		if isinstance(newValue, int):
			self._rowIndex = newValue
		else:
			raise TypeError('Parameter newValue must contain an integer')

	@property
	def columnIndex(self) -> int:
		return self._columnIndex

	@columnIndex.setter
	def columnIndex(self, newValue : int):
		if isinstance(newValue, int):
			self._columnIndex = newValue
		else:
			raise TypeError('Parameter newValue must contain an integer')

	@property
	def orientation(self) -> int:
		return self._orientation

	@orientation.setter
	def orientation(self, newValue : int):
		if isinstance(newValue, int):
			self._orientation = newValue % 4
		else:
			raise TypeError('Parameter newValue must contain an integer')

	def move(self):
		if self._orientation == 0:
			self._rowIndex -= 1
		elif self._orientation == 1:
			self._columnIndex += 1
		elif self._orientation == 2:
			self._rowIndex += 1
		elif self._orientation == 3:
			self._columnIndex -= 1
		else:
			raise ValueError('Invalid orientation value')

	def isInsideDimensions(self, rowIndexMinimum : int, rowIndexMaximum : int, columnIndexMinimum : int, columnIndexMaximum : int) -> bool:
		# Parameter rowIndexMinimum
		if not isinstance(rowIndexMinimum, int):
			raise TypeError('Parameter rowIndexMinimum must be an integer')
		# Parameter rowIndexMaximum
		if not isinstance(rowIndexMaximum, int):
			raise TypeError('Parameter rowIndexMaximum must be an integer')
		if rowIndexMaximum < rowIndexMinimum:
			raise ValueError('The value in parameter rowIndexMaximum must be greater or equal to the value in parameter rowIndexMinimum')
		# Parameter columnIndexMinimum
		if not isinstance(columnIndexMinimum, int):
			raise TypeError('Parameter columnIndexMinimum must be an integer')
		# Parameter columnIndexMaximum
		if not isinstance(columnIndexMaximum, int):
			raise TypeError('Parameter columnIndexMaximum must be an integer')
		if columnIndexMaximum < columnIndexMinimum:
			raise ValueError('The value in parameter columnIndexMaximum must be greater or equal to the value in parameter columnIndexMinimum')
		# Normal code
		return rowIndexMinimum <= self._rowIndex and self._rowIndex <= rowIndexMaximum and columnIndexMinimum <= self._columnIndex and self._columnIndex <= columnIndexMaximum

	def __repr__(self) -> str:
		return f'{type(self).__name__}(rowIndex = {self._rowIndex}, columnIndex = {self._columnIndex}, orientation = {self._orientation})'

	def __copy__(self) -> 'TRobotState':
		return TRobotState(self.rowIndex, self.columnIndex, self.orientation)

with open('input.txt', 'r') as inF:
	lMap = []
	iWidth = None
	rsRobot = None
	for idxLine, sLine in enumerate(inF):
		try:
			sLineS = sLine.strip()
			lMapRow = []
			for idxCol, ch in enumerate(sLineS):
				try:
					if ch in '.#':
						lMapRow.append(ch)
					elif ch == '^':
						lMapRow.append('.')
						rsRobot = TRobotState(idxLine, idxCol)
					else:
						raise ValueError('Unexpected character')
				except Exception as ex:
					raise type(ex)(f'{ex}\while parsing the character in column {idxCol + 1}').with_traceback(sys.exc_info()[2])
			if iWidth is None:
				iWidth = len(lMapRow)
			elif len(lMapRow) != iWidth:
				raise ValueError('The row must not have a different length than the previous rows')
			lMap.append(''.join(lMapRow))
		except Exception as ex:
			raise type(ex)(f'{ex}\nwhile reading line {idxLine + 1} from file input.txt').with_traceback(sys.exc_info()[2])
rsInitialRobotState = copy.copy(rsRobot)

lVisitedCoords = set[Tuple[int, int]]()
lRobotStateHistory = set[Tuple[int, int, int]]()
while rsRobot.isInsideDimensions(0, len(lMap) - 1, 0, iWidth - 1) and not (rsRobot.rowIndex, rsRobot.columnIndex, rsRobot.orientation) in lRobotStateHistory:
	lVisitedCoords.add((rsRobot.rowIndex, rsRobot.columnIndex))
	lRobotStateHistory.add((rsRobot.rowIndex, rsRobot.columnIndex, rsRobot.orientation))
	rsRobotNew = copy.copy(rsRobot)
	rsRobotNew.move()
	if rsRobotNew.isInsideDimensions(0, len(lMap) - 1, 0, iWidth - 1):
		if lMap[rsRobotNew.rowIndex][rsRobotNew.columnIndex] == '.':
			rsRobot = rsRobotNew
		else:
			rsRobot.orientation += 1
	else:
		rsRobot = rsRobotNew

print(f'The number of visited map locations is {len(lVisitedCoords)}.')

# if not rsRobot.isInsideDimensions(0, len(lMap) - 1, 0, iWidth - 1):
# 	print('The simulation shows that the robot exits the map sooner or later. Therefore, The Historians ask to determine all possible locations to place an obstacle in the way that the robot then wanders around indefinitely in a loop on the map. Searching for these possibilities now.')

# 	lTestedLocations = set[Tuple[int, int]]()
# 	lObstacleLocations = set[Tuple[int, int]]()
# 	lBaselineRobotStateHistory = lRobotStateHistory
# 	for idxRow, idxCol, _ in lBaselineRobotStateHistory:
# 		if not (idxRow, idxCol) in lTestedLocations:
# 			if not (idxRow == rsInitialRobotState.rowIndex and idxCol == rsInitialRobotState.columnIndex):
# 				if lMap[idxRow][idxCol] == '.':
# 					print(f'Testing location {idxRow}, {idxCol} with {len(lMap)} rows and {iWidth} columns...')
# 					lMap2 = copy.deepcopy(lMap)
# 					lMap2[idxRow] = lMap[idxRow][:idxCol] + '#' + lMap[idxRow][idxCol + 1:]
# 					rsRobot = rsInitialRobotState
# 					lRobotStateHistory = set[Tuple[int, int, int]]()
# 					while rsRobot.isInsideDimensions(0, len(lMap2) - 1, 0, iWidth - 1) and not (rsRobot.rowIndex, rsRobot.columnIndex, rsRobot.orientation) in lRobotStateHistory:
# 						lRobotStateHistory.add((rsRobot.rowIndex, rsRobot.columnIndex, rsRobot.orientation))
# 						rsRobotNew = copy.copy(rsRobot)
# 						rsRobotNew.move()
# 						if rsRobotNew.isInsideDimensions(0, len(lMap2) - 1, 0, iWidth - 1):
# 							if lMap2[rsRobotNew.rowIndex][rsRobotNew.columnIndex] == '.':
# 								rsRobot = rsRobotNew
# 							else:
# 								rsRobot.orientation += 1
# 						else:
# 							rsRobot = rsRobotNew
# 					if rsRobotNew.isInsideDimensions(0, len(lMap2) - 1, 0, iWidth - 1):
# 						lObstacleLocations.add((idxRow, idxCol))
# 						print('Determined that an obstacle in this location will make the guard loop over and over again.')
# 					else:
# 						print('Determined that an obstacle in this location will not make the guard loop over and over again.')
# 					lTestedLocations.add((idxRow, idxCol))

# 	print(f'Found {len(lObstacleLocations)} locations to place an obstacle that causes the guard to loop indefinitely at some point in his life.')


if not rsRobot.isInsideDimensions(0, len(lMap) - 1, 0, iWidth - 1):
	print('The simulation shows that the robot exits the map sooner or later. Therefore, The Historians ask to determine all possible locations to place an obstacle in the way that the robot then wanders around indefinitely in a loop on the map. Searching for these possibilities now.')

	lObstacleLocations = set[Tuple[int, int]]()
	for idxRow in range(len(lMap)):
		for idxCol in range(iWidth):
			if idxRow == rsInitialRobotState.rowIndex and idxCol == rsInitialRobotState.columnIndex:
				continue
			if lMap[idxRow][idxCol] == '.':
				print(f'Testing location {idxRow}, {idxCol} with {len(lMap)} rows and {iWidth} columns...')
				lMap2 = copy.deepcopy(lMap)
				lMap2[idxRow] = lMap[idxRow][:idxCol] + 'O' + lMap[idxRow][idxCol + 1:]
				rsRobot = copy.copy(rsInitialRobotState)
				lRobotStateHistory = set[Tuple[int, int, int]]()
				while rsRobot.isInsideDimensions(0, len(lMap2) - 1, 0, iWidth - 1) and not (rsRobot.rowIndex, rsRobot.columnIndex, rsRobot.orientation) in lRobotStateHistory:
					lRobotStateHistory.add((rsRobot.rowIndex, rsRobot.columnIndex, rsRobot.orientation))
					rsRobotNew = copy.copy(rsRobot)
					rsRobotNew.move()
					if rsRobotNew.isInsideDimensions(0, len(lMap2) - 1, 0, iWidth - 1):
						if lMap2[rsRobotNew.rowIndex][rsRobotNew.columnIndex] == '.':
							rsRobot = rsRobotNew
						else:
							rsRobot.orientation += 1
					else:
						rsRobot = rsRobotNew
				if (rsRobot.rowIndex, rsRobot.columnIndex, rsRobot.orientation) in lRobotStateHistory:
					lObstacleLocations.add((idxRow, idxCol))
					# print('Determined that an obstacle in this location will make the guard loop over and over again.')
# 				else:
# 					print('Determined that an obstacle in this location will not make the guard loop over and over again.')

	print(f'Found {len(lObstacleLocations)} locations to place an obstacle that causes the guard to loop indefinitely at some point in his life.\b')
