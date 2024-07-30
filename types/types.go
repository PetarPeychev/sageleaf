package types

type Type interface {
	typeNode()
}

type I64 struct {
	Type
}

type None struct {
	Type
}

type Any struct {
	Type
}
