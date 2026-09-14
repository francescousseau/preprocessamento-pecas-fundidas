# Planejamento do mini-projeto

Atualizado em **14/09/2026**. Checklist de preparação marcado como concluído conforme indicação do aluno de que a entrega está pronta. Código e resultados técnicos foram conferidos; vídeo e permissões do Google Drive dependem da confirmação do aluno e não foram auditados nesta revisão.

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
- [x] Salvar o cinza padronizado, preservando tons intermediários.
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
- [x] Verificar tecnicamente os resultados das 1.300 imagens reais do dataset.
- [x] Revisar amostras da versão inicial e documentar as limitações de segmentação e iluminação.

## Sprint 6 — Gravação e documentação

- [x] Salvar os resultados em PNG.
- [x] Documentar instalação, execução, decisões e limitações.
- [x] Preparar roteiro de apresentação com duração máxima de 5 minutos.
- [x] Evitar exibição de imagens e versionamento do dataset.
- [x] Preencher nome e turma no README.
- [x] Integrar código e README revisado de `development` em `main` após validação real (Pull Request #7 integrado).
- [x] Publicar o repositório no GitHub.
- [x] Incluir o texto integral da licença MIT em `LICENSE`.
- [x] Preparar o vídeo de até 5 minutos, com rosto visível e boa iluminação (confirmação do aluno).
- [x] Preparar README e vídeo no Google Drive com acesso de leitor para qualquer pessoa com o link (confirmação do aluno).
- [x] Preparar os links do README e do vídeo para submissão no AVA, sem exigir o link do vídeo no README.

## Critério de conclusão

Foram aprovados **8 testes automatizados** e processadas **1.300 imagens reais**, com **0 falhas**, gerando **3.900 PNGs válidos**: 1.300 em cinza, 1.300 segmentações e 1.300 mapas de bordas. Todas as saídas foram conferidas como imagens de canal único, tipo `uint8` e tamanho 256 × 256 pixels. Segmentação e bordas são binárias; o cinza preserva tons intermediários. Nenhum mapa de bordas ficou vazio. Dez entradas foram recalculadas, sem divergências em relação aos arquivos gravados.

A revisão inicial de duas amostras revelou limitações de iluminação e encobrimento de bordas na versão combinada. A versão atual salva as três representações separadamente. A validação comprova o funcionamento técnico, não a qualidade visual de todos os resultados nem a detecção de defeitos. O sistema apenas prepara imagens para uma futura etapa de Machine Learning.

## Última ação de entrega

Publicar esta atualização do planejamento e enviar os links do README e do vídeo na tarefa **Módulo 2 — Mini-Projeto Avaliativo, Semana 07**, no AVA. O envio ainda será realizado pelo aluno; este checklist não representa um comprovante de submissão. Antes de enviar, testar os dois links em janela anônima.

Prazo informado no enunciado: **14/09/2026 às 22h**. Este acompanhamento registra o estado real do projeto; não representa um histórico de seis sprints executadas em datas diferentes.
