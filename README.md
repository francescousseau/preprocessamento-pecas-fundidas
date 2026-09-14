# Pré-processamento de imagens para inspeção de peças fundidas

[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.11-green)](https://opencv.org)
[![Licença](https://img.shields.io/badge/licença-MIT-green)](LICENSE)

Mini-projeto de Machine Learning e Visão Computacional. O sistema prepara, em lote, imagens de peças metálicas fundidas para um futuro modelo de classificação de qualidade. Ele **não classifica defeitos**: reduz ruído, segmenta a peça e evidencia contornos e possíveis irregularidades, entregando dados padronizados para a etapa de modelagem.

## Objetivo e fluxo do sistema

Para cada imagem de entrada, o pipeline aplica:

1. leitura em escala de cinza (8 bits, canal único);
2. redimensionamento para 256 × 256 pixels;
3. filtro Gaussiano para reduzir ruído;
4. limiarização automática pelo método de Otsu;
5. abertura morfológica para remover pequenos ruídos;
6. fechamento morfológico para preencher pequenas lacunas;
7. detecção de bordas com Canny sobre a imagem suavizada;
8. gravação das três saídas em PNG, separadamente.

Cada entrada gera **três** resultados de 256 × 256 pixels:

| Saída | Conteúdo | Uso previsto |
|---|---|---|
| `grayscale/` | imagem em tons de cinza, padronizada, sem suavização na saída | candidata a entrada de treino, preservando tons intermediários |
| `segmentation/` | máscara binária de intensidade (Otsu + morfologia) | análise auxiliar de regiões e forma; não garante separar peça e fundo |
| `edges/` | mapa binário de bordas (Canny) | inspeção de contornos e ranhuras, auditoria visual |

A estrutura de subpastas do dataset é preservada na saída, mantendo a informação de classe de cada imagem.

## Estrutura do projeto

```text
.
├── raw_images/           # imagens originais (não versionadas)
├── processed_images/     # resultados gerados (não versionados)
├── src/
│   └── pipeline.py       # pipeline e interface de linha de comando
├── tests/
│   └── test_pipeline.py  # testes automatizados
├── pyproject.toml        # configuração dos testes
├── requirements.txt
├── PLANEJAMENTO.md       # sprints e acompanhamento
├── license              # texto integral da licença MIT
└── README.md
```

## Dataset

Dabhi, R. (2020). *Casting Product Image Data for Quality Inspection*. [Kaggle](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product). Licenciado sob [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).

Segundo a descrição do dataset no Kaggle, são imagens da vista superior de rotores de bomba submersível, capturadas sob iluminação controlada. Foi utilizada a variante `casting_512x512`, com 1.300 imagens **sem augmentation** (781 `def_front` e 519 `ok_front`), e não o conjunto de 300 × 300 pixels, que já contém aumento de dados. Na futura modelagem, a separação por imagem original deve ocorrer antes de gerar variações para treino, evitando que imagens relacionadas apareçam em treino e teste. Este pipeline não realiza essa separação nem aumento de dados.

Para este projeto, as imagens também foram disponibilizadas em um [arquivo ZIP no Google Drive](https://drive.google.com/file/d/1K5gNxQ7RXA-nb4boNzPYQTJlRvJyYBD1/view).

Baixe, extraia e organize as pastas em `raw_images/`:

```text
raw_images/
└── casting_512x512/
    ├── def_front/    # 781 imagens
    └── ok_front/     # 519 imagens
```

Nenhuma imagem, original ou processada, é versionada neste repositório — por causa do tamanho, das condições de distribuição do dataset e da privacidade da execução local. O `.gitignore` exclui arquivos ZIP e todo o conteúdo de `raw_images/` e `processed_images/`, mantendo apenas os arquivos `.gitkeep` que preservam a estrutura de pastas.

## Instalação

Requer Python 3.9 ou mais recente.

**macOS ou Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Windows (PowerShell)**

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

No macOS ou Linux, também é possível executar sem ativar o ambiente virtual:

```bash
.venv/bin/python -m src.pipeline
```

Os resultados são gravados em `processed_images/grayscale/`, `processed_images/segmentation/` e `processed_images/edges/`, preservando as subpastas de entrada. O total de sucessos informado ao final conta imagens de entrada com os três resultados salvos, não o número de arquivos gerados.

Para escolher outras pastas:

```bash
python -m src.pipeline --input caminho/entrada --output caminho/saida
```

Para ajustar os parâmetros:

```bash
python -m src.pipeline --width 256 --height 256 --blur-kernel 5 \
                       --morph-kernel 3 --canny-low 50 --canny-high 150
```

O kernel do filtro Gaussiano deve ser ímpar e positivo, e os limiares do Canny devem respeitar `0 <= baixo < alto <= 255`. Arquivos com o mesmo nome-base e extensões diferentes na mesma pasta devem ser renomeados antes da execução, sob risco de sobrescrita.

## Testes e validação

Os testes usam imagens sintéticas e não exigem o dataset:

```bash
pytest -q
```

São 8 testes, cobrindo dimensão e formato das três saídas, preservação de tons intermediários no cinza, validação dos parâmetros, leitura em lote, replicação das subpastas e rastreabilidade de falhas.

### Execução sobre o dataset

Na validação técnica de **14/09/2026**, os **8 testes foram aprovados** e foram processadas **1.300 imagens**, com **0 falhas de leitura, processamento ou gravação**, gerando **3.900 arquivos PNG**:

- 1.300 imagens em `grayscale/`;
- 1.300 máscaras em `segmentation/`;
- 1.300 mapas de bordas em `edges/`.

A conferência verificou todas as saídas: 256 × 256 pixels, canal único, tipo `uint8` e nenhum arquivo ausente ou inválido. Segmentações e bordas são binárias; todas as imagens em cinza preservam tons intermediários. Nenhum mapa de bordas está vazio. Foram recalculadas 10 entradas, cujas três saídas coincidiram exatamente com os PNGs gravados.

O lote foi executado em uma pasta temporária, sem sobrescrever resultados existentes e sem exibir imagens. A conferência do Git confirmou apenas os arquivos `.gitkeep` nas pastas de dados versionadas.

Essa verificação atesta o funcionamento do pipeline, não a qualidade visual dos resultados, avaliada separadamente por amostragem.

## Decisões técnicas

**Padronização antes dos filtros.** O redimensionamento ocorre logo após a leitura, e não ao final. Assim, os filtros operam sempre nas dimensões configuradas e não é necessário reamostrar as máscaras e bordas binárias ao final. Isso não garante resultados idênticos entre câmeras, escalas ou enquadramentos diferentes.

**Leitura restrita a 8 bits em canal único.** O lote usa `cv2.IMREAD_GRAYSCALE` para fornecer um formato consistente e compatível com os filtros e o Canny. Isso converte entradas de maior profundidade para 8 bits, sem preservar toda sua faixa original. Consulte a [documentação de limiarização](https://docs.opencv.org/4.11.0/d7/d1b/group__imgproc__misc.html) e a [documentação do Canny](https://docs.opencv.org/4.11.0/dd/d1a/group__imgproc__feature.html).

**Saídas separadas, não combinadas.** A operação OR deixa bordas brancas indistinguíveis onde a máscara já é branca. Na revisão de duas amostras da primeira versão, aproximadamente metade dos pixels de Canny ficava encoberta dessa forma. A separação elimina essa sobreposição, mas não comprova que todos os defeitos sejam preservados.

**O cinza padronizado é candidato a entrada de treino.** Ele não é binarizado e preserva tons intermediários, embora o redimensionamento possa remover detalhes pequenos. Essa saída é salva antes do Gaussian Blur. Segmentação e bordas são representações auxiliares; sua utilidade para um modelo deverá ser avaliada na etapa de modelagem.

**Otsu e Gaussiano.** O Otsu calcula automaticamente um limiar global a partir do histograma, mas não corrige iluminação desigual. O filtro Gaussiano reduz variações locais; abertura e fechamento refinam a máscara, podendo também remover pequenos detalhes.

## Limitações e próximos passos

A máscara de Otsu pode confundir regiões claras da peça com o fundo e não é uma delimitação perfeita do objeto. O mapa de bordas não distingue uma ranhura de um defeito real. Os parâmetros são valores padrão utilizados na validação, não uma calibração ótima demonstrada. Outra câmera ou iluminação pode exigir ajustes. As classes representam aproximadamente 60% `def_front` e 40% `ok_front`; na futura modelagem, precisão, revocação e matriz de confusão devem complementar a acurácia. Os custos de falsos positivos e negativos deverão ser definidos com a aplicação industrial.

Como evolução: correção de iluminação, equalização adaptativa de contraste (CLAHE), configuração por arquivo e avaliação quantitativa contra um conjunto anotado.

## Organização em sprints

Acompanhamento detalhado, incluindo pendências, em [PLANEJAMENTO.md](PLANEJAMENTO.md).

| Sprint | Entrega |
|---|---|
| 1 — Configuração | repositório Git, branch `development`, ambiente virtual e seleção do dataset |
| 2 — Dados | pastas de entrada e saída, leitura recursiva em lote |
| 3 — Pipeline base | escala de cinza e filtro Gaussiano |
| 4 — Características | limiarização de Otsu e detecção de bordas com Canny |
| 5 — Refinamento | abertura, fechamento e padronização em 256 × 256 |
| 6 — Entrega | gravação dos resultados, testes, documentação e apresentação |

## Estratégia de branches

- `main` — versão estável, pronta para entrega;
- `development` — integração e validação das funcionalidades durante o desenvolvimento.

Cada conjunto de alterações foi integrado por pull request de `development` para `main`, o que mantém o histórico legível e permite revisar o que entrou em cada etapa. Em um projeto de equipe, branches curtas de funcionalidade partiriam de `development` — como `feature/batch-processing` ou `feature/image-filters` — e seriam removidas após o merge.

## Privacidade da execução

O programa não abre janelas, não exibe imagens no terminal e não incorpora imagens ao código ou à documentação. As imagens transformadas ficam apenas no diretório local `processed_images/`, já que esse salvamento é requisito da atividade. Falhas são registradas **com o nome do arquivo**, porque um aviso anônimo em um lote de mais de mil imagens impediria localizar o arquivo problemático. Quem receber apenas o repositório terá o código, nunca as imagens.

## Licença

O código deste projeto está sob a licença [MIT](LICENSE). O arquivo contém o texto integral da licença e o aviso de copyright de 2026 de Francesco Cristiano Cousseau. Texto de referência: [Open Source Initiative](https://opensource.org/license/mit).

As imagens têm licença própria, indicada pelo autor no [Kaggle](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product) como CC BY-NC-ND 4.0. Uma licença do código não altera os termos dos dados. Nenhuma imagem original ou processada é incluída no repositório.

---

Francesco Cristiano Cousseau · Machine Learning e Visão Computacional (T2) · 2026
