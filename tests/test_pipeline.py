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

    assert set(result) == {"segmentation", "edges"}
    for output in result.values():
        assert output.shape == (256, 256)
        assert output.dtype == np.uint8
        assert set(np.unique(output)).issubset({0, 255})
        assert np.count_nonzero(output) > 0


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
    for stage in ("segmentation", "edges"):
        saved = cv2.imread(str(output_dir / stage / "def_front" / "sample.png"), 0)
        assert saved is not None
        assert saved.shape == (256, 256)


def test_edges_are_not_combined_with_segmentation() -> None:
    image = synthetic_part()
    config = PipelineConfig(width=240, height=180)
    result = preprocess_image(image, config)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    expected = cv2.Canny(blurred, 50, 150)

    assert np.array_equal(result["edges"], expected)
    assert not np.array_equal(result["edges"], result["segmentation"])


def test_normal_execution_does_not_log_image_names(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    private_name = "imagem_privada.jpeg"
    cv2.imwrite(str(input_dir / private_name), synthetic_part())

    process_batch(input_dir, tmp_path / "processed", PipelineConfig())

    assert private_name not in caplog.text


def test_unreadable_image_name_is_not_exposed(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    private_name = "imagem_privada_corrompida.png"
    (input_dir / private_name).touch()

    result = process_batch(input_dir, tmp_path / "processed", PipelineConfig())

    assert result == (0, 1)
    assert private_name not in caplog.text
