from pathlib import Path

import cv2
import numpy as np
import pytest

from src.pipeline import PipelineConfig, list_images, preprocess_image, process_batch


def synthetic_part() -> np.ndarray:
    image = np.zeros((180, 240, 3), dtype=np.uint8)
    cv2.rectangle(image, (30, 25), (210, 155), (190, 190, 190), -1)
    cv2.circle(image, (120, 90), 28, (35, 35, 35), -1)
    cv2.line(image, (70, 55), (165, 125), (20, 20, 20), 4)
    return image


def test_preprocess_standardizes_all_outputs() -> None:
    result = preprocess_image(synthetic_part(), PipelineConfig())

    assert set(result) == {"grayscale", "segmentation", "edges"}
    for output in result.values():
        assert output.shape == (256, 256)
        assert output.dtype == np.uint8
        assert np.count_nonzero(output) > 0

    for nome in ("segmentation", "edges"):
        assert set(np.unique(result[nome])).issubset({0, 255})


def test_grayscale_preserva_tons_intermediarios() -> None:
    """A saida de treino nao pode ser binaria: textura e o sinal util."""
    gray = preprocess_image(synthetic_part(), PipelineConfig())["grayscale"]

    assert not set(np.unique(gray)).issubset({0, 255})


def test_accepts_grayscale_image() -> None:
    gray = cv2.cvtColor(synthetic_part(), cv2.COLOR_BGR2GRAY)
    result = preprocess_image(gray, PipelineConfig(width=128, height=96))

    assert all(output.shape == (96, 128) for output in result.values())


def test_rejects_even_blur_kernel() -> None:
    with pytest.raises(ValueError, match="impar"):
        preprocess_image(synthetic_part(), PipelineConfig(blur_kernel=4))


def test_lists_only_supported_images(tmp_path: Path) -> None:
    (tmp_path / "b.JPG").touch()
    (tmp_path / "a.png").touch()
    (tmp_path / "notes.txt").touch()

    assert [path.name for path in list_images(tmp_path)] == ["a.png", "b.JPG"]


def test_processes_batch_and_preserves_subfolders(tmp_path: Path) -> None:
    input_dir = tmp_path / "raw"
    output_dir = tmp_path / "processed"
    category = input_dir / "def_front"
    category.mkdir(parents=True)
    cv2.imwrite(str(category / "sample.jpeg"), synthetic_part())

    successes, failures = process_batch(input_dir, output_dir, PipelineConfig())

    assert (successes, failures) == (1, 0)
    for stage in ("grayscale", "segmentation", "edges"):
        saved = cv2.imread(str(output_dir / stage / "def_front" / "sample.png"), 0)
        assert saved is not None
        assert saved.shape == (256, 256)


def test_edges_are_not_combined_with_segmentation() -> None:
    result = preprocess_image(synthetic_part(), PipelineConfig())

    assert np.count_nonzero(result["edges"]) > 0
    assert not np.array_equal(result["edges"], result["segmentation"])
    # bordas sao finas; a mascara cobre a area da peca
    assert np.count_nonzero(result["edges"]) < np.count_nonzero(result["segmentation"])


def test_unreadable_image_is_counted_and_identified(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Uma falha em lote precisa dizer QUAL arquivo falhou, para ser auditavel."""
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    corrompida = "arquivo_corrompido.png"
    (input_dir / corrompida).touch()
    cv2.imwrite(str(input_dir / "valida.jpeg"), synthetic_part())

    result = process_batch(input_dir, tmp_path / "processed", PipelineConfig())

    assert result == (1, 1)
    assert corrompida in caplog.text