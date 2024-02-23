# Bibliotecas
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Constantes
CONST_BONUS: int = 1000

# Solicita a entrada do nome do usuário
def check_nome() -> str:
    check_nome: bool = True
    while check_nome:
        try:
            nome: str = input("Digite o seu nome: ")
            if len(nome) <= 2:
                raise Exception('É necessário que seja um nome válido.')
            elif not nome.replace(' ', '').isalpha():
                raise Exception('O nome deve conter apenas letras.')
            else:
                check_nome = False
        except Exception as e:
            print(e)
    return nome

# Solicita ao usuário o valor do salário
def check_salario() -> float:
    salario: float = None
    while salario is None:
        try:
            salario = float(input('Digite o valor do seu salário: '))
            if salario <= 0:
                raise ValueError('O salário deve ser um valor positivo.')
        except ValueError as e:
            print(e)
    return salario

# Solicita ao usuário o valor do bônus
def check_bonus() -> float:
    bonus: float = None
    while bonus is None:
        try:
            bonus = float(input('Digite o valor do seu bônus: ').replace(',', '.'))
            if bonus <= 0:
                raise ValueError('O bônus deve ser um valor positivo.')
        except ValueError as e:
            print(e)
    return bonus

# Função para cálculo do bônus
def calc_bonus(salario:float, bonus:float) -> float:
    return (CONST_BONUS + salario * bonus)

# Função da mensagem final
def mensagem() -> str:
    print(f'Olá {check_nome()}, o seu bônus é: {locale.currency(calc_bonus(check_salario(), check_bonus()), grouping=True)}')

def main():
    mensagem()

# Run
if __name__ == '__main__':
    main()
