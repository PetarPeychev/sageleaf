package symbols

import (
	"errors"
	"sage/ast"
)

type Symbol struct {
	Type ast.Type
}

type SymbolTable struct {
	symbols map[string]Symbol
	parent  *SymbolTable
}

func New(parent *SymbolTable) *SymbolTable {
	return &SymbolTable{symbols: make(map[string]Symbol), parent: parent}
}

func (s *SymbolTable) Lookup(name string) (Symbol, error) {
	if s.symbols[name].Type != nil {
		return s.symbols[name], nil
	}
	if s.parent != nil {
		return s.parent.Lookup(name)
	}
	return Symbol{}, errors.New("symbol not found")
}
