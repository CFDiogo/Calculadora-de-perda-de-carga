import math

def Reynolds(rho, V, mu, D):

    Reynolds=(rho*V*D)/mu

    return Reynolds

def colebrook(Q, eps, D, rho, mu, tolerancia=0.001, fCHUTE=0.05):
    g = 9.81  # ACELERAÇÃO DA GRAVIDADE (m/s**2)
    f = fCHUTE
    tol = tolerancia
    TABELA_VAZIA = []  # vetor vazio para armazenar as variáveis a cada iteração
    while True:
        #D = ((f * L * (4 * Q) ** 2) / (HBmax * 2 * g*3.1415926**2)) ** (1 / 5)
        Re = (rho * D * (Q / ((3.1415926 * D ** 2) / 4))) / mu
        V  = Q / ((3.1415926 * D ** 2) / 4)
        T1 = 1 / math.sqrt(f)
        T2 = (eps / D) / 3.7
        T3 = 2.51 / (Re * math.sqrt(f))
        T4 = -2 * math.log10(T2 + T3)
        F1 = 1 / (-2 * math.log10(((eps / D) / 3.7) + (2.51 / (Re * math.sqrt(f))))) ** 2
        F2 = (1 / T1) ** 2
        fmoody = (F1 + F2) / 2
        TABELA_VAZIA.append([f, D, Q, Re, eps/D, fmoody])  # pra juntar todos os nossos valores na nossa tabela com o append
        if abs(f - fmoody) < tol:
            break
        f = fmoody

    # Criação da tabela propriamente dita com um dataframe
    #TABELA_PREENCHIDA = pd.DataFrame(TABELA_VAZIA, columns=['f', 'D', 'Q', 'Re', 'E/D', 'fcalc'])
    return f, float(Re), float(V)

