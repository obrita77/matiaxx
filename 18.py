from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty
from kivy.animation import Animation

class VerificadorIdadeApp(App):
    resultado_texto = StringProperty('')
    historico = ListProperty([])  # Armazena o histórico de verificações

    def build(self):
        """Cria e organiza todos os elementos da interface gráfica."""
        Window.clearcolor = (0.1, 0.15, 0.25, 1)  # Azul escuro

        self.layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint=(1, 1)
        )

        # Título
        titulo = Label(
            text='Verificador de Idade',
            font_size='24sp',
            bold=True,
            color=(0.9, 0.9, 0.95, 1),
            size_hint_y=None,
            height=50
        )

        # Campo para nome
        self.nome_input = TextInput(
            hint_text='Digite seu nome',
            size_hint_y=None,
            height=45,
            font_size='16sp',
            background_color=(0.2, 0.25, 0.3, 1),
            foreground_color=(1, 1, 1, 1),
            multiline=False
        )

        # Campo para idade
        self.idade_input = TextInput(
            hint_text='Digite sua idade (0-120)',
            size_hint_y=None,
            height=45,
            font_size='16sp',
            input_filter='int',
            background_color=(0.2, 0.25, 0.3, 1),
            foreground_color=(1, 1, 1, 1),
            multiline=False
        )

        # Botão de verificação
        enviar_btn = Button(
            text='VERIFICAR IDADE',
            size_hint_y=None,
            height=50,
            font_size='16sp',
            background_color=(0.4, 0.6, 0.8, 1),
            background_normal='',
            color=(1, 1, 1, 1),
            bold=True
        )
        enviar_btn.bind(on_press=self.animar_botao)
        enviar_btn.bind(on_release=self.verificar_idade)

        # Label para resultado com emojis
        self.resultado_label = Label(
            text='',
            font_size='18sp',
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50,
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.9, None),
            markup=True
        )

        # Label para histórico de verificações
        self.historico_label = Label(
            text='Histórico de verificações:\n',
            font_size='15sp',
            color=(0.9, 0.9, 0.95, 1),
            halign='left',
            valign='top',
            size_hint_y=None,
            height=200
        )

        # Adiciona widgets ao layout principal
        self.layout.add_widget(titulo)
        self.layout.add_widget(self.nome_input)
        self.layout.add_widget(self.idade_input)
        self.layout.add_widget(enviar_btn)
        self.layout.add_widget(self.resultado_label)
        self.layout.add_widget(self.historico_label)

        return self.layout

    def animar_botao(self, instance):
        """Aplica animação ao botão quando pressionado."""
        anim = Animation(background_color=(0.3, 0.5, 0.7, 1), duration=0.1) + \
               Animation(background_color=(0.4, 0.6, 0.8, 1), duration=0.1)
        anim.start(instance)

    def validar_idade(self, idade_texto):
        """Valida se a idade fornecida é um número inteiro entre 0 e 120."""
        if not idade_texto.strip():
            return False, "Por favor, digite sua idade!"
        try:
            idade = int(idade_texto)
            if idade < 0:
                return False, "Idade não pode ser negativa!"
            if idade > 120:
                return False, "Digite uma idade válida (0-120)!"
            return True, idade
        except ValueError:
            return False, "Digite apenas números para a idade!"

    def verificar_idade(self, instance):
        """Verifica a faixa etária do usuário e exibe o resultado com emojis."""
        nome = self.nome_input.text.strip()
        idade_texto = self.idade_input.text.strip()

        if not nome:
            self.exibir_resultado("Digite seu nome!", "erro")
            return

        valido, resultado = self.validar_idade(idade_texto)
        if not valido:
            self.exibir_resultado(resultado, "erro")
            return

        idade = resultado

        if idade >= 60:
            mensagem = f"👴 {nome}, você é idoso."
            cor_tipo = "idoso"
        elif idade >= 18:
            mensagem = f"🧑 {nome}, você é maior de idade."
            cor_tipo = "adulto"
        else:
            mensagem = f"👦 {nome}, você é menor de idade."
            cor_tipo = "jovem"

        self.exibir_resultado(mensagem, cor_tipo)
        self.atualizar_historico(mensagem)

    def exibir_resultado(self, mensagem, tipo):
        """Exibe o resultado da verificação com cor e ícone apropriados."""
        cores = {
            "erro": (1, 0.6, 0.6, 1),
            "jovem": (1, 1, 0.8, 1),
            "adulto": (0.8, 1, 0.8, 1),
            "idoso": (1, 0.8, 0.9, 1),
        }
        self.resultado_label.text = mensagem
        self.resultado_label.color = cores.get(tipo, (1, 1, 1, 1))

    def atualizar_historico(self, mensagem):
        """Adiciona cada resultado ao histórico de verificações."""
        self.historico.append(mensagem)
        self.historico_label.text = "Histórico de verificações:\n" + "\n".join(self.historico[-5:])  # Mostra só os 5 últimos

if __name__ == '__main__':
    VerificadorIdadeApp().run()