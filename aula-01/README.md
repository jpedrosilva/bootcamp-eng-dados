# Resultado

## Code
```python
# Bibliotecas (nesse caso apenas para o formato da moeda)
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Constante do acréscimo do bônus
CONST_BONUS = 1000

# Funções
def calc_bonus(salario: float, bonus: float):
    x = locale.currency(CONST_BONUS + salario * bonus, grouping=True)
    return print(f'Olá {nome}, o seu bônus foi de {x}.')

def check_nome(x: str):
    try:
        if len(x) <= 2 or not x.replace(' ', '').isalpha():
            raise Exception()
        else:
            return (x)
    except:
        raise Exception('Nome inválido, por favor, refaça a operação.')

def check_float(x: float):
    try:
        y = float(x.replace(',', '.'))
        if y < 0:
            raise Exception()
        else:
            return(y)
    except:
        raise Exception('Número inválido, por favor, refaça a operação.')

# Input de variáveis + check
nome = check_nome(input('Digite o seu nome: '))
salario = check_float(input('Digite o seu salário: '))
bonus = check_float(input('Digite o seu bônus: '))

# Run
calc_bonus(salario, bonus)
```

## Output
```
$ python kpi.py
Digite o seu nome: João Pedro
Digite o seu salário: 5000
Digite o seu bônus: 1,5
Olá João Pedro, o seu bônus foi de R$ 8.500,00.
```
