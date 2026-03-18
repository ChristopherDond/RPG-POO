import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import random
from abc import ABC, abstractmethod

def dummy_log(msg, tag=""):
    print(msg)
log_func = dummy_log
log_color_func = dummy_log

class Personagem(ABC):
    def __init__(self, nome, hp, atk, dfn, xp=0, level=1, elemento="neutro"):
        self.nome = nome
        self.hp_max_base = hp
        self.hp = hp
        self.atk_base = atk
        self.dfn_base = dfn
        self.xp = xp
        self.level = level
        self.elemento = elemento
        self.vivo = True

    @property
    def hp_max(self):
        return self.hp_max_base

    @abstractmethod
    def atacar(self, alvo):
        pass

    def calcular_dano(self, dano_base, tipo_dano="neutro", alvo=None):
        if alvo and hasattr(alvo, 'elemento'):
            if tipo_dano == "fogo" and alvo.elemento == "gelo":
                dano_base = int(dano_base * 1.5)
                log_color_func("É super efetivo!", "critical")
            elif tipo_dano == "gelo" and alvo.elemento == "fogo":
                dano_base = int(dano_base * 1.5)
                log_color_func("É super efetivo!", "critical")
            elif tipo_dano == alvo.elemento:
                dano_base = int(dano_base * 0.5)
                log_color_func("Não é muito efetivo...", "weak")
        return dano_base

    def receber_dano(self, dano):
        dano_real = max(0, dano - self.dfn_base)
        self.hp -= dano_real
        log_color_func(f"{self.nome} recebeu {dano_real} de dano. HP restante: {self.hp}/{self.hp_max}", "damage")
        if self.hp <= 0:
            self.hp = 0
            self.vivo = False
            log_color_func(f"{self.nome} morreu!", "critical")

    def curar(self, quantidade):
        self.hp = min(self.hp + quantidade, self.hp_max)
        log_color_func(f"{self.nome} recuperou {quantidade} de HP. HP atual: {self.hp}/{self.hp_max}", "heal")

    def esta_vivo(self):
        return self.vivo

