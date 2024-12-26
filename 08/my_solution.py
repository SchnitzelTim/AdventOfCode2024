#! python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 25 21:53:07 2024

@author: TimBa
"""

from typing import Set, Tuple
import sys

with open('input.txt', 'r') as inF:
	iWidth = None
	iHeight = 0
	dictAntennaLocations = dict[str, Set[Tuple[int, int]]]()
	for idxLine, sLine in enumerate(inF):
		try:
			sLineS = sLine.strip()
			if len(sLineS) == 0:
				break
			if iWidth is None:
				iWidth = len(sLineS)
			elif iWidth != len(sLineS):
				raise ValueError('The line must have the same length as the other lines')
			iHeight += 1
			for idxColumn, ch in enumerate(sLineS):
				try:
					if ch == '.':
						pass
					elif ch.isalnum():
						lLocations = dictAntennaLocations.get(ch)
						if lLocations is None:
							lLocations = set[Tuple[int, int]]()
							dictAntennaLocations[ch] = lLocations
						lLocations.add((idxLine, idxColumn))
					else:
						raise ValueError('Unexpected character')
				except Exception as ex:
					raise type(ex)(f'{ex}\nwhile reading character {idxColumn + 1}').with_traceback(sys.exc_info()[2])
		except Exception as ex:
			raise type(ex)(f'{ex}\nwhile reading line {idxLine + 1} from file input.txt').with_traceback(sys.exc_info()[2])

lAntinodeLocations = set[Tuple[int, int]]()
for lLocations in dictAntennaLocations.values():
	lLocationsList = list(lLocations)
	for idxAntenna1 in range(len(lLocationsList)):
		for idxAntenna2 in range(len(lLocationsList)):
			if idxAntenna1 != idxAntenna2:
				tLocationAntenna1 = lLocationsList[idxAntenna1]
				tLocationAntenna2 = lLocationsList[idxAntenna2]
				tLocationAntinode = (2 * tLocationAntenna2[0] - tLocationAntenna1[0], 2 * tLocationAntenna2[1] - tLocationAntenna1[1])
				if tLocationAntinode[0] >= 0 and tLocationAntinode[0] < iHeight and tLocationAntinode[1] >= 0 and tLocationAntinode[1] < iWidth:
					lAntinodeLocations.add(tLocationAntinode)

print(f'Determined {len(lAntinodeLocations)} antinodes.')

lAntinodeLocations = set[Tuple[int, int]]()
for lLocations in dictAntennaLocations.values():
	lLocationsList = list(lLocations)
	for idxAntenna1 in range(len(lLocationsList)):
		for idxAntenna2 in range(len(lLocationsList)):
			if idxAntenna1 != idxAntenna2:
				tLocationAntenna1 = lLocationsList[idxAntenna1]
				tLocationAntenna2 = lLocationsList[idxAntenna2]
				tDifference = (tLocationAntenna2[0] - tLocationAntenna1[0], tLocationAntenna2[1] - tLocationAntenna1[1])
				tNextAntidoteLocation = (tLocationAntenna1[0] + tDifference[0], tLocationAntenna1[1] + tDifference[1])
				while tNextAntidoteLocation[0] >= 0 and tNextAntidoteLocation[0] < iHeight and tNextAntidoteLocation[1] >= 0 and tNextAntidoteLocation[1] < iWidth:
					lAntinodeLocations.add(tNextAntidoteLocation)
					tNextAntidoteLocation = (tNextAntidoteLocation[0] + tDifference[0], tNextAntidoteLocation[1] + tDifference[1])

print(f'Determined {len(lAntinodeLocations)} antinodes.')