"""Regression tests for the flow-matching DPM++ scheduler."""

import importlib.util
from pathlib import Path

import pytest
import torch


@pytest.fixture(scope="module")
def flow_dpm_scheduler():
    """Load the scheduler without importing the heavyweight model package."""
    module_path = Path(__file__).parents[1] / "wan" / "utils" / "fm_solvers.py"
    spec = importlib.util.spec_from_file_location("wan_flow_solvers", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.FlowDPMSolverMultistepScheduler


def test_sigma_min_uses_flow_terminal_and_stays_finite(flow_dpm_scheduler):
    """The flow sigma_min endpoint must support a complete high-order rollout."""
    scheduler = flow_dpm_scheduler(
        solver_order=3,
        final_sigmas_type="sigma_min",
    )
    scheduler.set_timesteps(20)

    assert scheduler.sigmas[-1].item() == scheduler.sigma_min
    assert scheduler.sigmas[-2].item() > scheduler.sigmas[-1].item()

    sample = torch.randn(1, 2, 3)
    for timestep in scheduler.timesteps:
        sample = scheduler.step(torch.zeros_like(sample), timestep, sample).prev_sample

    assert torch.isfinite(sample).all()


def test_custom_sigma_sequence_accepts_lists(flow_dpm_scheduler):
    """Documented list inputs should follow the same shifted schedule path."""
    scheduler = flow_dpm_scheduler(shift=2.0)
    scheduler.set_timesteps(sigmas=[0.9, 0.6, 0.2])

    expected = torch.tensor(
        [2.0 * sigma / (1.0 + sigma) for sigma in (0.9, 0.6, 0.2)],
        dtype=torch.float32,
    )
    assert torch.allclose(scheduler.sigmas[:-1], expected)
    assert scheduler.sigmas[-1].item() == 0.0
    assert scheduler.num_inference_steps == 3


@pytest.mark.parametrize("algorithm_type", ["dpmsolver", "sde-dpmsolver"])
def test_noise_prediction_variants_have_zero_sigma_limit(
    flow_dpm_scheduler, algorithm_type
):
    """The zero-sigma endpoint must not create inf*zero in noise solvers."""
    scheduler = flow_dpm_scheduler(
        algorithm_type=algorithm_type,
        final_sigmas_type="sigma_min",
        solver_order=2,
    )
    scheduler.set_timesteps(20)

    sample = torch.randn(1, 2)
    generator = torch.Generator().manual_seed(7)
    for timestep in scheduler.timesteps:
        sample = scheduler.step(
            torch.zeros_like(sample),
            timestep,
            sample,
            generator=generator,
        ).prev_sample

    assert torch.isfinite(sample).all()


def test_custom_sigma_sequence_must_be_non_empty_vector(flow_dpm_scheduler):
    scheduler = flow_dpm_scheduler()

    with pytest.raises(ValueError, match="non-empty one-dimensional"):
        scheduler.set_timesteps(sigmas=[])

    with pytest.raises(ValueError, match="non-empty one-dimensional"):
        scheduler.set_timesteps(sigmas=[[0.8, 0.4]])
