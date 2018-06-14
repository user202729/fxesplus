function help()
	print([[
The supported functions are:

printf()        Print with format.
ins             Log all register values to the screen.
break_at        Set breakpoint. If input not specified, break at current address.
unbreak_at      Delete breakpoint.
																If input not specified, delete breakpoint at current address.
																Have no effect if there is no breakpoint at specified position.
cont()          Continue program execution.
inject          Inject 100 bytes to the input field.
pr_stack()      Print 48 bytes of the stack before and after SP.

emu:set_paused  Set emulator state.
emu:tick()      Execute one command.
emu:shutdown()  Shutdown the emulator.

cpu.xxx         Get register value.

code            Access code. (By words, only use even address, otherwise program will panic)
data            Access data. (By bytes)
]])
end

function print_number(address) -- Calculator's 10-byte decimal fp number as hex.
	local x = {};
	for i = 0,9,1 do
		table.insert(x, string.format("%02x", data[address+i]));
	end;
	print(table.concat(x, ' '));
end

p = print

function inject(str)
	if 200 ~= #str then
		print "Input 200 hexadecimal digits please"
		return
	end

	adr = 0x8154
	for byte in str:gmatch '..' do
		data[adr] = tonumber(byte, 16)
		adr = adr + 1
	end
end

function pr_stack(radius)
	radius = radius or 48

	sp = cpu.sp
	w = io.write
	linecnt = 0
	for i = sp-radius, sp+radius-1 do
		if i >= 0x8e00 then
			break
		end
		
		w(  ('%s%02x'):format(i==sp and '*' or ' ', data[i])  )
		linecnt = linecnt+1
		if linecnt==16 then
			w('\n')
			linecnt = 0
		end
	end
	p()
end

