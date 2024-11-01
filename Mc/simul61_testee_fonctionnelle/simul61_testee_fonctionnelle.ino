#include <Arduino.h>

const int MAX_INPUTS = 8;
const int MAX_OUTPUTS = 6;

const int inputPins[MAX_INPUTS] = {22, 23, 24, 25, 26, 27, 28, 29};  // Broches pour I1 à I8
const int outputPins[MAX_OUTPUTS] = {32, 33, 34, 35, 36, 37};        // Broches pour O1 à O6

String logicExpressions[MAX_OUTPUTS];

void setup() {
  Serial.begin(115200);
  Serial.println("Je démarre");
  for (int i = 0; i < MAX_INPUTS; i++) {
    pinMode(inputPins[i], INPUT);
  }
  for (int i = 0; i < MAX_OUTPUTS; i++) {
    pinMode(outputPins[i], OUTPUT);
    digitalWrite(outputPins[i], LOW);
  }
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    Serial.println(input);
    parseMultipleExpressions(input);
  }
  updateOutputs();
}

void resetOutputs() {
  for (int i = 0; i < MAX_OUTPUTS; i++) {
    logicExpressions[i] = "";
    digitalWrite(outputPins[i], LOW);
  }
}

void parseMultipleExpressions(String input) {
  resetOutputs();
  input.trim();
  int start = 0;
  while (start < input.length()) {
    int end = input.indexOf(';', start);
    if (end == -1) {
      end = input.length();
    }
    String expression = input.substring(start, end);
    parseExpression(expression);
    start = end + 1;
  }
}

void parseExpression(String input) {
  input.trim();
  int eqIndex = input.indexOf('=');
  if (eqIndex != -1 && input.startsWith("O")) {
    int outputIndex = input.substring(1, eqIndex).toInt() - 1;
    if (outputIndex >= 0 && outputIndex < MAX_OUTPUTS) {
      logicExpressions[outputIndex] = input.substring(eqIndex + 1);
    }
  }
}

bool evaluateExpression(String expr) {
  expr.trim();
  expr.replace(" ", "");
  for (int i = 0; i < MAX_INPUTS; i++) {
    expr.replace("!I" + String(i + 1), String(!digitalRead(inputPins[i])));
    expr.replace("I" + String(i + 1), String(digitalRead(inputPins[i])));
  }
  return evaluateComplexExpression(expr);
}

bool evaluateComplexExpression(String expr) {
  struct Stack {
    bool values[64];
    char operators[64];
    int valueTop = -1;
    int operatorTop = -1;

    void pushValue(bool value) {
      values[++valueTop] = value;
    }

    bool popValue() {
      return values[valueTop--];
    }

    void pushOperator(char op) {
      operators[++operatorTop] = op;
    }

    char popOperator() {
      return operators[operatorTop--];
    }

    char peekOperator() {
      return operators[operatorTop];
    }

    bool isOperatorStackEmpty() {
      return operatorTop == -1;
    }
  } stack;

  for (int i = 0; i < expr.length(); i++) {
    char c = expr.charAt(i);

    if (c == '0' || c == '1') {
      stack.pushValue(c == '1');
    } else if (c == '(') {
      stack.pushOperator(c);
    } else if (c == ')') {
      while (!stack.isOperatorStackEmpty() && stack.peekOperator() != '(') {
        char op = stack.popOperator();
        bool val2 = stack.popValue();
        bool val1 = (op == '!') ? false : stack.popValue();
        stack.pushValue(applyOperator(val1, val2, op));
      }
      stack.popOperator();
    } else if (c == '&' || c == '|' || c == '!' || c == '^') {
      while (!stack.isOperatorStackEmpty() && stack.peekOperator() != '(' && precedence(stack.peekOperator()) >= precedence(c)) {
        char op = stack.popOperator();
        bool val2 = stack.popValue();
        bool val1 = (op == '!') ? false : stack.popValue();
        stack.pushValue(applyOperator(val1, val2, op));
      }
      stack.pushOperator(c);
    }
  }

  while (!stack.isOperatorStackEmpty()) {
    char op = stack.popOperator();
    bool val2 = stack.popValue();
    bool val1 = (op == '!') ? false : stack.popValue();
    stack.pushValue(applyOperator(val1, val2, op));
  }

  return stack.popValue();
}

bool applyOperator(bool a, bool b, char op) {
  if (op == '&') return a && b;
  if (op == '|') return a || b;
  if (op == '^') return a != b;
  if (op == '!') return !b;
  return false;
}

int precedence(char op) {
  if (op == '!') return 4;
  if (op == '&') return 3;
  if (op == '^') return 2;
  if (op == '|') return 1;
  return 0;
}

void updateOutputs() {
  for (int i = 0; i < MAX_OUTPUTS; i++) {
    if (logicExpressions[i] != "") {
      bool outputValue = evaluateExpression(logicExpressions[i]);
      if (outputValue) {
        digitalWrite(outputPins[i], HIGH);
      } else {
        digitalWrite(outputPins[i], LOW);
      }
    }
  }
}
