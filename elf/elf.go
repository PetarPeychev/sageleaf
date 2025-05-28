package elf

import (
	"debug/elf"
)

type File struct {
	Header   elf.FileHeader
	Programs []elf.Prog
}

func WriteElf(path string) {
	// header := elf.Header{
	// 	Class:      elf.ELFCLASS64,
	// 	Data:       elf.ELFDATA2LSB,
	// 	Type:       elf.ET_EXEC,
	// 	Machine:    elf.EM_X86_64,
	// 	Version:    elf.EV_CURRENT,
	// 	Entry:      0,
	// 	ProgHeader: nil,
	// 	Section:    nil,
	// 	Symtab:     nil,
	// }

	// f, err := elf.Create(path)
	// if err != nil {
	// 	panic(err)
	// }
}
