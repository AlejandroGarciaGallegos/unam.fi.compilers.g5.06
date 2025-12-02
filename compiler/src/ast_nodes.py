from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Tuple


class BasicType(Enum):
    INT = "int"
    FLOAT = "float"
    STRING = "string"


@dataclass
class CompileError(Exception):
    line: int
    message: str

    def __str__(self) -> str:
        # Estilo requerido: "error in line n ..."
        return f"error in line {self.line}: {self.message}"


@dataclass
class VarInfo:
    name: str
    type: BasicType
    value: Any


@dataclass
class ExecutionContext:
    symbols: Dict[str, VarInfo] = field(default_factory=dict)

    def declare(self, name: str, var_type: BasicType, value: Any, line: int) -> None:
        if name in self.symbols:
            raise CompileError(line, f"variable '{name}' already declared")
        self.symbols[name] = VarInfo(name, var_type, value)

    def assign(self, name: str, value: Any, value_type: BasicType, line: int) -> None:
        if name not in self.symbols:
            raise CompileError(line, f"variable '{name}' not declared")
        var = self.symbols[name]

        if var.type == BasicType.INT:
            if value_type == BasicType.FLOAT:
                raise CompileError(line, f"cannot assign float to int variable '{name}'")
            if value_type != BasicType.INT:
                raise CompileError(line, f"cannot assign non-numeric value to int variable '{name}'")
            var.value = int(value)
        elif var.type == BasicType.FLOAT:
            if value_type not in (BasicType.INT, BasicType.FLOAT):
                raise CompileError(line, f"cannot assign non-numeric value to float variable '{name}'")
            var.value = float(value)
        else:
            var.value = value

    def lookup(self, name: str, line: int) -> VarInfo:
        if name not in self.symbols:
            raise CompileError(line, f"variable '{name}' not declared")
        return self.symbols[name]

@dataclass
class Node:
    line: int


@dataclass
class Statement(Node):
    def execute(self, ctx: ExecutionContext) -> None:
        raise NotImplementedError


@dataclass
class Expr(Node):
    def eval(self, ctx: ExecutionContext) -> Tuple[BasicType, Any]:
        raise NotImplementedError

@dataclass
class Program(Node):
    statements: List[Statement] = field(default_factory=list)

    def execute(self, ctx: ExecutionContext) -> None:
        for stmt in self.statements:
            stmt.execute(ctx)


@dataclass
class VarDecl(Statement):
    name: str
    var_type: BasicType
    expr: Expr

    def execute(self, ctx: ExecutionContext) -> None:
        expr_type, expr_val = self.expr.eval(ctx)

        if self.var_type == BasicType.INT:
            if expr_type == BasicType.FLOAT:
                raise CompileError(self.line, f"cannot assign float to int variable '{self.name}'")
            if expr_type != BasicType.INT:
                raise CompileError(self.line, f"cannot assign non-numeric value to int variable '{self.name}'")
            value = int(expr_val)
        elif self.var_type == BasicType.FLOAT:
            if expr_type not in (BasicType.INT, BasicType.FLOAT):
                raise CompileError(self.line, f"cannot assign non-numeric value to float variable '{self.name}'")
            value = float(expr_val)
        else:
            value = expr_val

        ctx.declare(self.name, self.var_type, value, self.line)


@dataclass
class Assign(Statement):
    name: str
    expr: Expr

    def execute(self, ctx: ExecutionContext) -> None:
        expr_type, expr_val = self.expr.eval(ctx)
        ctx.assign(self.name, expr_val, expr_type, self.line)


@dataclass
class Print(Statement):
    expr: Expr

    def execute(self, ctx: ExecutionContext) -> None:
        expr_type, expr_val = self.expr.eval(ctx)
        # Para el proyecto basta con imprimir el valor crudo
        print(expr_val)

@dataclass
class Literal(Expr):
    value: Any
    lit_type: BasicType

    def eval(self, ctx: ExecutionContext) -> Tuple[BasicType, Any]:
        return self.lit_type, self.value


@dataclass
class Var(Expr):
    name: str

    def eval(self, ctx: ExecutionContext) -> Tuple[BasicType, Any]:
        var = ctx.lookup(self.name, self.line)
        return var.type, var.value


@dataclass
class BinOp(Expr):
    op: str
    left: Expr
    right: Expr

    def eval(self, ctx: ExecutionContext) -> Tuple[BasicType, Any]:
        lt, lv = self.left.eval(ctx)
        rt, rv = self.right.eval(ctx)

        if lt not in (BasicType.INT, BasicType.FLOAT) or rt not in (BasicType.INT, BasicType.FLOAT):
            raise CompileError(self.line, f"binary operator '{self.op}' not supported for non-numeric types")

        if self.op == '/':
            if rv == 0:
                raise CompileError(self.line, "division by zero")
            result_type = BasicType.FLOAT
            result_val = float(lv) / float(rv)
        else:
            result_type = BasicType.FLOAT if BasicType.FLOAT in (lt, rt) else BasicType.INT
            if self.op == '+':
                result_val = lv + rv
            elif self.op == '-':
                result_val = lv - rv
            elif self.op == '*':
                result_val = lv * rv
            else:
                raise CompileError(self.line, f"unknown binary operator '{self.op}'")

            if result_type == BasicType.INT:
                result_val = int(result_val)
            else:
                result_val = float(result_val)

        return result_type, result_val


@dataclass
class UnaryOp(Expr):
    op: str
    operand: Expr

    def eval(self, ctx: ExecutionContext) -> Tuple[BasicType, Any]:
        t, v = self.operand.eval(ctx)
        if t not in (BasicType.INT, BasicType.FLOAT):
            raise CompileError(self.line, f"unary operator '{self.op}' not supported for non-numeric type")
        if self.op == '-':
            v = -v
        else:
            raise CompileError(self.line, f"unknown unary operator '{self.op}'")
        return t, v
