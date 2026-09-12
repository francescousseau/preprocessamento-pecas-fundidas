# Planejamento do mini-projeto

## Sprint 1 — Configuração e versionamento

- [x] Inicializar o repositório Git.
- [x] Criar as branches `main` e `development`.
- [x] Criar o ambiente virtual e instalar as dependências.
- [x] Identificar o dataset e o arquivo ZIP fornecido no Google Drive.
- [x] Baixar e extrair o dataset em `raw_images/`.

## Sprint 2 — Estruturação dos dados e leitura

- [x] Criar `raw_images/` e `processed_images/`.
- [x] Implementar leitura recursiva em lote.
- [x] Aceitar extensões comuns de imagens e ignorar outros arquivos.
- [x] Preservar as subpastas na saída.

## Sprint 3 — Pré-processamento base

- [x] Converter as imagens para escala de cinza.
- [x] Aplicar Gaussian Blur para reduzir ruído.

## Sprint 4 — Segmentação e características

- [x] Aplicar limiarização automática de Otsu.
- [x] Detectar bordas com Canny.
- [x] Salvar segmentação e bordas separadamente para não encobrir contornos.

## Sprint 5 — Morfologia e padronização

- [x] Aplicar abertura (erosão seguida de dilatação).
- [x] Aplicar fechamento (dilatação seguida de erosão).
- [x] Redimensionar os resultados para 256 × 256 pixels.
- [x] Validar dimensões e parâmetros com testes sintéticos.
- [ ] Verificar os resultados em imagens reais do dataset.

## Sprint 6 — Gravação e documentação

- [x] Salvar os resultados em PNG.
- [x] Documentar instalação, execução, decisões e limitações.
- [x] Preparar roteiro de apresentação com duração máxima de 5 minutos.
- [x] Evitar exibição de imagens e versionamento do dataset.
- [ ] Preencher nome e turma no README.
- [ ] Integrar a versão final de `development` em `main` após validação real.
- [ ] Publicar o repositório no GitHub.
- [ ] Gravar o vídeo com rosto visível e boa iluminação.
- [ ] Colocar README e vídeo no Google Drive com acesso de leitor para qualquer pessoa com o link.
- [ ] Preencher os links no README e submetê-los no AVA.

## Critério de conclusão

O lote real foi reprocessado após separar segmentação e bordas: 1.300 entradas, 2.600 PNGs válidos, 0 falhas e 8 testes aprovados. A revisão inicial de duas amostras revelou limitações de iluminação e encobrimento de bordas na versão combinada. A nova versão elimina essa combinação, mas ainda exige avaliação visual mais ampla; não é necessário nem permitido afirmar que o sistema classifica defeitos: ele apenas prepara imagens.

A entrega também depende da integração das últimas alterações no GitHub, da documentação final e da gravação.

Prazo informado no enunciado: **14/09/2026 às 22h**. Este acompanhamento registra o estado real do projeto; não representa um histórico de seis sprints executadas em datas diferentes.
