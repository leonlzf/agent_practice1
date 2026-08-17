from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel

from governed_banking_agent.schemas.enums import ToolStatus
from governed_banking_agent.schemas.tools import ToolResult


class Operation(StrEnum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculatorInput(BaseModel):
    operation: Operation
    left: Decimal
    right: Decimal


class PolicyCalculatorTool:
    name = "policy_calculator"
    input_model = CalculatorInput

    def invoke(self, arguments: dict[str, object]) -> ToolResult:
        operation = Operation(arguments["operation"])
        left = Decimal(arguments["left"])
        right = Decimal(arguments["right"])

        if operation == Operation.ADD:
            value = left + right
        elif operation == Operation.SUBTRACT:
            value = left - right
        elif operation == Operation.MULTIPLY:
            value = left * right
        else:
            if right == 0:
                return ToolResult(
                    name=self.name,
                    status=ToolStatus.ERROR,
                    error="Division by zero is not allowed.",
                )
            value = left / right

        return ToolResult(
            name=self.name,
            status=ToolStatus.SUCCESS,
            output={
                "operation": operation,
                "left": str(left),
                "right": str(right),
                "result": str(value),
            },
        )

