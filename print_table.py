def print_table(symbols,ncol=16):
	colwidth = [1]*ncol
	for i,sym in enumerate(symbols):
		colwidth[i%ncol] = max(colwidth[i%ncol], len(sym))
	for i,sym in enumerate(symbols):
		print(sym.ljust(colwidth[i%ncol]), end=' ')
		if (i+1)%ncol == 0: print()
	print()

