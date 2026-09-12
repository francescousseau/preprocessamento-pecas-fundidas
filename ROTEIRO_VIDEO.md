# Roteiro sugerido para o vídeo (até 5 minutos)

## 0:00–0:30 — Apresentação e objetivo

“Olá, meu nome é **[nome]**. Este projeto prepara imagens de peças metálicas fundidas para uso futuro em um modelo de Machine Learning. O sistema não classifica defeitos; ele aplica pré-processamento para padronizar as imagens e evidenciar contornos e possíveis irregularidades.”

## 0:30–1:30 — Demonstração

Mostre a estrutura das pastas, sem abrir ou exibir as imagens. No terminal, execute:

```bash
python -m src.pipeline
```

Mostre a mensagem com a quantidade de imagens processadas. Explique que os arquivos são salvos localmente em `processed_images/`, têm 256 × 256 pixels e preservam as subpastas do dataset. Para demonstrar a padronização sem exibir imagens, execute os testes e explique a verificação de dimensões e formato binário.

## 1:30–2:20 — Como executar

“Para executar, é necessário ter Python instalado, criar e ativar um ambiente virtual, instalar as dependências do arquivo `requirements.txt`, baixar o dataset e colocar as imagens na pasta `raw_images`. Depois, basta executar o módulo do pipeline. Também é possível informar outras pastas e ajustar os parâmetros de suavização, morfologia e Canny.”

Mostre rapidamente as seções “Instalação” e “Execução” do README.

## 2:20–3:15 — Organização das tarefas

“Organizei o trabalho em seis sprints: primeiro configurei o projeto; depois criei a leitura em lote; implementei escala de cinza e redução de ruído; adicionei Otsu e Canny; refinei com morfologia e redimensionamento; e finalizei com gravação, testes e documentação.”

Mostre a seção de sprints do README e, brevemente, o código nas funções `preprocess_image` e `process_batch`.

## 3:15–3:50 — Branches

“Usei a branch `main` para a versão estável e a branch `development` para integrar e validar o desenvolvimento. Em uma equipe maior, eu poderia criar branches de funcionalidade, mas para o tamanho deste projeto duas branches deixam o fluxo simples e compreensível.”

Mostre as branches do repositório no GitHub ou no terminal.

## 3:50–4:40 — Melhorias possíveis

“Uma melhoria seria corrigir diferenças de iluminação e usar CLAHE para contraste local. Também seria útil salvar etapas intermediárias, carregar parâmetros de um arquivo e comparar os resultados com anotações reais. No futuro, as imagens processadas poderão alimentar uma rede neural convolucional, mas essa classificação está fora do escopo atual.”

## 4:40–5:00 — Encerramento

“Os testes automatizados validam o tamanho, o formato binário e o processamento em lote. O código, as instruções e o link deste vídeo estão documentados no README. Obrigado.”

Antes de gravar, substitua os campos de identificação, use uma imagem real do dataset e confirme que seu rosto aparece com boa iluminação.
