#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

struct Point {
    int x;
    int y;
};

int main() {
    // Declaración de variables (VarDec)
    struct Point point1;
    int result;
    int a = 5;
    int b = 3;

    // Asignación y llamada a función (StatementRest)
    point1.x = 10;
    point1.y = 20;
    result = add(a, b);

    // Bucle while (WhileStatement)
    while (result > 0) {
        printf("Resultado: %d\n", result);
        result = result - 1;
    }

    return 0;
}


/*

#include <stdio.h>

// Declaración de una estructura (TypeDec)
struct Point {
    int x;
    int y;
};

// Declaración de una función (FunctionDec)
int add(int a, int b) {
    return a + b;
}

int main() {
    // Declaración de variables (VarDec)
    struct Point point1;
    int result;
    int a = 5;
    int b = 3;

    // Asignación y llamada a función (StatementRest)
    point1.x = 10;
    point1.y = 20;
    result = add(a, b);

    // Bucle while (WhileStatement)
    while (result > 0) {
        printf("Resultado: %d\n", result);
        result--;
    }

    return 0;
}

*/