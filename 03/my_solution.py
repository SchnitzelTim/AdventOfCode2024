#! python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 21:32:37 2024

@author: TimBa
"""

import re

with open('input.txt', 'r') as inF:
	sInput = inF.read()

reMul = re.compile(r'mul\((?P<Operand1>\d{1,3}),(?P<Operand2>\d{1,3})\)')

iSum = 0
itM = reMul.finditer(sInput)
for m in itM:
	iOperand1 = int(m['Operand1'])
	iOperand2 = int(m['Operand2'])
	iSum += iOperand1 * iOperand2

print(f'The sum of all multiplications is {iSum}.')

reInstruction = re.compile(r'(?P<Multiplication>mul)\((?P<Operand1>\d{1,3}),(?P<Operand2>\d{1,3})\)|(?P<Enable>do)\(\)|(?P<Disable>don\'t)\(\)')
iSum = 0
bMultiplicationEnabled = True
itM = reInstruction.finditer(sInput)
for m in itM:
	if m['Multiplication']:
		if bMultiplicationEnabled:
			iOperand1 = int(m['Operand1'])
			iOperand2 = int(m['Operand2'])
			iSum += iOperand1 * iOperand2
	elif m['Enable']:
		bMultiplicationEnabled = True
	elif m['Disable']:
		bMultiplicationEnabled = False

print(f'The sum of all enabled multiplications is {iSum}.')