import tkinter as tk
from tkinter import messagebox
import random

class FortuneTigerAdivinhacao:
    def __init__(self, root):
        self.root = root
        self.root.title("🐯 FORTUNE TIGER - ADIVINHAÇÃO 🐯")
        self.root.geometry("460x480")
        self.root.resizable(False, False)

        # Paleta de cores inspirada no Fortune Tiger (Vermelho Imperial e Ouro)
        self.bg_principal = "#8B0000"      # Vermelho escuro vibrante
        self.bg_card = "#B22222"           # Vermelho médio para painéis
        self.cor_ouro = "#FFD700"          # Dourado brilhante
        self.cor_ouro_escuro = "#DAA520"   # Dourado metálico
        self.cor_laranja = "#FF8C00"       # Laranja tigre
        self.cor_verde = "#00FF7F"         # Verde vitória (Big Win)

        self.root.configure(bg=self.bg_principal)

        # Mecânica de aposta
        self.saldo_inicial = 1000
        self.custo_palpite = 50
        self.animando = False
        self.reiniciar_jogo()

        # --- BANNER TOPO ---
        self.lbl_titulo = tk.Label(
            root,
            text="🐯 FORTUNE NUMBER 🐯",
            font=("Impact", 22),
            bg=self.bg_principal,
            fg=self.cor_ouro
        )
        self.lbl_titulo.pack(pady=(12, 5))

        # --- PAINEL DE SALDO ---
        self.frame_topo = tk.Frame(
            root, bg=self.bg_card, bd=4, relief="ridge", highlightbackground=self.cor_ouro, highlightthickness=2
        )
        self.frame_topo.pack(fill="x", padx=25, pady=8)

        self.lbl_saldo = tk.Label(
            self.frame_topo,
            text=f"💰 SALDO: R$ {self.saldo},00 💰",
            font=("Arial Black", 15),
            bg=self.bg_card,
            fg=self.cor_ouro
        )
        self.lbl_saldo.pack(pady=10)

        # --- INSTRUÇÕES ---
        self.lbl_instrucoes = tk.Label(
            root,
            text="🔥 Escolha um número da sorte (1 a 100) 🔥\nCada giro custa R$ 50 | Prêmio: R$ 500 (10x!)",
            font=("Arial", 10, "bold"),
            bg=self.bg_principal,
            fg="#FFE4B5"
        )
        self.lbl_instrucoes.pack(pady=8)

        # --- VISOR / ENTRADA ESTILIZADA (SLOT) ---
        self.frame_slot = tk.Frame(root, bg=self.cor_ouro, bd=4, relief="raised")
        self.frame_slot.pack(pady=10)

        self.txt_palpite = tk.Entry(
            self.frame_slot,
            font=("Impact", 32),
            justify="center",
            width=4,
            bg="#FFF8DC",       # Creme claro estilo rolo de caça-níquel
            fg="#B22222",
            insertbackground="#B22222",
            bd=0
        )
        self.txt_palpite.pack(padx=6, pady=6)
        self.txt_palpite.bind("<Return>", lambda event: self.iniciar_giro())

        # --- BOTÃO SPIN CHAMATIVO ---
        self.btn_enviar = tk.Button(
            root,
            text="🎰 GIRAR AGORA 🎰",
            command=self.iniciar_giro,
            font=("Arial Black", 14),
            bg=self.cor_ouro,
            fg="#8B0000",
            activebackground=self.cor_laranja,
            activeforeground="#FFFFFF",
            bd=5,
            relief="raised",
            padx=25,
            pady=10,
            cursor="hand2"
        )
        self.btn_enviar.pack(pady=12)

        # --- FEEDBACK DE STATUS ---
        self.lbl_feedback = tk.Label(
            root,
            text="🧧 O Tigre soltou a carta! Faça sua aposta! 🧧",
            font=("Arial", 11, "bold"),
            bg=self.bg_principal,
            fg=self.cor_ouro
        )
        self.lbl_feedback.pack(pady=10)

    def reiniciar_jogo(self):
        self.numero_secreto = random.randint(1, 100)
        if not hasattr(self, 'saldo') or self.saldo <= 0:
            self.saldo = self.saldo_inicial

    def atualizar_interface_saldo(self):
        self.lbl_saldo.config(text=f"💰 SALDO: R$ {self.saldo},00 💰")

    def iniciar_giro(self):
        if self.animando:
            return

        entrada = self.txt_palpite.get().strip()
        if not entrada.isdigit() or not (1 <= int(entrada) <= 100):
            messagebox.showwarning("Aviso do Tigre 🐯", "Digite um número válido entre 1 e 100!")
            self.txt_palpite.delete(0, tk.END)
            return

        palpite = int(entrada)
        self.animando = True
        self.btn_enviar.config(state="disabled", text="⏳ GIRANDO... ⏳")
        self.lbl_feedback.config(text="✨ Cruzando os dedos... ✨", fg="#FFFFFF")

        # Efeito visual de animação antes de revelar o resultado
        self.animar_roleta(0, palpite)

    def animar_roleta(self, passo, palpite_final):
        if passo < 8:
            cor_atual = self.cor_ouro if passo % 2 == 0 else self.cor_laranja
            self.frame_slot.config(bg=cor_atual)
            self.root.after(70, lambda: self.animar_roleta(passo + 1, palpite_final))
        else:
            self.frame_slot.config(bg=self.cor_ouro)
            self.animando = False
            self.btn_enviar.config(state="normal", text="🎰 GIRAR AGORA 🎰")
            self.verificar_palpite(palpite_final)

    def verificar_palpite(self, palpite):
        self.saldo -= self.custo_palpite
        self.atualizar_interface_saldo()

        if palpite < self.numero_secreto:
            self.lbl_feedback.config(text="⬆️ QUASE! Tente um número MAIOR! ⬆️", fg="#FFA07A")
        elif palpite > self.numero_secreto:
            self.lbl_feedback.config(text="⬇️ QUASE! Tente um número MENOR! ⬇️", fg="#FFA07A")
        else:
            premio = 500
            self.saldo += premio
            self.atualizar_interface_saldo()
            self.lbl_feedback.config(text="🎉 BIG WIN! O TIGRE PAGOU! 🎉", fg=self.cor_verde)

            resposta = messagebox.askyesno(
                "🐯 CARTA DO TIGRE! 🐯",
                f"🔥 GRANDE GANHO! 🔥\nVocê acertou o número {self.numero_secreto}!\nGanhou R$ {premio},00!\n\nDeseja continuar girando?"
            )
            if resposta:
                self.reiniciar_jogo()
                self.lbl_feedback.config(text="🧧 Nova rodada! O Tigre está pagando! 🧧", fg=self.cor_ouro)
            else:
                self.root.destroy()
                return

        if self.saldo <= 0:
            messagebox.showerror("Saldo Zerado 😿", "Suas moedas acabaram!")
            resposta = messagebox.askyesno("Recarga Bônus 🎁", "Pegar bônus de R$ 1.000,00 para continuar?")
            if resposta:
                self.saldo = self.saldo_inicial
                self.reiniciar_jogo()
                self.atualizar_interface_saldo()
                self.lbl_feedback.config(text="💰 Bônus ativado! Boa sorte! 💰", fg=self.cor_ouro)
            else:
                self.root.destroy()
                return

        self.txt_palpite.delete(0, tk.END)

if __name__ == "__main__":
    janela = tk.Tk()
    app = FortuneTigerAdivinhacao(janela)
    janela.mainloop()
