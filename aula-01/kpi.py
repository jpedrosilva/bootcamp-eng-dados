# Constante do acréscimo do bônus
CONST_BONUS = 1000

# Funções
def calc_bonus(salario: float, bonus: float):
    x = CONST_BONUS + salario * bonus
    return print(f'Olá {nome}, o seu bônus foi de R${x}')

def check_float(x):
    try:
        y = float(x.replace(',', '.'))
        if y < 0:
            raise Exception()
        else:
            return(y)
    except:
        raise Exception('Número inválido, por favor, refaça a operação.')

# Input de variáveis + check
nome = input('Digite o seu nome: ')
salario = check_float(input('Digite o seu salário: '))
bonus = check_float(input('Digite o seu bônus: '))

# Run
calc_bonus(salario, bonus)
