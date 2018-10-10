#!/usr/bin/env python3
import sys
from code_check import CodeCheck
def main():
    code_checker = CodeCheck("model1.py", 15)
    print('reach')
    if not code_checker.check_code():
        print(code_checker.errormsg)
        print('wrong answer')
    else:
        print('pass')
        
if __name__ == '__main__':
	main()
