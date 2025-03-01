from tkinter import *
from tkinter import ttk
from Func import colebrook

def escolha_material(material):

    mmtom = 10e-3       # metros p mm
    eps = 0             # inicializando a variável eps
    material = material.strip()
    match material:
        case "Plástico/Vidro":
            eps = 0.0001 * mmtom
        case "Concreto":
            eps = ((0.9 + 9) / 2) * mmtom
        case "Madeira":
            eps = 0.5 * mmtom
        case "Aço inox":
            eps = 0.002 * mmtom
        case "PVC":
            eps = 0.0001 * mmtom
        case "Cobre/Latão":
            eps = 0.0015 * mmtom
        case _:
            print("Material não encontrado")
    
    return float(eps)

def escolha_fluido(fluido):
    fluido = fluido.strip()
    match fluido:
        case "Ar":
            rho = 1.184 
            mu = 1.81e-5 
        case "Gás Natural":
            rho = 0.717  
            mu = 1.10e-5   
        case "CO2":
            rho = 1.842  
            mu = 1.48e-5  
        case _:
            print("Fluido não encontrado")
            rho = mu = 0    
    return float(rho), float(mu)

def saida_Vazao(diametro):
    if radiobutton_value.get()==1:
        # Se 'Velocidade' estiver marcado, calcula vazão com base na velocidade
        velocidade = float(input3.get())
        Q = 3.1416 * (float(diametro)/2)**2 * velocidade  # Fórmula para vazão (Q = A * v)
    elif radiobutton_value.get()==2:
        # Se 'Vazão' estiver marcado, calcula a velocidade com base na vazão
        Q = float(input3.get())
    else:
        Q = None
     
    if Q is None:
        print("Erro: Valor de vazão não foi calculado corretamente.")
    return float(Q) if Q is not None else 0.0  # Retorna 0.0 ou outro valor válido em caso de erro


def perdaDeCargaDist(f, L, V, D, g):
    H = (f*L*V**2)/(D*2*g)
    return float(H)

def atualizar_resultados(reynolds, f, H):
    resultado = f"Reynolds [adim]: {round(reynolds,3)}\nFator de atrito [adim] (f): {round(f,3)}\nPerda de carga [m] (H): {round(H,3)}"
    result_label.config(text=resultado)

def calcular():
    # Chama as funções para obter os valores dos menus e entradas
    eps = escolha_material(construcao_menu.get())
    D = float(input2.get())
    L = float(input1.get())
    Q = saida_Vazao(D)
    rho, mu = escolha_fluido(fluido_menu.get())
    f, Re, V = colebrook(Q, eps, D, rho, mu, 0.001, 0.05)
    H = perdaDeCargaDist(f, L, V, D, 9.81)

    # Atualiza o label com os resultados
    atualizar_resultados(Re, f, H)

root = Tk()
root.title("Calculadora de perda de carga distribuida em tubulações")
root.geometry("520x320")  # Define o tamanho da janela

# Frame principal
content = ttk.Frame(root)
content.grid(column=0, row=0, sticky=(N, W, E, S))
# Frame ajustável (posição independente)
frame = ttk.Frame(content, borderwidth=10, relief="ridge", width=275, height=375)
frame.grid(column=0, row=6, columnspan=4, padx=5, pady=5, sticky=(N,S,E, W))

# Componentes de texto
text1 = ttk.Label(content, text="Comprimento da tubulação [m]", justify="center")
text2 = ttk.Label(content, text="Diâmetro hidráulico [m]", justify="center")
text3 = ttk.Label(content, text="Vazão [m^3/s] (Opção 1)", justify="center")
text4 = ttk.Label(content, text="Velocidade do escoamento [m/s] (Opção 2)", justify="center")

# Entradas de texto
input1 = ttk.Entry(content, )
input2 = ttk.Entry(content)
input3 = ttk.Entry(content)

radiobutton_value = IntVar()

radiobutton1 = ttk.Radiobutton(content, text="Opção 1", value=1, variable=radiobutton_value)
radiobutton2 =ttk.Radiobutton(content, text="Opção 2", value=2, variable=radiobutton_value)

# Menus suspensos
fluido_label = ttk.Label(content, text="Escolha do Fluido à 15 ºC:")
fluido_menu = ttk.Combobox(content, values=["Ar", "Gás Natural", "CO2"], state="readonly")
fluido_menu.set("Selecione")

construcao_label = ttk.Label(content, text="Material da tubulação:")
construcao_menu = ttk.Combobox(content, values=["Plástico/Vidro", "Concreto", "Madeira", "Aço inox",
                                                "PVC", "Cobre/Latão"], state="readonly")
construcao_menu.set("Selecione")

# Botão para calcular os resultados
calcular_button = ttk.Button(content, text="Calcular", command=calcular)

# Posicionamento dos elementos
text1.grid(column=0, row=0, sticky=W, padx=5, pady=5)
text2.grid(column=0, row=1, sticky=W, padx=5, pady=5)
text3.grid(column=0, row=2, sticky=W, padx=5, pady=5)
text4.grid(column=0, row=3, sticky=W, padx=5, pady=5)

input1.grid(column=1, row=0, columnspan=2, padx=5, pady=5, sticky=(W, E))
input2.grid(column=1, row=1, columnspan=2, padx=5, pady=5, sticky=(W, E))
input3.grid(column=1, row=2, columnspan=2, padx=5, pady=5, sticky=(W, E))

radiobutton1.grid(column=1, row=3, sticky=W, padx=5, pady=5)
radiobutton2.grid(column=2, row=3, sticky=W, padx=5, pady=5)

fluido_label.grid(column=0, row=4, sticky=W, padx=5, pady=5)
fluido_menu.grid(column=1, row=4, padx=5, pady=5, sticky=(W, E))

construcao_label.grid(column=0, row=5, sticky=W, padx=5, pady=5)
construcao_menu.grid(column=1, row=5, padx=5, pady=5, sticky=(W, E))

# Adicionar um Label para exibir os resultados dentro do frame
result_label = ttk.Label(frame, text="", justify="left")
result_label.grid(column=0, row=0, columnspan=6, padx=5, pady=5)

# Botão de calcular
calcular_button.grid(column=0, row=7, columnspan=3, padx=5, pady=5)

root.mainloop()
