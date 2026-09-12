# Pré-processamento de imagens para inspeção de peças fundidas

Mini-projeto de Machine Learning e Visão Computacional. O sistema prepara, em lote, imagens de peças metálicas para um futuro modelo de classificação de qualidade. Ele **não classifica defeitos**: sua função é reduzir ruído, segmentar a peça e evidenciar contornos e possíveis irregularidades.

## Objetivo e fluxo do sistema

Para cada imagem de entrada, o pipeline aplica:

1. conversão para escala de cinza;
2. filtro Gaussiano para reduzir ruído;
3. limiarização automática pelo método de Otsu;
4. abertura morfológica para remover pequenos ruídos;
5. fechamento morfológico para preencher pequenas lacunas;
6. redimensionamento da segmentação e da imagem suavizada para 256 × 256 pixels;
7. detecção de bordas com Canny na imagem suavizada já padronizada;
8. gravação da segmentação e das bordas em PNG, separadamente.

Cada entrada gera dois resultados binários: uma máscara de segmentação e um mapa de bordas. Eles não são combinados, pois bordas brancas sobre uma máscara branca seriam encobertas. A estrutura de subpastas do dataset é preservada. Arquivos com o mesmo nome-base e extensões diferentes na mesma pasta devem ser renomeados antes da execução para evitar sobrescrita.

## Estrutura do projeto

```text
.
├── raw_images/           # imagens originais (não versionadas)
├── processed_images/     # resultados gerados (não versionados)
├── src/
│   └── pipeline.py       # pipeline e interface de linha de comando
├── tests/
│   └── test_pipeline.py  # testes automatizados
├── pyproject.toml         # configuração dos testes
├── requirements.txt
└── README.md
```

## Dataset

O dataset sugerido é o [Casting Product Image Data for Quality Inspection](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product). Para este projeto, as imagens também foram disponibilizadas em um [arquivo ZIP no Google Drive](https://drive.google.com/file/d/1K5gNxQ7RXA-nb4boNzPYQTJlRvJyYBD1/view).

Baixe e extraia as imagens. Depois, copie para `raw_images/` as pastas desejadas, por exemplo:

```text
raw_images/
├── def_front/
└── ok_front/
```

As imagens não são incluídas no Git por causa do tamanho, da privacidade da execução e das condições de distribuição do dataset. O `.gitignore` exclui arquivos ZIP e todo o conteúdo de `raw_images/` e `processed_images/`, mantendo somente os arquivos `.gitkeep` que preservam a estrutura de pastas.

## Privacidade das imagens e saída do programa

O programa não abre janelas, não exibe imagens no terminal e não incorpora imagens no código ou no README. Durante a execução normal, o terminal mostra somente a quantidade de sucessos e falhas. As imagens transformadas são gravadas apenas no diretório local `processed_images/`, pois esse salvamento é um requisito da atividade.

Assim, quem receber apenas o repositório terá acesso ao código, mas não às imagens originais nem às processadas. Para compartilhar algum exemplo de resultado, faça isso separadamente e apenas de forma intencional.

## Instalação

Requer Python 3.9 ou mais recente.

### macOS ou Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Execução

Com as imagens em `raw_images/`, execute na raiz do projeto:

```bash
python -m src.pipeline
```

Os arquivos serão gravados em `processed_images/segmentation/` e `processed_images/edges/`, preservando as subpastas de entrada. O total de sucessos conta imagens de entrada com os dois resultados salvos, não o número de PNGs. Para escolher outras pastas:

```bash
python -m src.pipeline --input caminho/entrada --output caminho/saida
```

Também é possível ajustar os parâmetros:

```bash
python -m src.pipeline --width 256 --height 256 --blur-kernel 5 --morph-kernel 3 --canny-low 50 --canny-high 150
```

O kernel do filtro Gaussiano deve ser um número ímpar positivo. Os limiares do Canny devem respeitar `0 <= baixo < alto <= 255`.

## Testes

Os testes usam imagens sintéticas, portanto não exigem o dataset:

```bash
pytest -q
```

Eles verificam formato, dimensões, resultado binário, validação de parâmetros, leitura em lote e preservação das subpastas.

### Validação realizada

Foram aprovados 8 testes automatizados e reprocessadas 1.300 imagens reais do dataset, com 0 falhas de leitura, processamento ou gravação. Foram conferidos os 2.600 PNGs gerados: 1.300 de segmentação e 1.300 de bordas, todos binários e com 256 × 256 pixels, sem resultados ausentes.
Essa verificação confirma o funcionamento do pipeline, mas não substitui a avaliação visual da qualidade dos resultados.

Na revisão de duas amostras da versão anterior, a combinação por OR encobria aproximadamente metade dos pixels de Canny. A nova versão mantém as saídas separadas. A segmentação ainda tem limitações com regiões claras e iluminação variável; não se afirma que todos os defeitos são preservados ou detectados.

Nesta execução local, os resultados antigos foram preservados em `processed_images/legacy_combined/` para comparação. Essa pasta não é gerada pela versão nova e também fica fora do Git.

## Organização em sprints

O acompanhamento detalhado, incluindo as pendências da entrega, está em [PLANEJAMENTO.md](PLANEJAMENTO.md).

- **Sprint 1 — Configuração:** repositório Git, branch `development`, ambiente virtual e seleção do dataset.
- **Sprint 2 — Dados:** pastas de entrada e saída e leitura recursiva em lote.
- **Sprint 3 — Pipeline base:** escala de cinza e filtro Gaussiano.
- **Sprint 4 — Características:** Otsu e Canny.
- **Sprint 5 — Refinamento:** abertura, fechamento e padronização em 256 × 256.
- **Sprint 6 — Entrega:** gravação dos resultados, testes, documentação e apresentação.

## Estratégia de branches

- `main`: versão estável, pronta para entrega;
- `development`: integração e validação das funcionalidades durante o desenvolvimento.

Em um projeto maior, branches curtas de funcionalidade poderiam partir de `development`, como `feature/batch-processing` e `feature/image-filters`. Para este mini-projeto, uma única branch de integração mantém o histórico simples.

## Decisões técnicas e limitações

O Otsu foi escolhido por determinar automaticamente o limiar a partir do histograma. O filtro Gaussiano reduz variações antes da segmentação, e as operações morfológicas limpam a máscara. O Canny gera um mapa independente de contornos que podem representar ranhuras ou descontinuidades. Ele é aplicado na resolução final para evitar descartar linhas finas ao redimensionar um mapa binário.

Como iluminação, contraste e escala variam, os parâmetros ideais podem mudar entre lotes. A máscara de Otsu pode confundir regiões claras da peça com o fundo; ela não é uma delimitação perfeita do objeto. O mapa de bordas separado evita o encobrimento pela máscara, mas não identifica se uma borda corresponde realmente a um defeito. Melhorias futuras incluem correção de iluminação, equalização adaptativa de contraste (CLAHE), configuração por arquivo e avaliação quantitativa com um conjunto anotado.

## Autoria

Desenvolvido para fins acadêmicos. Preencha antes da entrega:

- **Aluno(a):** Francesco Cristiano Cousseau
- **Turma:** Machine Learning e Visão Computacional T2
- **Repositório:** https://github.com/francescousseau/preprocessamento-pecas-fundidas
