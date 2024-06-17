medicos = {}
pacientes = {}

def listar_medico():
    if medicos:
        print("Lista de médicos:")
        for codigo, (nome, especialidade, crm, telefone) in medicos.items():
            print(f"Código: {codigo}, Nome: {nome}, Especialidade: {especialidade}, CRM: {crm}, Telefone: {telefone}")
    else:
        print("Não há médicos registrados! Tente adicionar algum médico!")


def pesquisar_medico():
    try:
        codigo = int(input("Digite o código do médico que deseja pesquisar: ").strip())
        if codigo in medicos:
            nome, especialidade, crm, telefone = medicos[codigo]
            print(f"Médico encontrado: Código: {codigo}, Nome: {nome}, Especialidade: {especialidade}, CRM: {crm}, Telefone: {telefone}")
        else:
            print("Médico não encontrado.")
    except ValueError:
        print("Código inválido. Por favor, digite um número inteiro.")


def adicionar_medico():
    try:
        codigo = int(input("Digite o código do médico: ").strip())
        if codigo in medicos:
            print("Erro: Já existe um médico registrado com este código.")
            return
        nome = input("Digite o nome do médico: ").strip().title()
        especialidade = input("Digite a especialidade do médico: ").strip().title()
        crm = input("Digite o CRM do médico: ").strip()
        telefone = input("Digite o telefone do médico: ").strip()
        medicos[codigo] = (nome, especialidade, crm, telefone)
        print("Médico adicionado com sucesso!")
    except ValueError:
        print("Código inválido. Por favor, digite um número inteiro.")


def remover_medico():
    if medicos:
        try:
            codigo = int(input("Digite o código do médico a ser removido: ").strip())
            if codigo in medicos:
                del medicos[codigo]
                print("Médico removido com sucesso!")
            else:
                print("Código não encontrado!")
        except ValueError:
            print("Código inválido. Por favor, digite um número inteiro.")
    else:
        print("Não há médicos registrados!")


def listar_paciente():
    if pacientes:
        print("Lista de pacientes:")
        for cpf, (nome, idade, endereco, telefone) in pacientes.items():
            print(f"CPF: {cpf}, Nome: {nome}, Idade: {idade}, Endereço: {endereco}, Telefone: {telefone}")
    else:
        print("Não há pacientes registrados! Tente adicionar algum paciente!")


def pesquisar_paciente():
    cpf = input("Digite o CPF do paciente que deseja pesquisar: ").strip()
    if cpf in pacientes:
        nome, idade, endereco, telefone = pacientes[cpf]
        print(f"Paciente encontrado: CPF: {cpf}, Nome: {nome}, Idade: {idade}, Endereço: {endereco}, Telefone: {telefone}")
    else:
        print("Paciente não encontrado.")


def adicionar_paciente():
    cpf = input("Digite o CPF do paciente: ").strip()
    if cpf in pacientes:
        print("Erro: Já existe um paciente registrado com este CPF.")
        return
    nome = input("Digite o nome do paciente: ").strip().title()
    idade = input("Digite a idade do paciente: ").strip()
    endereco = input("Digite o endereço do paciente: ").strip().title()
    telefone = input("Digite o telefone do paciente: ").strip()
    pacientes[cpf] = (nome, idade, endereco, telefone)
    print("Paciente adicionado com sucesso!")


def remover_paciente():
    cpf = input("Digite o CPF do paciente que deseja remover: ").strip()
    if cpf in pacientes:
        del pacientes[cpf]
        print("Paciente removido com sucesso!")
    else:
        print("Paciente não encontrado.")


def opcao_menu():
    try:
        return int(input("Digite a opção requerida, 1 Listar, 2 Pesquisar, 3 Adicionar, 4 Remover, 0 Sair: ").strip())
    except ValueError:
        print("Opção inválida. Por favor, digite um número inteiro.")
        return -1


def opcao_medico_paciente():
    try:
        return int(input("Digite a opção requerida: 1 Médico, 2 Paciente, 0 Voltar: ").strip())
    except ValueError:
        print("Opção inválida. Por favor, digite um número inteiro.")
        return -1


opcao = opcao_menu()

while opcao != 0:
    if opcao in [1, 2, 3, 4]:
        opcaoAlternativa = opcao_medico_paciente()

        while opcaoAlternativa != 0:
            if opcaoAlternativa == -1:
                opcaoAlternativa = opcao_medico_paciente()
                continue

            if opcaoAlternativa == 1:
                if opcao == 1:
                    listar_medico()
                elif opcao == 2:
                    pesquisar_medico()
                elif opcao == 3:
                    adicionar_medico()
                elif opcao == 4:
                    remover_medico()

            elif opcaoAlternativa == 2:
                if opcao == 1:
                    listar_paciente()
                elif opcao == 2:
                    pesquisar_paciente()
                elif opcao == 3:
                    adicionar_paciente()
                elif opcao == 4:
                    remover_paciente()

            else:
                print("Opção inválida!")

            opcaoAlternativa = opcao_medico_paciente()

        print("Voltando...")

    else:
        print("Opção inválida!")

    opcao = opcao_menu()

print("Obrigado por usar o sistema!")
