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


def test_preprocess_standardizes_and_binarizes() -> None:
    result = preprocess_image(synthetic_part(), PipelineConfig())

    assert result.shape == (256, 256)
    assert result.dtype == np.uint8
    assert set(np.unique(result)).issubset({0, 255})
    assert np.count_nonzero(result) > 0


def test_accepts_grayscale_image() -> None:
    gray = cv2.cvtColor(synthetic_part(), cv2.COLOR_BGR2GRAY)
    result = preprocess_image(gray, PipelineConfig(width=128, height=96))

    assert result.shape == (96, 128)


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

    saved = cv2.imread(str(output_dir / "def_front" / "sample.png"), 0)
    assert (successes, failures) == (1, 0)
    assert saved is not None
    assert saved.shape == (256, 256)


def test_normal_execution_does_not_log_image_names(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    private_name = "imagem_privada.jpeg"
    cv2.imwrite(str(input_dir / private_name), synthetic_part())

    process_batch(input_dir, tmp_path / "processed", PipelineConfig())

    assert private_name not in caplog.text
