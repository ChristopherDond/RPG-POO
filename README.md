⚔️ RPG POO:
Um jogo de RPG por turnos com interface gráfica, desenvolvido inteiramente em Python para exercitar conceitos de Programação Orientada a Objetos (POO).

Este projeto simula uma aventura clássica onde o jogador escolhe uma classe, enfrenta monstros, gerencia recursos e sobe de nível, tudo isso em uma interface construída com a biblioteca tkinter.


🚀 Funcionalidades
Sistema de Classes: Escolha entre Guerreiro, Mago ou Ladino, cada um com atributos e habilidades únicas.

Combate por Turnos: Sistema de dano calculado com base em ataque, defesa e vantagens elementais (Fogo > Gelo).

Progressão: Ganho de XP, subida de nível e evolução de atributos.

Eventos Aleatórios: Encontros com mercadores, baús de tesouro, armadilhas e até charadas propostas por um sapo gigante!

Gerenciamento de Inventário: Equipar armas, armaduras e usar poções de cura ou mana.

Interface Colorida: Log de combate dinâmico com cores para destacar danos, curas e eventos críticos.


🧠 Conceitos de POO Aplicados
O objetivo principal deste projeto foi a prática de:

Abstração: Uso da classe Personagem como uma ABC (Abstract Base Class).

Herança: Criação de diversos inimigos (Goblin, Orc, Dragão) herdando da classe base.

Encapsulamento: Gerenciamento de atributos como HP e Mana através de properties.

Polimorfismo: Métodos de ataque que se comportam de forma diferente dependendo do tipo de inimigo ou classe do jogador.


🛠️ Como Instalar e Jogar
Pré-requisitos
Você só precisa do Python 3.x instalado no seu computador. A biblioteca de interface gráfica tkinter geralmente já vem inclusa na instalação padrão do Python.

Passo a Passo
Baixe o código:
Clone o repositório ou copie o código para um arquivo chamado main.py.

Bash
git clone https://github.com/seu-usuario/rpg-poo-python.git
cd rpg-poo-python
Execute o jogo:
No terminal ou prompt de comando, dentro da pasta do arquivo, digite:

Bash
python main.py
Como Jogar
Criação: Digite o nome do seu herói e escolha sua classe inicial.


Exploração: Clique em "Explorar..." para avançar na jornada. Você pode encontrar um monstro ou um evento pacífico.

Combate: * Use Atacar para um golpe físico simples.

Use Habilidades para gastar Mana e desferir golpes poderosos ou se curar.

Use Inventário para usar itens ou trocar seus equipamentos.

Evolução: Fique de olho na barra de XP. A cada 5 batalhas vencidas, prepare-se para um Chefe!

📜 Licença
Este projeto é de código aberto sob a licença MIT. Sinta-se à vontade para clonar, modificar e melhorar o sistema!

Desenvolvido com ☕ e Python para fins de estudo.
