package symbols

import (
	"errors"
	"sage/types"
)

type Symbol struct {
	Type types.Type
}

type Table struct {
	symbols map[string]Symbol
	parent  *Table
}

func New(parent *Table) *Table {
	return &Table{symbols: make(map[string]Symbol), parent: parent}
}

func (s *Table) Lookup(name string) (Symbol, error) {
	if s.symbols[name].Type != nil {
		return s.symbols[name], nil
	}
	if s.parent != nil {
		return s.parent.Lookup(name)
	}
	return Symbol{}, errors.New("symbol not found")
}

func (s *Table) Define(name string, type_ types.Type) {
	s.symbols[name] = Symbol{Type: type_}
}
