from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from kivy.animation import Animation

class VerificadorIdadeApp(App):
    resultado_texto = StringProperty('')
    resultado_cor = StringProperty('cinza_claro')
    
    def build(self):
        # Configurar cor de fundo da janela - Azul escuro elegante
        Window.clearcolor = (0.1, 0.15, 0.25, 1)  # Azul escuro
        
        # Layout principal com alinhamento centralizado
        layout = BoxLayout(
            orientation='vertical', 
            padding=30,  # Reduzido de 40 para 30
            spacing=20,   # Reduzido de 25 para 20
            size_hint=(0.8, 0.8),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Título centralizado com cor harmoniosa
        titulo = Label(
            font_size='26sp',  # Reduzido de 28sp para 26sp
            bold=True,
            color=(0.9, 0.9, 0.95, 1),  # Branco azulado
            size_hint_y=None,
            height=50,  # Reduzido de 60 para 50
            halign='center'
        )
        titulo.bind(texture_size=titulo.setter('size'))
        
        # Container para campos de entrada
        campos_layout = BoxLayout(orientation='vertical', spacing=12)  # Reduzido de 15 para 12
        
        # Campo para nome
        label_nome = Label(
            text='Nome:', 
            font_size='15sp',  # Reduzido de 16sp para 15sp
            color=(0.8, 0.85, 0.9, 1),  # Azul claro
            size_hint_y=None,
            height=25,  # Reduzido de 30 para 25
            halign='left'
        )
        
        self.nome_input = TextInput(
            hint_text='Digite seu nome',
            hint_text_color=(0.6, 0.6, 0.65, 1),
            size_hint_y=None,
            height=45,  # Reduzido de 55 para 45
            font_size='16sp',  # Reduzido de 17sp para 16sp
            background_color=(0.2, 0.25, 0.3, 1),
            foreground_color=(0.95, 0.95, 1, 1),
            cursor_color=(0.8, 0.8, 1, 1),
            padding=[12, 8],  # Reduzido de [15, 10] para [12, 8]
            multiline=False
        )
        
        # Campo para idade
        label_idade = Label(
            text='Idade:', 
            font_size='15sp',  # Reduzido de 16sp para 15sp
            color=(0.8, 0.85, 0.9, 1),
            size_hint_y=None,
            height=25,  # Reduzido de 30 para 25
            halign='left'
        )
        
        self.idade_input = TextInput(
            hint_text='Digite sua idade (0-120)',
            hint_text_color=(0.6, 0.6, 0.65, 1),
            size_hint_y=None,
            height=45,  # Reduzido de 55 para 45
            font_size='16sp',  # Reduzido de 17sp para 16sp
            input_filter='int',
            background_color=(0.2, 0.25, 0.3, 1),
            foreground_color=(0.95, 0.95, 1, 1),
            cursor_color=(0.8, 0.8, 1, 1),
            padding=[12, 8],  # Reduzido de [15, 10] para [12, 8]
            multiline=False
        )
        
        # Botão de enviar com tamanho reduzido
        enviar_btn = Button(
            text='VERIFICAR IDADE',
            size_hint_y=None,
            height=50,  # Reduzido de 65 para 50 (diminuição significativa)
            font_size='16sp',  # Reduzido de 18sp para 16sp
            background_color=(0.4, 0.6, 0.8, 1),  # Azul médio
            background_normal='',
            color=(1, 1, 1, 1),  # Corrigido: (3, 5, 2, 1) para (1, 1, 1, 1)
            bold=True,
            padding=[15, 5]  # Reduzido de [20, 10] para [15, 5]
        )
        enviar_btn.bind(on_press=self.animar_botao)
        enviar_btn.bind(on_release=self.verificar_idade)
        
        # Label para resultado com ícone
        self.resultado_label = Label(
            text='',
            font_size='17sp',  # Reduzido de 19sp para 17sp
            color=(0.9, 0.9, 0.95, 1),
            size_hint_y=None,
            height=100,  # Reduzido de 120 para 100
            halign='center',
            valign='middle',
            text_size=(None, None),
            markup=True
        )
        
        # Adicionar widgets aos layouts
        campos_layout.add_widget(label_nome)
        campos_layout.add_widget(self.nome_input)
        campos_layout.add_widget(label_idade)
        campos_layout.add_widget(self.idade_input)
        
        layout.add_widget(titulo)
        layout.add_widget(campos_layout)
        layout.add_widget(enviar_btn)
        layout.add_widget(self.resultado_label)
        
        return layout
    
    def animar_botao(self, instance):
        """Animação de clique no botão"""
        anim = Animation(background_color=(0.3, 0.5, 0.7, 1), duration=0.1) + \
               Animation(background_color=(0.4, 0.6, 0.8, 1), duration=0.1)
        anim.start(instance)
    
    def validar_idade(self, idade_texto):
        """Validação centralizada da idade"""
        if not idade_texto.strip():
            return False, "Por favor, digite sua idade!"
        
        try:
            idade = int(idade_texto)
            if idade < 0:
                return False, "Idade não pode ser negativa!"
            if idade > 120:
                return False, "digite uma idade válida (0-120)!"
            return True, idade
        except ValueError:
            return False, "Digite apenas números para a idade!"
    
    def verificar_idade(self, instance):
        # Obter valores dos campos
        nome = self.nome_input.text.strip()
        idade_texto = self.idade_input.text.strip()
        
        # Validar campos obrigatórios
        if not nome:
            self.exibir_resultado(" digite seu nome!", "erro")
            return
        
        # Validar idade
        valido, resultado = self.validar_idade(idade_texto)
        if not valido:
            self.exibir_resultado(resultado, "erro")
            return
        
        idade = resultado
        
        # Determinar a mensagem baseada na idade
        if idade >= 60:
            mensagem = f" {nome}! Você é idoso ."
            cor_tipo = "idoso"
        elif idade >= 18:
            mensagem = f"{nome}! Você é maior de idade."
            cor_tipo = "adulto"
        else:
            mensagem = f" {nome}! Você é menor de idade."
            cor_tipo = "jovem"
        
        self.exibir_resultado(mensagem, cor_tipo)
    
    def exibir_resultado(self, mensagem, tipo):
        """Exibe resultado com cores e formatação apropriadas"""
        cores = {
            "erro": (1, 0.6, 0.6, 1),      # Vermelho claro
            "jovem": (1, 1, 0.8, 1),       # Amarelo claro
            "adulto": (0.8, 1, 0.8, 1),    # Verde claro
            "idoso": (1, 0.8, 0.9, 1),     # Rosa claro
            "cinza_claro": (0.9, 0.9, 0.95, 1)
        }
        
        self.resultado_label.text = mensagem
        self.resultado_label.color = cores.get(tipo, cores["cinza_claro"])

if __name__ == '__main__':
    VerificadorIdadeApp().run()