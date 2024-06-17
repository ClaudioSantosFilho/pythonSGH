import sqlite3
from datetime import datetime

def conectar_bd():
    conn = sqlite3.connect('HopitalABC.db')
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas():
    conn, cursor = conectar_bd()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS MEDICOS 
            (
                CRM INTEGER PRIMARY KEY,
                NOME TEXT NOT NULL,
                ESPECIALIDADE TEXT,
                TELEFONE TEXT
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS PACIENTES 
            (
                CPF INTEGER PRIMARY KEY,
                NOME TEXT NOT NULL,
                IDADE INTEGER,
                ENDERECO TEXT,
                TELEFONE TEXT
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS PRONTUARIOS 
            (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                MEDICO TEXT NOT NULL,
                DATA TEXT,
                PACIENTE TEXT,
                ENFERMIDADE TEXT,
                TRATAMENTO TEXT
            )
        ''')

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS AGENDAMENTOS
             (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                CIENTE TEXT NOT NULL,
                DATA TEXT,
                MOTIVO TEXT,
                MEDICO TEXT
            )
        ''')

    conn.commit()
    conn.close()

def listar_medico():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT CRM, NOME, ESPECIALIDADE, TELEFONE FROM MEDICOS')
    medicos = cursor.fetchall()

    if medicos:
        print("Lista de médicos:")
        for medico in medicos:
            print(f"CRM: {medico[0]}, NOME: {medico[1]}, ESPECIALIDADE: {medico[2]}, TELEFONE: {medico[3]}")

    else:
        print("Não há médicos registrados. Tente adicionar algum médico.")

    conn.close()

def pesquisar_medico():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT CRM, NOME, ESPECIALIDADE, TELEFONE FROM MEDICOS')
    medicos = cursor.fetchall()

    if medicos:
        while True:
            try:
                crmPesquisadoSTR = input("Digite o CRM do médico que deseja encontrar: ").strip()

                if not crmPesquisadoSTR.isdigit():
                    raise ValueError("Apenas números são válidos.")

                crmNovoMedico = int(crmPesquisadoSTR)

                medicoEncontrado = None
                for medico in medicos:
                    if medico[0] == crmNovoMedico:
                        medicoEncontrado = medico
                        break

                if medicoEncontrado:
                    print(f"CRM: {medicoEncontrado[0]}, NOME: {medicoEncontrado[1]}, ESPECIALIDADE: {medicoEncontrado[2]}, TELEFONE: {medicoEncontrado[3]}")
                else:
                    print("Médico não encontrado.")

                return crmPesquisadoSTR

            except ValueError:
                print("Voltando...")

    else:
        print("Não há médicos registrados. Tente adicionar algum médico.")

    conn.close()

def adicionar_medico():
    conn, cursor = conectar_bd()

    crmNovoMedico = crm_medico_validacao(cursor)
    nomeNovoMedico = nome_medico_validacao()
    especialidadeNovoMedico = especialidade_medico_validacao()
    telefoneNovoMedico = telefone_medico_validacao(cursor)

    cursor.execute('INSERT INTO MEDICOS (CRM, NOME, ESPECIALIDADE, TELEFONE) VALUES (?, ?, ?, ?)',(crmNovoMedico, nomeNovoMedico, especialidadeNovoMedico, telefoneNovoMedico))
    conn.commit()

    print("Adicionado com sucesso!!!")

    conn.close()

def crm_medico_validacao(cursor):
    while True:
        try:
            crmMedicoSTR = input("Digite o CRM do médico: ").strip()

            if not crmMedicoSTR.isdigit():
                raise ValueError("O CRM deve conter apenas números.")

            crmMeicoINT = int(crmMedicoSTR)

            cursor.execute('SELECT CRM FROM MEDICOS WHERE CRM = ?', (crmMeicoINT,))
            medico = cursor.fetchone()

            if medico:
                print("Já existe médico registrado com esse CRM.")
            else:
                return crmMedicoSTR

        except ValueError:
            print("CRN inválido. Tente novamente.")
            print("Voltando...")

def nome_medico_validacao():
    while True:
        try:
            nomeMedicoSTR = input("Digite o nome do médico: ").strip().title()

            if not nomeMedicoSTR.replace(" ", "").isalpha():
                raise ValueError("Deve conter apenas letras.")

            return nomeMedicoSTR

        except ValueError:
            print("Nome inválido. Tente novamente")
            print("Voltando...")

def especialidade_medico_validacao():
    while True:
        try:
            especialidadeMedicoSTR = input("Digite a especialidade do médico: ").strip().title()

            if not especialidadeMedicoSTR.replace(" ", "").isalpha():
                raise ValueError("Deve conter apenas letras.")

            return especialidadeMedicoSTR

        except ValueError:
            print("Especialidade inválida. Tente novamente")
            print("Voltando...")

def telefone_medico_validacao(cursor):
    while True:
        try:
            telefoneMedicoSTR = input("Digite o número do médico: ").strip()

            if not telefoneMedicoSTR.isdigit():
                raise ValueError("O número de telefone deve conter apenas números.")

            telefoneMedicoINT = int(telefoneMedicoSTR)

            cursor.execute('SELECT TELEFONE FROM MEDICOS WHERE TELEFONE = ?', (telefoneMedicoINT,))
            medico = cursor.fetchone()

            cursor.execute('SELECT TELEFONE FROM PACIENTES WHERE TELEFONE = ?', (telefoneMedicoINT,))
            paciente = cursor.fetchone()

            if medico or paciente:
                print("Já existe indivíduo registrado com esse número.")
                print("Voltando...")

            else:
                return telefoneMedicoSTR

        except ValueError:
            print("Voltando...")

def remover_medico():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT CRM, NOME, ESPECIALIDADE, TELEFONE FROM MEDICOS')
    medicos = cursor.fetchall()

    if medicos:
        while True:
            try:
                crmPesquisadoSTR = input("Digite o CRM do médico que deseja remover: ").strip()

                if not crmPesquisadoSTR.isdigit():
                    raise ValueError("Apenas números são validos.")

                crmNovoMedico = int(crmPesquisadoSTR)

                cursor.execute('SELECT CRM, NOME, ESPECIALIDADE, TELEFONE FROM MEDICOS WHERE CRM = ?', (crmNovoMedico,))
                medicoEncontrado = cursor.fetchone()

                if medicoEncontrado:
                    cursor.execute('DELETE FROM MEDICOS WHERE CRM = ?', (crmNovoMedico,))
                    conn.commit()
                    print(f"Médico {medicoEncontrado[0]} removido com secesso!")

                else:
                    print("Médico não encontrado.")

                return crmPesquisadoSTR

            except ValueError:
                print("CRM inválido.")
                print("voltando...")

    else:
        print("Não há médicos registrados. Tente adicionar algum médico.")

def listar_paciente():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT CPF, NOME, IDADE, ENDERECO, TELEFONE FROM PACIENTES')
    pacientes = cursor.fetchall()

    if pacientes:
        print("Lista de pacientes:")
        for paciente in pacientes:
            print(f"CPF: {paciente[0]}, NOME: {paciente[1]}, IDADE: {paciente[2]}, ENDERECO: {paciente[3]}, TELEFONE: {paciente[4]}")

    else:
        print("Não há pacientes registrados. Tente adicionar algum paciente.")

        conn.close()

def pesquisar_paciente():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT CPF, NOME, IDADE, ENDERECO, TELEFONE FROM PACIENTES')
    pacientes = cursor.fetchall()

    if pacientes:
        while True:
            try:
                cpfPesquisado = input("Digite o CPF do paciente que deseja encontrar: ").strip()

                if not cpfPesquisado.isdigit():
                    raise ValueError("CPF deve conter apenas números.")

                cpfPesquisado = int(cpfPesquisado)

                cursor.execute('SELECT CPF, NOME, IDADE, ENDERECO, TELEFONE FROM PACIENTES WHERE CPF = ?',(cpfPesquisado,))
                pacienteEncontrado = cursor.fetchone()

                if pacienteEncontrado:
                    print(f"CPF: {pacienteEncontrado[0]}, NOME: {pacienteEncontrado[1]}, IDADE: {pacienteEncontrado[2]}, ENDEREÇO: {pacienteEncontrado[3]}, TELEFONE: {pacienteEncontrado[4]}")
                    return cpfPesquisado

                else:
                    print("Paciente não encontrado.")

                return cpfPesquisado

            except ValueError:
                print("Voltando...")

    else:
        print("Não há pacientes registrados. Tente adicionar algum paciente.")

    conn.close()

def adicionar_paciente():
    conn, cursor = conectar_bd()

    cpfNovoPaciente = cpf_paciente_validacao(cursor)
    nomeNovoPaciente = nome_paciente_validacao()
    idadeNovoPaciente = idade_paciente_validacao()
    enderecoNovoPaciente = endereco_paciente_validacao()
    telefoneNovoPaciente = telefone_paciente_validacao(cursor)

    cursor.execute('INSERT INTO PACIENTES (CPF, NOME, IDADE, ENDERECO, TELEFONE) VALUES (?, ?, ?, ?, ?)',(cpfNovoPaciente, nomeNovoPaciente, idadeNovoPaciente, enderecoNovoPaciente, telefoneNovoPaciente))
    conn.commit()

    print("Paciente adicionado com sucesso!!!")

    conn.close()

def cpf_paciente_validacao(cursor):
    while True:
        try:
            cpfPacienteSTR = input("Digite o CPF do paciente: ").strip()

            if not cpfPacienteSTR.isdigit():
                raise ValueError("O CPF deve conter apenas números.")

            cpfPacienteINT = int(cpfPacienteSTR)

            cursor.execute('SELECT CPF FROM PACIENTES WHERE CPF = ?', (cpfPacienteINT,))
            paciente = cursor.fetchone()

            if paciente:
                print("Já existe paciente registrado com esse CPF.")

            else:
                return cpfPacienteSTR

        except ValueError:
            print("CPF inválido. Tente novamente.")
            print("Voltando...")

def nome_paciente_validacao():
    while True:
        try:
            nomePacienteSTR = input("Digite o nome do paciente: ").strip().title()

            if not nomePacienteSTR.replace(" ", "").isalpha():
                raise ValueError("Deve conter apenas letras.")

            return nomePacienteSTR

        except ValueError:
            print("Nome inválido. Tente novamente")
            print("Voltando...")

def idade_paciente_validacao():
    while True:
        try:
            idadePacienteSTR = input("Digite a idade do paciente: ").strip()

            if not idadePacienteSTR.isdigit():
                raise ValueError("Deve conter apenas números.")

            return idadePacienteSTR

        except ValueError:
            print("Idade inválido. Tente novamente.")
            print("Voltando...")

def endereco_paciente_validacao():
    while True:
        try:
            enderecoPacienteSTR = input("Digite o endereço do paciente: ").strip().title()

            return enderecoPacienteSTR

        except ValueError:
            print("Endereço inválido. Tente novamente")
            print("Voltando...")

def telefone_paciente_validacao(cursor):
    while True:
        try:
            telefonePacienteSTR = input("Digite o número do paciente: ").strip()

            if not telefonePacienteSTR.isdigit():
                raise ValueError("O telefone deve conter apenas números.")

            cursor.execute('SELECT TELEFONE FROM MEDICOS WHERE TELEFONE = ?', (telefonePacienteSTR,))
            medico = cursor.fetchone()

            cursor.execute('SELECT TELEFONE FROM PACIENTES WHERE TELEFONE = ?', (telefonePacienteSTR,))
            paciente = cursor.fetchone()

            if medico or paciente:
                print("Já existe um indivíduo registrado com esse número de telefone.")
                print("Voltando...")

            else:
                return telefonePacienteSTR

        except ValueError:
            print("Telefone inválido. Tente novamente")
            print("Voltando...")

def remover_paciente():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT CPF, NOME FROM PACIENTES')
    pacientes = cursor.fetchall()

    if pacientes:
        while True:
            try:
                cpfPesquisadoSTR = input("Digite o CPF do paciente que deseja remover: ").strip()

                if not cpfPesquisadoSTR.isdigit():
                    raise ValueError("Apenas números são validos.")

                cpfNovoPaciente = int(cpfPesquisadoSTR)

                cursor.execute('SELECT CPF, NOME FROM PACIENTES WHERE CPF = ?', (cpfNovoPaciente,))
                paciente_encontrado = cursor.fetchone()

                if paciente_encontrado:
                    cursor.execute('DELETE FROM PACIENTES WHERE CPF = ?', (cpfNovoPaciente,))
                    conn.commit()
                    print(f"Paciente com CPF {cpfNovoPaciente} removido com sucesso!")

                else:
                    print("Paciente não encontrado.")

                return cpfPesquisadoSTR

            except ValueError:
                print("CRM inválido.")
                print("voltando...")

    else:
        print("Não há pacientes registrados. Tente adicionar algum paciente.")

    conn.close()

def listar_prontuario_medico():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT ID, MEDICO, DATA, PACIENTE, ENFERMIDADE, TRATAMENTO FROM PRONTUARIOS')
    prontuarios = cursor.fetchall()

    if prontuarios:
        print("Lista de prontuários:")
        for prontuario in prontuarios:
            print(f"ID: {prontuario[0]}, MÉDICO: {prontuario[1]}, DATA: {prontuario[2]}, PACIENTE: {prontuario[3]}, ENFERMIDADE: {prontuario[4]}, TRATAMENTO: {prontuario[5]}")

    else:
        print("Não há prontuários registrados.")

    conn.close()

def pesquisar_prontuario_medio():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT ID, MEDICO, DATA, PACIENTE, ENFERMIDADE, TRATAMENTO FROM PRONTUARIOS')
    prontuarios = cursor.fetchall()

    if prontuarios:
        while True:
            try:
                idPesquisadoSTR = input("Digite o id do prontuário que deseja encontrar: ").strip()

                if not idPesquisadoSTR.isdigit():
                    raise ValueError("Apenas números são validos.")

                prontuarioIDNovo = int(idPesquisadoSTR)

                cursor.execute('SELECT ID, MEDICO, DATA, PACIENTE, ENFERMIDADE, TRATAMENTO FROM PRONTUARIOS WHERE ID = ?',(prontuarioIDNovo,))
                prontuarioEncontrado = cursor.fetchone()

                if prontuarioEncontrado:
                    print("Prontuário encontrado com sucesso.")
                    print(f"ID: {prontuarioEncontrado[0]}, MÉDICO: {prontuarioEncontrado[1]}, DATA: {prontuarioEncontrado[2]}, PACIENTE: {prontuarioEncontrado[3]}, ENFERMIDADE: {prontuarioEncontrado[4]}, TRATAMENTO: {prontuarioEncontrado[5]}")

                else:
                    print("Prontuário não encontrado.")

                return idPesquisadoSTR

            except ValueError:
                print("ID inválido. Tente novamente.")
                print("voltando...")

    else:
        print("Não há prontuários registrados.")

    conn.close()

def adicionar_prontuario_medico():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT MAX(ID) FROM PRONTUARIOS')
    maxID = cursor.fetchone()[0]

    if maxID is None:
        prontuarioIDNovo = 1

    else:
        prontuarioIDNovo = maxID + 1

    prontuarioNomeMedicoNovo = prontuario_nome_medico_validacao()
    pronturaioDataNovo = prontuario_data_validacao()
    prontuarioNomePacienteNovo = prontuario_nome_paciente_validacao()
    prontuarioEnfermidadeNovo = prontuario_enfermidade_validacao()
    prontuarioTratamentoNovo = prontuario_tratamento_validacao()

    cursor.execute('INSERT INTO PRONTUARIOS (ID, MEDICO, DATA, PACIENTE, ENFERMIDADE, TRATAMENTO) VALUES (?, ?, ?, ?, ?, ?)',(prontuarioIDNovo, prontuarioNomeMedicoNovo, pronturaioDataNovo, prontuarioNomePacienteNovo, prontuarioEnfermidadeNovo, prontuarioTratamentoNovo))
    conn.commit()

    print("Prontuário registrado com sucesso!")

    conn.close()

def prontuario_nome_paciente_validacao():
    while True:
        try:
            prontuarioNomePaciente = input("Digite o nome do paciente: ").strip().title()

            if not prontuarioNomePaciente.replace(" ", "").isalpha():
                raise ValueError("Deve conter apenas letras.")

            return prontuarioNomePaciente

        except ValueError:
            print("Nome inválido. Tente novamente")
            print("Voltando...")

def prontuario_data_validacao():
    while True:
        try:
            prontuarioData = input("Digite a data do agendamento (DD/MM/AAAA): ").strip()

            dataFormatada = datetime.strptime(prontuarioData, "%d/%m/%Y")

            return dataFormatada.strftime("%d/%m/%Y")

        except ValueError:
            print("Data inválida. Tente novamente.")
            print("Voltando...")

def prontuario_nome_medico_validacao():
    while True:
        try:
            prontuarioNomeMedico = input("Digite o nome do médico: ").strip().title()

            if not prontuarioNomeMedico.replace(" ", "").isalpha():
                raise ValueError("Deve conter apenas letras.")

            return prontuarioNomeMedico

        except ValueError:
            print("Nome inválido. Tente novamente")
            print("Voltando...")

def prontuario_enfermidade_validacao():
    while True:
        try:
            prontuarioEnfermidade = input("Digite a enfermidade encontrada: ").strip().title()

            if not prontuarioEnfermidade.replace(" ", "").isalpha():
                raise ValueError("Deve conter apenas letras.")

            return prontuarioEnfermidade

        except ValueError:
            print("Texto inválido. Tente novamente")
            print("Voltando...")

def prontuario_tratamento_validacao():
    while True:
        try:
            prontuarioTratamento = input("Digite o tratamento recomendado: ").strip().title()

            if not prontuarioTratamento.replace(" ", "").isalpha():
                raise ValueError("Deve conter apenas letras.")

            return prontuarioTratamento

        except ValueError:
            print("Texto inválido. Tente novamente")
            print("Voltando...")

def remover_prontuario_medico():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT ID, MEDICO, DATA, PACIENTE, ENFERMIDADE, TRATAMENTO FROM PRONTUARIOS')
    prontuarios = cursor.fetchall()

    if prontuarios:
        while True:
            try:
                idProntuarioSTR = input("Digite o ID do prontuário que deseja remover: ").strip()

                if not idProntuarioSTR.isdigit():
                    raise ValueError("Apenas números são válidos para o ID do prontuário.")

                idProntuarioINT = int(idProntuarioSTR)

                cursor.execute('SELECT ID FROM PRONTUARIOS WHERE ID = ?', (idProntuarioINT,))
                prontuarioEncontrado = cursor.fetchone()

                if prontuarioEncontrado:
                    cursor.execute('DELETE FROM PRONTUARIOS WHERE ID = ?', (idProntuarioINT,))
                    conn.commit()
                    print("Prontuário removido com sucesso!")
                else:
                    print("Prontuário não encontrado.")

                return idProntuarioSTR

            except ValueError:
                print("ID inválido. Tente novamente.")
                print("Voltando...")

    else:
        print("Não há prontuários registrados.")

    conn.close()

def listar_agendamento():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT ID, CIENTE, DATA, MOTIVO, MEDICO FROM AGENDAMENTOS')
    agendamentos = cursor.fetchall()

    if agendamentos:
        print("Lista de agendamentos:")
        for agendamento in agendamentos:
            print(f"ID: {agendamento[0]}, CIENTE: {agendamento[1]}, DATA: {agendamento[2]}, MOTIVO: {agendamento[3]}, MÉDICO: {agendamento[4]}")

    else:
        print("Não há agendamentos registrados.")

    conn.close()

def pesquisar_agendamento():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT ID, CIENTE, DATA, MOTIVO, MEDICO FROM AGENDAMENTOS')
    agendamentos = cursor.fetchall()

    if agendamentos:
        while True:
            try:
                agendamentoIDSTR = input("Digite o ID do agendamento que deseja encontrar: ").strip()

                if not agendamentoIDSTR.isdigit():
                    raise ValueError("Apenas números são válidos para o ID do agendamento.")

                agendamentoIDINT = int(agendamentoIDSTR)

                cursor.execute('SELECT ID, CIENTE, DATA, MOTIVO, MEDICO FROM AGENDAMENTOS WHERE ID = ?',(agendamentoIDINT,))
                agendamentoEncontrado = cursor.fetchone()

                if agendamentoEncontrado:
                    print("Agendamento encontrado com sucesso.")
                    print(
                        f"ID: {agendamentoEncontrado[0]}, CIENTE: {agendamentoEncontrado[1]}, DATA: {agendamentoEncontrado[2]}, MOTIVO: {agendamentoEncontrado[3]}, MÉDICO: {agendamentoEncontrado[4]}")
                    return agendamentoIDSTR

                else:
                    print("Agendamento não encontrado.")

                return agendamentoIDSTR

            except ValueError:
                print("ID inválido. Tente novamente.")
                print("Voltando...")

    else:
        print("Não há agendamentos registrados.")

    conn.close()

def adicionar_agendamento():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT MAX(ID) FROM AGENDAMENTOS')
    maxID = cursor.fetchone()[0]

    if maxID is None:
        agendamentoIDNovo = 1

    else:
        agendamentoIDNovo = maxID + 1

    agendamentoNomePacienteNovo = agendamento_paciente_validacao()
    agendamentoDataNovo = agendamento_data_validacao(cursor)
    agendamentoMotivoNovo = agendamento_motivo_validacao()
    agendamentoMedicoNovo = agendamento_medico_preferencia_validacao()

    cursor.execute('INSERT INTO AGENDAMENTOS (ID, CIENTE, DATA, MOTIVO, MEDICO) VALUES (?, ?, ?, ?, ?)',(agendamentoIDNovo, agendamentoNomePacienteNovo, agendamentoDataNovo, agendamentoMotivoNovo, agendamentoMedicoNovo))
    conn.commit()

    print("Agendamento registrado com sucesso!")

    conn.close()

def agendamento_paciente_validacao():
    while True:
        try:
            agendamentoNomePaciente = input("Digite o seu nome: ").strip().title()

            if not agendamentoNomePaciente.replace(" ", "").isalpha():
                raise ValueError("Deve conter apenas letras.")

            return agendamentoNomePaciente

        except ValueError:
            print("Nome inválido. Tente novamente.")
            print("Voltando...")

def agendamento_data_validacao(cursor):
    while True:
        try:
            agendamentoData = input("Digite a data do agendamento (DD/MM/AAAA): ").strip()

            dataFormatada = datetime.strptime(agendamentoData, "%d/%m/%Y")

            cursor.execute('SELECT DATA FROM AGENDAMENTOS WHERE DATA = ?', (agendamentoData,))
            data_existente = cursor.fetchone()

            if data_existente:
                raise ValueError("Data já agendada. Escolha outra data.")

            return dataFormatada.strftime("%d/%m/%Y")

        except ValueError:
            print("Data inválida. Tente novamente.")
            print("Voltando...")

def agendamento_motivo_validacao():
    while True:
        try:
            agendamentoMotivo = input("Digite o motivo do agendamento: ").strip()

            if not agendamentoMotivo.replace(" ", "").isalpha():
                raise ValueError("Deve conter apenas letras.")

            return agendamentoMotivo

        except ValueError:
            print("Motivo inválido. Tente novamente.")
            print("Voltando...")

def agendamento_medico_preferencia_validacao():
    while True:
        try:
            agendamentoMedico = input("Digite o médico de preferência: ").strip().title()

            if not agendamentoMedico.replace(" ", "").isalpha():
                raise ValueError("O nome do médico deve conter apenas letras.")

            return agendamentoMedico

        except ValueError:
            print("Nome de médico inválido. Tente novamente.")
            print("Voltando...")

def remover_agendamento():
    conn, cursor = conectar_bd()

    cursor.execute('SELECT ID, CIENTE, DATA, MOTIVO, MEDICO FROM AGENDAMENTOS')
    agendamentos = cursor.fetchall()

    if agendamentos:
        while True:
            try:
                idAgendamentoSTR = input("Digite o ID do agendamento que deseja remover: ").strip()

                if not idAgendamentoSTR.isdigit():
                    raise ValueError("Apenas números são válidos para o ID do agendamento.")

                idAgendamentoINT = int(idAgendamentoSTR)

                cursor.execute('SELECT ID FROM AGENDAMENTOS WHERE ID = ?', (idAgendamentoINT,))
                agendamentoEncontrado = cursor.fetchone()

                if agendamentoEncontrado:
                    cursor.execute('DELETE FROM AGENDAMENTOS WHERE ID = ?', (idAgendamentoINT,))
                    conn.commit()
                    print("Agendamento removido com sucesso!")

                else:
                    print("Agendamento não encontrado.")

                return idAgendamentoSTR

            except ValueError:
                print("ID inválido. Tente novamente.")
                print("Voltando...")

    else:
        print("Não há agendamentos registrados.")

    conn.close()

def menu_medicos():
    while True:
        print("\n===== MENU MÉDICOS =====")
        print("1 - Adicionar Médico")
        print("2 - Listar Médicos")
        print("3 - Pesquisar Médico")
        print("4 - Remover Médico")
        print("0 - Voltar ao Menu Principal")
        print("========================")

        opcao = input("Digite a opção desejada: ").strip()

        if opcao == "1":
            adicionar_medico()

        elif opcao == "2":
            listar_medico()

        elif opcao == "3":
            pesquisar_medico()

        elif opcao == "4":
            remover_medico()

        elif opcao == "0":
            break

        else:
            print("Opção inválida. Tente novamente.")

def menu_pacientes():
    while True:
        print("\n===== MENU PACIENTES =====")
        print("1 - Adicionar Paciente")
        print("2 - Listar Pacientes")
        print("3 - Pesquisar Paciente")
        print("4 - Remover Paciente")
        print("0 - Voltar ao Menu Principal")
        print("==========================")

        opcao = input("Digite a opção desejada: ").strip()

        if opcao == "1":
            adicionar_paciente()

        elif opcao == "2":
            listar_paciente()

        elif opcao == "3":
            pesquisar_paciente()

        elif opcao == "4":
            remover_paciente()

        elif opcao == "0":
            break

        else:
            print("Opção inválida. Tente novamente.")

def menu_prontuarios():
    while True:
        print("\n===== MENU PRONTUÁRIOS =====")
        print("1 - Adicionar Prontuário")
        print("2 - Listar Prontuários")
        print("3 - Pesquisar Prontuário")
        print("4 - Remover Prontuário")
        print("0 - Voltar ao Menu Principal")
        print("============================")

        opcao = input("Digite a opção desejada: ").strip()

        if opcao == "1":
            adicionar_prontuario_medico()

        elif opcao == "2":
            listar_prontuario_medico()

        elif opcao == "3":
            pesquisar_prontuario_medio()

        elif opcao == "4":
            remover_prontuario_medico()

        elif opcao == "0":
            break

        else:
            print("Opção inválida. Tente novamente.")

def menu_agendamentos():
    while True:
        print("\n===== MENU AGENDAMENTOS =====")
        print("1 - Adicionar Agendamento")
        print("2 - Listar Agendamentos")
        print("3 - Pesquisar Agendamento")
        print("4 - Remover Agendamento")
        print("0 - Voltar ao Menu Principal")
        print("=============================")


        opcao = input("Digite a opção desejada: ").strip()

        if opcao == "1":
            adicionar_agendamento()

        elif opcao == "2":
            listar_agendamento()

        elif opcao == "3":
            pesquisar_agendamento()

        elif opcao == "4":
            remover_agendamento()

        elif opcao == "0":
            break

        else:
            print("Opção inválida. Tente novamente.")

def menu_principal():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Médicos")
        print("2 - Pacientes")
        print("3 - Prontuários")
        print("4 - Agendamentos")
        print("0 - Sair")
        print("==========================")

        opcao = input("Digite a opção desejada: ").strip()

        if opcao == "1":
            menu_medicos()

        elif opcao == "2":
            menu_pacientes()

        elif opcao == "3":
            menu_prontuarios()

        elif opcao == "4":
            menu_agendamentos()

        elif opcao == "0":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

criar_tabelas()
menu_principal()