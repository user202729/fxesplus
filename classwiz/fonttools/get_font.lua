-- Get classwiz calculator font.
-- Usage:
--   Set break addresses (depends on the calculator model)
--   Call main function.
--   Output is written to `out`.
--   Output file format: text file with '#' = on and ' ' = off.
-- Use to_png.py to convert output file to png.

function a(base)
	printf('"' ..
		(base>=0x100 and '%04X' or '  %02X')
		.. ':",', base)
	b()
	cpu.csr=0x0 cpu.pc=0x9132 -- after push lr of line_print

	for row=0,16 do
		for col=0,23 do
			data[0xe3d4+24*row+col]=0
		end
	end

	local sp=0xef00
	cpu.sp=sp

	local st=0xef20

	local adr=st
	for i=base,base+15 do
		if i&0xff==0 then
			data[adr]=0x20
			adr=adr+1
		elseif i>=0x100 then
			data[adr]=i>>8
			data[adr+1]=i&0xff
			adr=adr+2
		else
			data[adr]=i
			adr=adr+1
		end
	end

	cpu.r0=0
	cpu.r1=1
	cpu.r2=st&0xff
	cpu.r3=st>>8

	while cpu.csr~=0 or cpu.pc~=0x91a6 do
		--local old=cpu.csr<<16|cpu.pc
		emu:tick()
		--local new=cpu.csr<<16|cpu.pc
		--if old==new then
		--	printf('old=%x,new=%x,same',old,new)
		--	return
		--end
	end

	for row=0,16 do
		for col=0,23 do
			local bt=data[0xe3d4+24*row+col]
			for bit=7,0,-1 do
				fi:write(((bt>>bit)&1)==1 and '#' or ' ')
			end
		end
		fi:write('\n')
	end
	fi:flush()
end

function waitret(cb)
	local z=function()
		del(1)
		del(2)
		cb()
	end
	c()
	b(cpu.csr<<16|cpu.pc+2,z)
	b(cpu.csr<<16|cpu.pc+4,z)
end

function main()
	waitret(function()
		fi = io.open('out','w')
		for i=0x00,0xef,0x10 do a(i) end
		for i=0xf000,0xffff,0x10 do
			if i&0xff~=0xf0 then
				a(i)
			end
		end
		fi:close()
	end)
end
