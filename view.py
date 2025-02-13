from models import Conta, engine, Bancos, Status, Historico, Tipos
from sqlmodel import Session, select
from datetime import date, datetime, timedelta

def criar_conta(conta: Conta):
    with Session(engine) as session:  #para fechar o banco automaticamente 
        statement = select(Conta).where(Conta.banco == conta.banco) #where faz um filtro
        results = session.exec(statement).all()
        
        if results:
            print('Já existe uma conta nesse banco.')
            return 

        session.add(conta)
        session.commit()
        return conta

def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
    return results

def desativar_conta(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id == id)
        conta = session.exec(statement).first() 

        if conta.valor > 0:
            raise ValueError('Essa conta ainda possui saldo, não é possível desativar.') #poderia colocar um print com mensagem de erro e dar return
        conta.status = Status.INATIVO
        session.commit()
    
def transferir_saldo(id_saida, id_entrada, valor):
    with Session(engine) as session: 
        statement = select(Conta).where(Conta.id == id_saida)
        conta_saida = session.exec(statement).first()

        if conta_saida.valor < valor:
            raise ValueError('Saldo insuficiente.')
        
        statement = select(Conta).where(Conta.id == id_entrada)
        conta_entrada = session.exec(statement).first()

        conta_saida.valor -= valor 
        conta_entrada.valor += valor 
        session.commit()

def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session: 
        statement = select(Conta).where(Conta.id == historico.conta_id)
        conta = session.exec(statement).first()

        if conta.status == Status.INATIVO: 
            raise ValueError('Conta está inativa, não é possível fazer movimentações.')

        if historico.tipo == Tipos.ENTRADA:
            conta.valor += historico.valor 
        else:
            if conta.valor < historico.valor:
                raise ValueError('Saldo insuficiente.')
            conta.valor -= historico.valor
        
        session.add(historico) 
        session.commit() 
        return historico 

def total_contas():
    with Session(engine) as session: 
        statement = select(Conta)
        contas = session.exec(statement).all()
    
    total = 0
    for conta in contas: 
        total += conta.valor 
    
    return total

def buscar_historico_entre_datas(data_inicio: date, data_fim: date):
    with Session(engine) as session: 
        statement = select(Historico).where(
            Historico.data >= data_inicio,
            Historico.data <= data_fim
        )
        resultados = session.exec(statement).all()
        return resultados 
    
def criar_grafico_por_conta():
    with Session(engine) as session: 
        statement = select(Conta).where(Conta.status == Status.ATIVO)
        conta = session.exec(statement).all()

        bancos = []
        total = []
        for i in conta:
            bancos.append(i.banco.value)
        for i in conta:
            total.append(i.valor)
        
        print(bancos)
        print(total)

        import matplotlib.pyplot as plt 

        plt.bar(bancos, total)
        plt.show()

#desativar_conta(1)

#conta = Conta(valor=500, banco = Bancos.NUBANK)
#criar_conta(conta)

#conta = Conta(valor=10000, banco = Bancos.SANTANDER)
#criar_conta(conta)

#transferir_saldo(2, 3, 10)

#historico = Historico(conta_id=1, tipo=Tipos.ENTRADA, valor=100, data=date.today())
#movimentar_dinheiro(historico)

#historico = Historico(conta_id=2, tipo=Tipos.SAIDA, valor=100, data=datetime.now())
#movimentar_dinheiro(historico)

#historico = Historico(conta_id=1, tipo=Tipos.SAIDA, valor=100, data=datetime.now())
#movimentar_dinheiro(historico)

#total_contas()



#X =buscar_historico_entre_datas(date.today() - timedelta(days=1), date.today() + timedelta(days=1))
#print(X)

#criar_grafico_por_conta()