class Habilidade:
    def __init__(self, nome, custo_mana, dano_base, tipo="neutro", cura=0):
        self.nome = nome
        self.custo_mana = custo_mana
        self.dano_base = dano_base
        self.tipo = tipo
        self.cura = cura

    def usar(self, usuario, alvo):
        if usuario.mana < self.custo_mana:
            log_func("Mana insuficiente!")
            return False
        usuario.mana -= self.custo_mana
        if self.cura > 0:
            usuario.curar(self.cura)
            log_color_func(f"{usuario.nome} usou {self.nome} e recuperou {self.cura} de HP.", "heal")
        else:
            dano_calculado = usuario.calcular_dano(self.dano_base + usuario.atk_base // 2 + random.randint(-2, 2), self.tipo, alvo)
            log_color_func(f"{usuario.nome} usou {self.nome} causando {dano_calculado} de dano {self.tipo}!", "skill")
            alvo.receber_dano(dano_calculado)
        return True

class Jogador(Personagem):
    def __init__(self, nome, classe_nome):
        self.classe_nome = classe_nome
        hp, atk, dfn, mana = 30, 8, 2, 20
        self.habilidades = []
        
        if classe_nome == "Guerreiro":
            hp, atk, dfn, mana = 50, 12, 4, 15
            self.habilidades = [
                Habilidade("Golpe Esmagador", 5, 20, "neutro"),
                Habilidade("Grito de Guerra", 8, 0, "neutro", cura=25)
            ]
        elif classe_nome == "Mago":
            hp, atk, dfn, mana = 35, 4, 1, 50
            self.habilidades = [
                Habilidade("Explosão Arcana", 8, 30, "fogo"),
                Habilidade("Cura Leve", 5, 0, "neutro", cura=30),
                Habilidade("Estilhaço de Gelo", 7, 25, "gelo")
            ]
        elif classe_nome == "Ladino":
            hp, atk, dfn, mana = 40, 10, 2, 20
            self.habilidades = [
                Habilidade("Ataque Furtivo", 5, 28, "neutro"),
                Habilidade("Drenar Vida", 10, 20, "neutro", cura=20)
            ]

        super().__init__(nome, hp=hp, atk=atk, dfn=dfn, xp=0, level=1, elemento="neutro")
        self.mana_max_base = mana
        self.mana = mana
        self.inventario = []
        self.ouro = 80
        self.xp_para_proximo_level = 20
        
        self.arma_equipada = None
        self.armadura_equipada = None
        self.acessorio_equipado = None
        
        self.batalhas_vencidas = 0
        self.dias = 1

    @property
    def hp_max(self):
        bonus = self.acessorio_equipado.valor if self.acessorio_equipado and self.acessorio_equipado.tipo == "acessorio_hp" else 0
        return self.hp_max_base + bonus

    @property
    def mana_max(self):
        bonus = self.acessorio_equipado.valor if self.acessorio_equipado and self.acessorio_equipado.tipo == "acessorio_mp" else 0
        return self.mana_max_base + bonus

    @property
    def atk_total(self):
        bonus_arma = self.arma_equipada.valor if self.arma_equipada else 0
        bonus_acessorio = self.acessorio_equipado.valor if self.acessorio_equipado and self.acessorio_equipado.tipo == "acessorio_atk" else 0
        return self.atk_base + bonus_arma + bonus_acessorio

    @property
    def dfn_total(self):
        bonus_armadura = self.armadura_equipada.valor if self.armadura_equipada else 0
        bonus_acessorio = self.acessorio_equipado.valor if self.acessorio_equipado and self.acessorio_equipado.tipo == "acessorio_dfn" else 0
        return self.dfn_base + bonus_armadura + bonus_acessorio

    def receber_dano(self, dano):
        dano_real = max(0, dano - self.dfn_total)
        self.hp -= dano_real
        log_color_func(f"{self.nome} recebeu {dano_real} de dano. HP restante: {self.hp}/{self.hp_max}", "damage")
        if self.hp <= 0:
            self.hp = 0
            self.vivo = False
            log_color_func(f"{self.nome} morreu!", "critical")

    def atacar(self, alvo):
        dano = self.atk_total + random.randint(-1, 3)
        if self.classe_nome == "Ladino" and random.random() < 0.35:
            dano = int(dano * 1.6)
            log_color_func("Ataque Crítico Fatal!", "critical")
        
        dano = self.calcular_dano(dano, "neutro", alvo)
        log_func(f"{self.nome} ataca {alvo.nome} causando {dano} de dano!")
        alvo.receber_dano(dano)

    def usar_habilidade(self, index, alvo):
        if 0 <= index < len(self.habilidades):
            habilidade = self.habilidades[index]
            if habilidade.nome == "Drenar Vida":
                if self.mana < habilidade.custo_mana:
                    log_func("Mana insuficiente!")
                    return False
                self.mana -= habilidade.custo_mana
                dano = self.calcular_dano(habilidade.dano_base + self.atk_base // 2, "neutro", alvo)
                log_color_func(f"{self.nome} usou Drenar Vida causando {dano} de dano!", "skill")
                alvo.receber_dano(dano)
                self.curar(dano)
                return True
            return habilidade.usar(self, alvo)
        return False

    def equipar(self, equipamento):
        if equipamento.tipo == "arma":
            if self.arma_equipada:
                self.arma_equipada.quantidade = 1  # Retorna o antigo com qtd 1
                self.inventario.append(self.arma_equipada)
            self.arma_equipada = equipamento
            log_color_func(f"{self.nome} equipou {equipamento.nome} (+{equipamento.valor} ATK).", "info")
            if equipamento in self.inventario:
                self.inventario.remove(equipamento)
                
        elif equipamento.tipo == "armadura":
            if self.armadura_equipada:
                self.armadura_equipada.quantidade = 1
                self.inventario.append(self.armadura_equipada)
            self.armadura_equipada = equipamento
            log_color_func(f"{self.nome} vestiu {equipamento.nome} (+{equipamento.valor} DFN).", "info")
            if equipamento in self.inventario:
                self.inventario.remove(equipamento)
                
        elif equipamento.tipo.startswith("acessorio_"):
            if self.acessorio_equipado:
                # Se tinha bonus de HP/Mana max, curamos se o max cair?
                self.acessorio_equipado.quantidade = 1
                self.inventario.append(self.acessorio_equipado)
            self.acessorio_equipado = equipamento
            log_color_func(f"{self.nome} colocou o acessório: {equipamento.nome}.", "info")
            if equipamento in self.inventario:
                self.inventario.remove(equipamento)

    def desequipar(self, categoria):
        if categoria == "arma" and self.arma_equipada:
            self.arma_equipada.quantidade = 1
            self.inventario.append(self.arma_equipada)
            log_func(f"{self.nome} desequipou a arma {self.arma_equipada.nome}.")
            self.arma_equipada = None
        elif categoria == "armadura" and self.armadura_equipada:
            self.armadura_equipada.quantidade = 1
            self.inventario.append(self.armadura_equipada)
            log_func(f"{self.nome} desequipou a armadura {self.armadura_equipada.nome}.")
            self.armadura_equipada = None
        elif categoria == "acessorio" and self.acessorio_equipado:
            self.acessorio_equipado.quantidade = 1
            self.inventario.append(self.acessorio_equipado)
            log_func(f"{self.nome} desequipou o acessório {self.acessorio_equipado.nome}.")
            self.acessorio_equipado = None

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        log_color_func(f"{self.nome} ganhou {quantidade} de XP.", "xp")
        while self.xp >= self.xp_para_proximo_level:
            self.subir_nivel()

    def subir_nivel(self):
        self.level += 1
        self.xp -= self.xp_para_proximo_level
        self.xp_para_proximo_level = int(self.xp_para_proximo_level * 1.5)
        
        aumento_hp = 12 if self.classe_nome == "Guerreiro" else (8 if self.classe_nome == "Mago" else 10)
        aumento_mana = 3 if self.classe_nome == "Guerreiro" else (15 if self.classe_nome == "Mago" else 8)
        
        self.hp_max_base += aumento_hp
        self.mana_max_base += aumento_mana
        self.atk_base += 3 if self.classe_nome != "Mago" else 2
        self.dfn_base += 3 if self.classe_nome == "Guerreiro" else 2
        
        self.hp = self.hp_max
        self.mana = self.mana_max
        log_color_func(f"PARABÉNS! {self.nome} subiu para o nível {self.level}!", "levelup")

class Item:
    def __init__(self, nome, tipo, valor, quantidade=1):
        self.nome = nome
        self.tipo = tipo
        self.valor = valor
        self.quantidade = quantidade

    def aplicar(self, jogador, alvo=None):
        if self.tipo == "pocao_hp":
            jogador.curar(self.valor)
        elif self.tipo == "pocao_mana":
            jogador.mana = min(jogador.mana + self.valor, jogador.mana_max)
            log_color_func(f"{jogador.nome} recuperou {self.valor} de mana.", "heal")
        elif self.tipo == "elixir_forca":
            jogador.atk_base += self.valor
            log_color_func(f"{jogador.nome} usou {self.nome} e ganhou {self.valor} de ATQ permanente!", "levelup")
        elif self.tipo == "elixir_defesa":
            jogador.dfn_base += self.valor
            log_color_func(f"{jogador.nome} usou {self.nome} e ganhou {self.valor} de DFN permanente!", "levelup")
        elif self.tipo == "bomba":
            if alvo:
                log_color_func(f"{jogador.nome} arremessou {self.nome} causando {self.valor} de dano!", "skill")
                alvo.receber_dano(self.valor)
            else:
                log_func("Nenhum alvo para a bomba.")
        elif self.tipo.startswith("arma") or self.tipo == "armadura" or self.tipo.startswith("acessorio_"):
            jogador.equipar(self)
        else:
            log_func(f"{self.nome} não tem efeito definido.")

class Inimigo(Personagem):
    def __init__(self, nome, hp, atk, dfn, xp_recompensa, ouro_recompensa, elemento="neutro"):
        super().__init__(nome, hp, atk, dfn, elemento=elemento)
        self.xp_recompensa = xp_recompensa
        self.ouro_recompensa = ouro_recompensa

    def atacar(self, alvo):
        dano = self.atk_base + random.randint(-2, 1)
        dano = self.calcular_dano(dano, self.elemento, alvo)
        log_func(f"{self.nome} ataca causando {dano} de dano!")
        alvo.receber_dano(dano)

class Goblin(Inimigo):
    def __init__(self, level=1):
        super().__init__("Goblin", hp=10+level*2, atk=4+level, dfn=0+level//2,
                         xp_recompensa=12+level*2, ouro_recompensa=8+level*2, elemento="neutro")

class Slime(Inimigo):
    def __init__(self, level=1):
        super().__init__("Slime", hp=20+level*3, atk=2+level, dfn=0+level//2,
                         xp_recompensa=15+level*2, ouro_recompensa=10+level*2, elemento="neutro")
    def atacar(self, alvo):
        super().atacar(alvo)
        cura = max(2, self.level + 1)
        self.hp = min(self.hp + cura, self.hp_max)
        log_color_func(f"{self.nome} se regenerou por {cura} HP.", "heal")

class Orc(Inimigo):
    def __init__(self, level=1):
        super().__init__("Orc", hp=25+level*3, atk=6+level, dfn=2+level//2,
                         xp_recompensa=20+level*3, ouro_recompensa=15+level*3, elemento="neutro")

class Esqueleto(Inimigo):
    def __init__(self, level=1):
        super().__init__("Esqueleto", hp=15+level*2, atk=5+level, dfn=4+level,
                         xp_recompensa=18+level*3, ouro_recompensa=12+level*2, elemento="neutro")

class LoboMutante(Inimigo):
    def __init__(self, level=1):
        super().__init__("Lobo Mutante", hp=15+level*2, atk=8+level, dfn=1+level//2,
                         xp_recompensa=25+level*3, ouro_recompensa=15+level*2, elemento="neutro")
    def atacar(self, alvo):
        super().atacar(alvo)
        if random.random() < 0.25:
            log_color_func(f"{self.nome} ataca novamente devido à sua velocidade!", "damage")
            super().atacar(alvo)

class ChefaoOrc(Inimigo):
    def __init__(self, level=1):
        super().__init__("Rei Orc (Chefe)", hp=60+level*8, atk=9+level*2, dfn=4+level,
                         xp_recompensa=120+level*10, ouro_recompensa=100+level*10, elemento="fogo")
    def atacar(self, alvo):
        dano = self.atk_base + random.randint(2, 5)
        log_color_func(f"{self.nome} desfere um GOLPE ESMAGADOR causando {dano} de dano!", "critical")
        alvo.receber_dano(dano)

class Dragao(Inimigo):
    def __init__(self, level=2):
        super().__init__("Dragão", hp=80+level*8, atk=12+level*2, dfn=6+level,
                         xp_recompensa=180+level*5, ouro_recompensa=150+level*5, elemento="fogo")

class RPGApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG POO")
        self.root.geometry("850x700")

        global log_func, log_color_func
        log_func = self.log
        log_color_func = self.log_color

        self.player = None
        self.current_enemy = None
        self.in_combat = False
        self.in_event = False

        self.create_widgets()
        self.root.after(100, self.start_game)

    def create_widgets(self):
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass
        style.configure("TProgressbar", thickness=15)
        style.configure("HP.Horizontal.TProgressbar", foreground="red", background="red")
        style.configure("MP.Horizontal.TProgressbar", foreground="blue", background="blue")
        style.configure("XP.Horizontal.TProgressbar", foreground="yellow", background="gold")

        self.top_frame = tk.Frame(self.root, bg="#2b2b2b")
        self.top_frame.pack(fill=tk.X, padx=5, pady=5)

        self.lbl_name = tk.Label(self.top_frame, text="Nome: ---", font=("Helvetica", 12, "bold"), bg="#2b2b2b", fg="white")
        self.lbl_name.grid(row=0, column=0, padx=10, sticky="w")
        self.lbl_class = tk.Label(self.top_frame, text="Classe: ---", font=("Helvetica", 10), bg="#2b2b2b", fg="#aaa")
        self.lbl_class.grid(row=1, column=0, padx=10, sticky="w")
        
        self.lbl_dias = tk.Label(self.top_frame, text="Dia: 1", font=("Helvetica", 10, "italic"), bg="#2b2b2b", fg="#0fff0f")
        self.lbl_dias.grid(row=2, column=0, padx=10, sticky="w")

        self.lbl_level = tk.Label(self.top_frame, text="Nível: 1", font=("Helvetica", 12, "bold"), bg="#2b2b2b", fg="white")
        self.lbl_level.grid(row=0, column=1, padx=20)
        self.lbl_gold = tk.Label(self.top_frame, text="Ouro: 0", font=("Helvetica", 12, "bold"), bg="#2b2b2b", fg="gold")
        self.lbl_gold.grid(row=1, column=1, padx=20)

        self.lbl_atk_dfn = tk.Label(self.top_frame, text="ATK: ? | DFN: ?", font=("Helvetica", 10), bg="#2b2b2b", fg="white")
        self.lbl_atk_dfn.grid(row=0, column=2, padx=10, sticky="w")
        
        self.lbl_equips = tk.Label(self.top_frame, text="Arma: Nenhuma | Armadura: Nenhuma", font=("Helvetica", 8), bg="#2b2b2b", fg="#aaa")
        self.lbl_equips.grid(row=1, column=2, padx=10, sticky="w")
        
        self.lbl_acessorio = tk.Label(self.top_frame, text="Acessório: Nenhum", font=("Helvetica", 8), bg="#2b2b2b", fg="#aaa")
        self.lbl_acessorio.grid(row=2, column=2, padx=10, sticky="w")

        frame_bars = tk.Frame(self.top_frame, bg="#2b2b2b")
        frame_bars.grid(row=0, column=3, rowspan=3, padx=20, sticky="e")

        tk.Label(frame_bars, text="HP:", bg="#2b2b2b", fg="white").grid(row=0, column=0, sticky="e")
        self.bar_hp = ttk.Progressbar(frame_bars, style="HP.Horizontal.TProgressbar", orient="horizontal", length=200, mode="determinate")
        self.bar_hp.grid(row=0, column=1, pady=2)
        self.lbl_hp_text = tk.Label(frame_bars, text="0/0", bg="#2b2b2b", fg="white", width=8)
        self.lbl_hp_text.grid(row=0, column=2, padx=5)

        tk.Label(frame_bars, text="MP:", bg="#2b2b2b", fg="white").grid(row=1, column=0, sticky="e")
        self.bar_mp = ttk.Progressbar(frame_bars, style="MP.Horizontal.TProgressbar", orient="horizontal", length=200, mode="determinate")
        self.bar_mp.grid(row=1, column=1, pady=2)
        self.lbl_mp_text = tk.Label(frame_bars, text="0/0", bg="#2b2b2b", fg="white", width=8)
        self.lbl_mp_text.grid(row=1, column=2, padx=5)

        tk.Label(frame_bars, text="XP:", bg="#2b2b2b", fg="white").grid(row=2, column=0, sticky="e")
        self.bar_xp = ttk.Progressbar(frame_bars, style="XP.Horizontal.TProgressbar", orient="horizontal", length=200, mode="determinate")
        self.bar_xp.grid(row=2, column=1, pady=2)
        self.lbl_xp_text = tk.Label(frame_bars, text="0/0", bg="#2b2b2b", fg="white", width=8)
        self.lbl_xp_text.grid(row=2, column=2, padx=5)

        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.log_text = scrolledtext.ScrolledText(self.middle_frame, state='disabled', height=14, bg="#fafafa", font=("Consolas", 11))
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.log_text.tag_config("damage", foreground="#cc0000")
        self.log_text.tag_config("heal", foreground="#008800")
        self.log_text.tag_config("skill", foreground="#8800cc")
        self.log_text.tag_config("critical", foreground="#ff0000", font=("Consolas", 11, "bold"))
        self.log_text.tag_config("info", foreground="#0000bb")
        self.log_text.tag_config("levelup", foreground="#dd8800", font=("Consolas", 11, "bold"))
        self.log_text.tag_config("xp", foreground="#888800")
        self.log_text.tag_config("weak", foreground="#888888")

        self.enemy_frame = tk.Frame(self.root, bg="#3b1b1b")
        self.enemy_frame.pack(fill=tk.X, padx=5, pady=5)

        self.lbl_enemy_name = tk.Label(self.enemy_frame, text="Nenhum Inimigo", font=("Helvetica", 14, "bold"), bg="#3b1b1b", fg="white")
        self.lbl_enemy_name.pack(side=tk.TOP, pady=5)
        self.bar_enemy_hp = ttk.Progressbar(self.enemy_frame, style="HP.Horizontal.TProgressbar", orient="horizontal", length=400, mode="determinate")
        self.bar_enemy_hp.pack(side=tk.TOP, pady=5)
        self.lbl_enemy_hp_text = tk.Label(self.enemy_frame, text="", bg="#3b1b1b", fg="white")
        self.lbl_enemy_hp_text.pack(side=tk.TOP, pady=2)

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill=tk.X, padx=5, pady=5)

        self.btn_attack = ttk.Button(self.bottom_frame, text="Atacar", command=self.player_attack, state=tk.DISABLED)
        self.btn_attack.pack(side=tk.LEFT, padx=5)

        self.btn_skills = ttk.Button(self.bottom_frame, text="Habilidades", command=self.show_skills, state=tk.DISABLED)
        self.btn_skills.pack(side=tk.LEFT, padx=5)

        self.btn_items = ttk.Button(self.bottom_frame, text="Inventário", command=self.show_items, state=tk.DISABLED)
        self.btn_items.pack(side=tk.LEFT, padx=5)

        self.btn_flee = ttk.Button(self.bottom_frame, text="Fugir", command=self.player_flee, state=tk.DISABLED)
        self.btn_flee.pack(side=tk.LEFT, padx=5)

        self.btn_continue = ttk.Button(self.bottom_frame, text="Explorar...", command=self.next_step, state=tk.DISABLED)
        self.btn_continue.pack(side=tk.LEFT, padx=5)

        self.btn_quit = ttk.Button(self.bottom_frame, text="Sair", command=self.root.quit)
        self.btn_quit.pack(side=tk.RIGHT, padx=5)

    def start_game(self):
        class_win = tk.Toplevel(self.root)
        class_win.title("Criação de Personagem")
        class_win.geometry("300x250")
        class_win.protocol("WM_DELETE_WINDOW", self.root.quit)
        class_win.grab_set()

        tk.Label(class_win, text="Nome do Personagem:").pack(pady=5)
        name_var = tk.StringVar()
        tk.Entry(class_win, textvariable=name_var).pack()

        tk.Label(class_win, text="Escolha a Classe:").pack(pady=5)
        class_var = tk.StringVar(value="Guerreiro")
        classes = ["Guerreiro", "Mago", "Ladino"]
        for cls in classes:
            tk.Radiobutton(class_win, text=cls, variable=class_var, value=cls).pack()

        def confirm():
            if name_var.get().strip():
                nome = name_var.get().strip()
                classe = class_var.get()
                self.player = Jogador(nome, classe)
                
                self.player.inventario.append(Item("Poção de HP (Maior)", "pocao_hp", 60, 2))
                self.player.inventario.append(Item("Poção de Mana", "pocao_mana", 30, 2))
                self.player.inventario.append(Item("Pequena Faca", "arma", 3, 1))
                if classe == "Guerreiro":
                    self.player.inventario.append(Item("Armadura de Pano", "armadura", 3, 1))
                elif classe == "Mago":
                    self.player.inventario.append(Item("Anel de Quartzo", "acessorio_mp", 10, 1))

                self.update_stats()
                self.log_color("Bem-vindo ao RPG POO", "info")
                self.log(f"Sua jornada começa agora como {classe}.")
                
                class_win.destroy()
                self.enable_continue_button(True)
            else:
                messagebox.showerror("Erro", "Nome não pode ficar vazio.")

        tk.Button(class_win, text="Confirmar", command=confirm).pack(pady=15)

    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
    def log_color(self, message, tag):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def update_stats(self):
        if self.player:
            self.lbl_name.config(text=f"Nome: {self.player.nome}")
            self.lbl_class.config(text=f"Classe: {self.player.classe_nome}")
            self.lbl_level.config(text=f"Nível: {self.player.level}")
            self.lbl_gold.config(text=f"Ouro: {self.player.ouro}")
            self.lbl_dias.config(text=f"Dia: {self.player.dias}")
            self.lbl_atk_dfn.config(text=f"ATK: {self.player.atk_total} | DFN: {self.player.dfn_total}")
            
            nome_arma = self.player.arma_equipada.nome if self.player.arma_equipada else "Nenhuma"
            nome_armadura = self.player.armadura_equipada.nome if self.player.armadura_equipada else "Nenhuma"
            nome_acessorio = self.player.acessorio_equipado.nome if self.player.acessorio_equipado else "Nenhum"
            
            self.lbl_equips.config(text=f"Arma: {nome_arma} | Armadura: {nome_armadura}")
            self.lbl_acessorio.config(text=f"Acessório: {nome_acessorio}")

            self.bar_hp['maximum'] = self.player.hp_max
            self.bar_hp['value'] = self.player.hp
            self.lbl_hp_text.config(text=f"{self.player.hp}/{self.player.hp_max}")

            self.bar_mp['maximum'] = self.player.mana_max
            self.bar_mp['value'] = self.player.mana
            self.lbl_mp_text.config(text=f"{self.player.mana}/{self.player.mana_max}")

            self.bar_xp['maximum'] = self.player.xp_para_proximo_level
            self.bar_xp['value'] = self.player.xp
            self.lbl_xp_text.config(text=f"{self.player.xp}/{self.player.xp_para_proximo_level}")

    def update_enemy_info(self):
        if self.current_enemy and self.current_enemy.esta_vivo():
            self.lbl_enemy_name.config(text=f"{self.current_enemy.nome} (Nível {self.current_enemy.level}) - {self.current_enemy.elemento.upper()}")
            self.bar_enemy_hp['maximum'] = self.current_enemy.hp_max
            self.bar_enemy_hp['value'] = self.current_enemy.hp
            self.lbl_enemy_hp_text.config(text=f"{self.current_enemy.hp}/{self.current_enemy.hp_max}")
        else:
            self.lbl_enemy_name.config(text="Nenhum Inimigo")
            self.bar_enemy_hp['value'] = 0
            self.lbl_enemy_hp_text.config(text="")

    def enable_combat_buttons(self, enable=True):
        state = tk.NORMAL if enable else tk.DISABLED
        self.btn_attack.config(state=state)
        self.btn_skills.config(state=state)
        self.btn_items.config(state=state)
        self.btn_flee.config(state=state)
        self.btn_continue.config(state=tk.DISABLED)

    def enable_continue_button(self, enable=True):
        self.btn_continue.config(state=tk.NORMAL if enable else tk.DISABLED)
        if enable:
            self.btn_attack.config(state=tk.DISABLED)
            self.btn_skills.config(state=tk.DISABLED)
            self.btn_items.config(state=tk.DISABLED)
            self.btn_flee.config(state=tk.DISABLED)

    def next_step(self):
        if not self.player.esta_vivo():
            self.log("Você morreu. Fim de jogo.")
            self.enable_continue_button(False)
            return

        if self.player.batalhas_vencidas > 0 and self.player.batalhas_vencidas % 5 == 0:
            self.start_combat(boss=True)
            self.player.batalhas_vencidas += 1 
            return

        chance = random.random()
        if chance < 0.40:
            self.start_event()
        else:
            self.start_combat()

    def start_event(self):
        self.in_event = True
        self.enable_combat_buttons(False)
        self.btn_continue.config(state=tk.DISABLED)
        self.log("\n--- Explorando... ---")
        
        # Evento enigma mais raro
        evento = random.choices(
            ["baú", "armadilha", "descanso", "mercador", "santuario", "enigma", "nada"],
            weights=[20, 10, 15, 15, 15, 10, 15],
            k=1
        )[0]
        
        if evento == "baú":
            self.event_chest()
        elif evento == "armadilha":
            self.event_trap()
        elif evento == "descanso":
            self.event_rest()
        elif evento == "mercador":
            self.event_merchant()
        elif evento == "santuario":
            self.event_santuario()
        elif evento == "enigma":
            self.event_enigma()
        elif evento == "nada":
            self.log("Você caminhou por horas e não encontrou nada de interessante.")
            self.after_event()
            
    def event_chest(self):
        if random.random() < 0.7:
            item_sorteado = random.choice([
                Item("Poção de HP Excelente", "pocao_hp", 120),
                Item("Poção de Mana Média", "pocao_mana", 60),
                Item("Bomba Poderosa", "bomba", 80),
                Item("Chapéu de Aventureiro", "armadura", 4),
                Item("Anel do Vigor", "acessorio_hp", 30)
            ])
            item_existente = next((i for i in self.player.inventario if i.nome == item_sorteado.nome and i.tipo not in ["arma", "armadura", 'acessorio_hp']), None)
            if item_existente:
                item_existente.quantidade += 1
            else:
                self.player.inventario.append(item_sorteado)
            self.log_color(f"Você encontrou um baú de madeira! Obteve: {item_sorteado.nome}!", "info")
        else:
            ouro = random.randint(30, 70)
            self.player.ouro += ouro
            self.log_color(f"Você encontrou um baú pequeno com {ouro} de ouro!", "info")
        self.after_event()

    def event_trap(self):
        dano = random.randint(5, 15)
        self.log_color(f"Você caiu em uma armadilha cravada no chão, perdendo {dano} de HP!", "damage")
        self.player.receber_dano(dano)
        self.after_event()

    def event_rest(self):
        cura = random.randint(25, 50)
        self.player.curar(cura)
        mana = random.randint(15, 30)
        self.player.mana = min(self.player.mana + mana, self.player.mana_max)
        self.player.dias += 1
        self.log_color(f"A noite cai. Você monta acampamento (+{cura} HP, +{mana} MP). O dia amanhece.", "weak")
        self.after_event()

    def event_santuario(self):
        self.log_color("Você encontrou um Santuário Misterioso brilhante na floresta!", "info")
        self.player.hp = self.player.hp_max
        self.player.mana = self.player.mana_max
        self.log_color("Uma luz divina te envolve. HP e Mana estão completamente restaurados!", "heal")
        if random.random() < 0.35:
            self.log_color("Você se sente imbuído com conhecimento divino...", "levelup")
            self.player.subir_nivel()
        self.after_event()

    def event_merchant(self):
        self.log_color("Um mercador ambulante suspeito te oferece itens!", "info")
        self.open_shop()

    def event_enigma(self):
        self.log_color("Um SAPO GIGANTE COM UM CACHIMBO bloqueia seu caminho...", "info")
        self.log("- 'Viajante... responda minha charada ou pague o preço!'")
        
        charadas = [
            ("O que é, o que é: tem pernas mas não anda, tem braço mas não abraça?", ["cadeira", "poltrona"]),
            ("Mudo de forma dependendo da temperatura. Posso curar sua sede ou quebrar seus ossos. O que sou?", ["agua", "água"]),
            ("Eu caio mas nunca quebro, a noite cai mas não se machuca. O que sou eu?", ["noite", "sombra", "escuridao", "escuridão"])
        ]
        
        charada, respostas = random.choice(charadas)
        
        self.log(f"Sapo sussurra: '{charada}'")
        res = simpledialog.askstring("O Enigma do Sapo", charada, parent=self.root)
        
        if res and res.lower().strip() in respostas:
            self.log_color("- 'Excelente... O conhecimento é poder.'", "levelup")
            anel = Item("Amuleto do Mestre", "acessorio_atk", 5)
            self.player.inventario.append(anel)
            self.log_color("Você ganhou um Amuleto do Mestre (+5 Todos os Danos) e +25 XP!", "xp")
            self.player.ganhar_xp(25)
        else:
            self.log_color("- 'Idiota. A ignorância dói.' O Sapo cospe em você e some.", "damage")
            self.player.receber_dano(20)

        self.after_event()

    def open_shop(self):
        shop_win = tk.Toplevel(self.root)
        shop_win.title("Mercador")
        shop_win.geometry("400x350")
        shop_win.grab_set()

        itens_venda = [
            Item("Poção HP (Maior)", "pocao_hp", 60, 1),
            Item("Poção HP (Divina)", "pocao_hp", 200, 1),
            Item("Poção Mana (Maior)", "pocao_mana", 100, 1),
            Item("Nova Granada", "bomba", 100, 1),
            Item("Elixir Força Divina", "elixir_forca", 4, 1),
            Item("Espada Larga", "arma", 10, 1),
            Item("Malha de Aço", "armadura", 8, 1),
            Item("Anel de Ferro", "acessorio_dfn", 2, 1) # Novo acessório na loja
        ]
        precos = [25, 80, 55, 70, 250, 180, 150, 120]

        tk.Label(shop_win, text=f"Seu ouro: {self.player.ouro}", font=("Arial", 10, "bold")).pack(pady=5)

        listbox = tk.Listbox(shop_win, font=("Arial", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for i, item in enumerate(itens_venda):
            listbox.insert(tk.END, f"{item.nome} ({item.tipo}) - {precos[i]} ouro")

        def buy():
            selection = listbox.curselection()
            if selection:
                idx = selection[0]
                if self.player.ouro >= precos[idx]:
                    self.player.ouro -= precos[idx]
                    item_comprado = itens_venda[idx]
                    
                    is_stackable = item_comprado.tipo in ["pocao_hp", "pocao_mana", "elixir_forca", "elixir_defesa", "bomba"]
                    item_existente = next((i for i in self.player.inventario if i.nome == item_comprado.nome), None)
                    
                    if item_existente and is_stackable:
                        item_existente.quantidade += 1
                    else:
                        copia = Item(item_comprado.nome, item_comprado.tipo, item_comprado.valor, 1)
                        self.player.inventario.append(copia)
                        
                    self.log(f"Você comprou: {item_comprado.nome}")
                    self.update_stats()
                    # Atualiza o title do shop_win ouro
                    tk.Label(shop_win, text=f"Seu ouro: {self.player.ouro}", font=("Arial", 10, "bold")).place(x=0,y=0, relwidth=1)
                else:
                    messagebox.showerror("Aviso", "Ouro insuficiente!")

        def on_close():
            shop_win.destroy()
            self.log("Você ignorou o mercador.")
            self.after_event()

        shop_win.protocol("WM_DELETE_WINDOW", on_close)
        tk.Button(shop_win, text="Comprar Mais (Não Sai da Loja)", command=buy).pack(pady=5)
        tk.Button(shop_win, text="Concluir e Sair", command=on_close).pack(pady=5)

    def after_event(self):
        self.update_stats()
        if not self.player.esta_vivo():
            self.log("Você morreu devido aos ferimentos do evento. Fim de jogo.")
            self.enable_continue_button(False)
            return
        self.in_event = False
        self.enable_continue_button(True)

    def start_combat(self, boss=False):
        if boss:
            nivel_inimigo = self.player.level + 2
            classe_inimigo = random.choice([ChefaoOrc, Dragao])
            self.log_color("!!! UM CHEFÃO PODEROSO BLOQUEIA SEU CAMINHO !!!", "critical")
        else:
            nivel_inimigo = max(1, self.player.level + random.randint(-1, 0)) # Um pouco mais fácil, mobs não serão lvl+1
            classe_inimigo = random.choice([Goblin, Slime, Orc, Esqueleto, LoboMutante])
        
        self.current_enemy = classe_inimigo(level=nivel_inimigo)
        self.in_combat = True
        self.log_color(f"\nUm(a) {self.current_enemy.nome} nivel {self.current_enemy.level} apareceu!", "info")
        self.update_enemy_info()
        self.enable_combat_buttons(True)

    def player_attack(self):
        if not self.in_combat or not self.current_enemy or not self.current_enemy.esta_vivo():
            return
        self.player.atacar(self.current_enemy)
        self.update_stats()
        self.update_enemy_info()
        if not self.current_enemy.esta_vivo():
            self.victory()
            return
        self.enable_combat_buttons(False)
        self.root.after(500, self.enemy_turn)

    def enemy_turn(self):
        if self.current_enemy and self.current_enemy.esta_vivo() and self.player.esta_vivo():
            self.current_enemy.atacar(self.player)
            self.update_stats()
            self.update_enemy_info()
            if not self.player.esta_vivo():
                self.defeat()
                return
        self.enable_combat_buttons(True)

    def player_flee(self):
        if not self.in_combat:
            return
        
        chance = 0.60
        if self.player.classe_nome == "Ladino":
            chance = 0.85 

        if random.random() < chance:
            self.log_color("Você meteu o pé e fugiu com sucesso da batalha!", "weak")
            self.current_enemy = None
            self.in_combat = False
            self.update_enemy_info()
            self.enable_combat_buttons(False)
            self.enable_continue_button(True)
        else:
            self.log_color("Você tentou fugir, mas tropeçou!", "damage")
            self.enable_combat_buttons(False)
            self.root.after(500, self.enemy_turn)

    def show_skills(self):
        if not self.in_combat:
            return
        skill_win = tk.Toplevel(self.root)
        skill_win.title("Habilidades")
        skill_win.geometry("300x200")

        for i, hab in enumerate(self.player.habilidades):
            ttk.Button(skill_win, text=f"{hab.nome} (Mana: {hab.custo_mana})",
                            command=lambda idx=i: self.use_skill(idx, skill_win)).pack(pady=5, fill=tk.X, padx=10)

    def use_skill(self, idx, win):
        win.destroy()
        if not self.in_combat or not self.current_enemy or not self.current_enemy.esta_vivo():
            return
            
        usou = self.player.usar_habilidade(idx, self.current_enemy)
        self.update_stats()
        self.update_enemy_info()
        
        if not self.current_enemy.esta_vivo():
            self.victory()
            return
        if usou:
            self.enable_combat_buttons(False)
            self.root.after(500, self.enemy_turn)

    def show_items(self):
        item_win = tk.Toplevel(self.root)
        item_win.title("Inventário")
        item_win.geometry("350x400")
        
        if not self.player.inventario and not self.player.arma_equipada and not self.player.armadura_equipada and not self.player.acessorio_equipado:
            tk.Label(item_win, text="Inventário vazio.").pack(pady=20)
            return

        if self.player.arma_equipada or self.player.armadura_equipada or self.player.acessorio_equipado:
            f_eq = tk.Frame(item_win)
            f_eq.pack(fill=tk.X, pady=5)
            if self.player.arma_equipada:
                ttk.Button(f_eq, text=f"Desequipar Arma", command=lambda: self.do_unequip("arma", item_win)).pack(side=tk.TOP, padx=5, pady=2)
            if self.player.armadura_equipada:
                ttk.Button(f_eq, text=f"Desequipar Armadura", command=lambda: self.do_unequip("armadura", item_win)).pack(side=tk.TOP, padx=5, pady=2)
            if self.player.acessorio_equipado:
                ttk.Button(f_eq, text=f"Desequipar Acessório", command=lambda: self.do_unequip("acessorio", item_win)).pack(side=tk.TOP, padx=5, pady=2)

        itens_unicos = []
        for item in self.player.inventario:
            itens_unicos.append(item)

        container_itens = tk.Frame(item_win)
        container_itens.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container_itens)
        scrollbar = ttk.Scrollbar(container_itens, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for i, item in enumerate(itens_unicos):
            acao = "Usar"
            if item.tipo in ["arma", "armadura"] or item.tipo.startswith("acessorio"): acao = "Equipar"

            btn_text = f"[{acao}] {item.nome} (x{item.quantidade})"
            ttk.Button(scrollable_frame, text=btn_text, command=lambda idx=i: self.use_item(idx, itens_unicos, item_win)).pack(pady=2, fill=tk.X, padx=10)

    def do_unequip(self, tipo, win):
        self.player.desequipar(tipo)
        self.update_stats()
        win.destroy()
        self.show_items()

    def use_item(self, idx, itens_unicos, win):
        win.destroy()
        if self.in_combat and (not self.current_enemy or not self.current_enemy.esta_vivo()):
            return
            
        item_usado = itens_unicos[idx]
        
        if item_usado.tipo == "bomba" and not self.in_combat:
            messagebox.showinfo("Aviso", "Bombas só podem ser usadas em combate!")
            return

        alvo = self.current_enemy if self.in_combat else None
        
        if item_usado.tipo in ["arma", "armadura"] or item_usado.tipo.startswith("acessorio"):
            self.player.equipar(item_usado)
        else:

            item_usado.aplicar(self.player, alvo)
            item_usado.quantidade -= 1
            if item_usado.quantidade <= 0:
                self.player.inventario.remove(item_usado)
        
        self.update_stats()
        self.update_enemy_info()
        
        if self.in_combat:
            if not self.current_enemy.esta_vivo():
                self.victory()
                return
            if self.player.esta_vivo():
                self.enable_combat_buttons(False)
                self.root.after(500, self.enemy_turn)

    def victory(self):
        self.log_color(f"VITÓRIA! O {self.current_enemy.nome} foi derrotado!", "levelup")
        self.player.batalhas_vencidas += 1
        self.player.ganhar_xp(self.current_enemy.xp_recompensa)
        self.player.ouro += self.current_enemy.ouro_recompensa
        self.log_color(f"Você encontrou {self.current_enemy.ouro_recompensa} de ouro nos espólios.", "info")
        
        chance_drop = 0.5
        if "Chefe" in self.current_enemy.nome:
            chance_drop = 1.0
            drops = [
                Item("Adaga Vampírica", "arma", 15, 1),
                Item("Machado Quebra Ossos", "arma", 18, 1),
                Item("Armadura Lendária", "armadura", 12, 1),
                Item("Elixir dos Deuses", "elixir_forca", 5, 1),
                Item("Coroa do Rei Orc", "acessorio_hp", 50, 1)
            ]
        else:
            drops = [
                Item("Poção HP (Maior)", "pocao_hp", 60, 1),
                Item("Poção Mana (Maior)", "pocao_mana", 60, 1),
                Item("Bomba Ardente", "bomba", 50, 1),
                Item("Faca de Combate", "arma", 4, 1),
                Item("Escudo de Madeira", "armadura", 3, 1),
                Item("Anel da Raposa", "acessorio_mp", 10, 1)
            ]
            
        if random.random() < chance_drop:
            item_sorteado = random.choice(drops)
            
            if item_sorteado.tipo in ["pocao_hp", "pocao_mana", "elixir_forca", "elixir_defesa", "bomba"]:
                item_existente = next((i for i in self.player.inventario if i.nome == item_sorteado.nome), None)
                if item_existente:
                    item_existente.quantidade += 1
                else:
                    copia = Item(item_sorteado.nome, item_sorteado.tipo, item_sorteado.valor, 1)
                    self.player.inventario.append(copia)
            else:
                 copia = Item(item_sorteado.nome, item_sorteado.tipo, item_sorteado.valor, 1)
                 self.player.inventario.append(copia)
                 
            self.log_color(f"DROP: Você encontrou um(a) {item_sorteado.nome}!", "weak")

        self.update_stats()
        self.current_enemy = None
        self.in_combat = False
        self.update_enemy_info()
        self.enable_combat_buttons(False)
        self.enable_continue_button(True)

    def defeat(self):
        self.log_color("Você foi derrotado em combate... A escuridão te consome. Fim de jogo.", "critical")
        self.enable_combat_buttons(False)
        self.enable_continue_button(False)
        self.current_enemy = None
        self.update_enemy_info()

if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    app = RPGApp(root)
    root.mainloop()