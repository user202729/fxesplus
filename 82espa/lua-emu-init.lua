require 'CasioEmu/emulator/lua-common'
dis_lines, line_by_addr, label_by_addr = readdis '82espa/disas.txt'
l_hl = {hl_start='\27[33;1m', -- bold yellow
	hl_stop='\27[0m', -- normal
	no_start='', no_stop=''}
