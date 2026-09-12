"""Pre-processamento em lote para imagens de pecas de fundicao.

Etapas: escala de cinza, suavizacao, limiarizacao de Otsu,
operacoes morfologicas, deteccao de bordas e redimensionamento.
"""

from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


EXTENSOES_SUPORTADAS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
LOGGER = logging.getLogger("casting_pipeline")


@dataclass(frozen=True)
class PipelineConfig:
    """Parametros configuraveis do pipeline."""

    width: int = 256
    height: int = 256
    blur_kernel: int = 5
    morph_kernel: int = 3
    canny_low: int = 50
    canny_high: int = 150

    def validate(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("A largura e a altura devem ser maiores que zero.")
        if self.blur_kernel <= 0 or self.blur_kernel % 2 == 0:
            raise ValueError("O kernel de suavizacao deve ser positivo e impar.")
        if self.morph_kernel <= 0:
            raise ValueError("O kernel morfologico deve ser maior que zero.")
        if not 0 <= self.canny_low < self.canny_high <= 255:
            raise ValueError("Use 0 <= canny_low < canny_high <= 255.")


def preprocess_image(image: np.ndarray, config: PipelineConfig) -> dict[str, np.ndarray]:
    """Retorna segmentacao e bordas separadas, binarias e padronizadas."""
    config.validate()
    if image is None or image.size == 0:
        raise ValueError("A imagem recebida esta vazia.")

    if image.ndim == 2:
        gray = image.copy()
    elif image.ndim == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif image.ndim == 3 and image.shape[2] == 4:
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    else:
        raise ValueError(f"Formato de imagem nao suportado: {image.shape}")

    blurred = cv2.GaussianBlur(
        gray, (config.blur_kernel, config.blur_kernel), sigmaX=0
    )
    _, thresholded = cv2.threshold(
        blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (config.morph_kernel, config.morph_kernel)
    )
    opened = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)
    refined = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    segmentation = cv2.resize(
        refined,
        (config.width, config.height),
        interpolation=cv2.INTER_NEAREST,
    )
    # Canny na resolucao final evita perder linhas finas ao reduzir uma
    # imagem de bordas ja binarizada. A mascara nao encobre essas linhas.
    interpolation = (
        cv2.INTER_AREA
        if config.width <= gray.shape[1] and config.height <= gray.shape[0]
        else cv2.INTER_LINEAR
    )
    standardized = cv2.resize(
        blurred, (config.width, config.height), interpolation=interpolation
    )
    edges = cv2.Canny(standardized, config.canny_low, config.canny_high)
    return {"segmentation": segmentation, "edges": edges}


def list_images(input_dir: Path) -> list[Path]:
    """Lista imagens suportadas em ordem deterministica."""
    return sorted(
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in EXTENSOES_SUPORTADAS
    )


def process_batch(
    input_dir: Path, output_dir: Path, config: PipelineConfig
) -> tuple[int, int]:
    """Processa todas as imagens; retorna quantidades de sucesso e falha."""
    config.validate()
    if not input_dir.exists() or not input_dir.is_dir():
        raise FileNotFoundError(f"Diretorio de entrada nao encontrado: {input_dir}")

    images = list_images(input_dir)
    if not images:
        raise FileNotFoundError(
            f"Nenhuma imagem suportada foi encontrada em: {input_dir}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    successes = 0
    failures = 0

    for image_path in images:
        image = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        if image is None:
            LOGGER.warning("Um arquivo de imagem ilegivel foi ignorado.")
            LOGGER.debug("Arquivo ilegivel: %s", image_path)
            failures += 1
            continue

        try:
            result = preprocess_image(image, config)
            relative = image_path.relative_to(input_dir).with_suffix(".png")
            for stage, output in result.items():
                destination = output_dir / stage / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                if not cv2.imwrite(str(destination), output):
                    raise OSError(f"Nao foi possivel salvar {destination}")
            # Os caminhos das imagens so aparecem com log de depuracao.
            # A execucao normal informa apenas as quantidades finais.
            LOGGER.debug("Processada: %s -> %s", image_path, destination)
            successes += 1
        except (ValueError, cv2.error, OSError) as error:
            LOGGER.warning("Uma imagem nao pode ser processada ou salva.")
            LOGGER.debug("Falha em %s: %s", image_path, error)
            failures += 1

    return successes, failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pre-processa imagens de pecas metalicas em lote."
    )
    parser.add_argument("--input", type=Path, default=Path("raw_images"))
    parser.add_argument("--output", type=Path, default=Path("processed_images"))
    parser.add_argument("--width", type=int, default=256)
    parser.add_argument("--height", type=int, default=256)
    parser.add_argument("--blur-kernel", type=int, default=5)
    parser.add_argument("--morph-kernel", type=int, default=3)
    parser.add_argument("--canny-low", type=int, default=50)
    parser.add_argument("--canny-high", type=int, default=150)
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    config = PipelineConfig(
        width=args.width,
        height=args.height,
        blur_kernel=args.blur_kernel,
        morph_kernel=args.morph_kernel,
        canny_low=args.canny_low,
        canny_high=args.canny_high,
    )
    try:
        successes, failures = process_batch(args.input, args.output, config)
    except (ValueError, FileNotFoundError) as error:
        LOGGER.error("%s", error)
        return 1

    LOGGER.info("Concluido: %d sucesso(s), %d falha(s).", successes, failures)
    return 0 if successes > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
