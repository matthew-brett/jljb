""" Test Python interface to CLI
"""

from pathlib import Path
import sys
from unittest.mock import patch

from jljb.make_jl_dir import main as main_cli

HERE = Path(__file__).parent.resolve()


def test_main(tmp_path):
    config_file = HERE / 'example__config.yml'
    support_files = [str(HERE / '..' / 'src'), str(config_file)]
    start_args = support_files + ['--config', str(config_file)]
    # Defaults to temporary JL scratch directory.
    check_jl_cmd(tmp_path / 'out1', start_args)
    # Explicit JL scratch directory.
    jl_out = tmp_path / 'jl'
    check_jl_cmd(tmp_path / 'out2', start_args + ['--jl-tmp', str(jl_out)])
    assert (jl_out / 'eg.ipynb').is_file()
    # Displace config.
    config_pth = tmp_path / 'a_project'
    config_pth.mkdir()
    displaced_config = config_pth / 'displaced_config.yml'
    displaced_config.write_text(config_file.read_text())
    displaced_out = tmp_path / 'out3'
    _cli_write(displaced_out, ['--config', str(displaced_config)])
    f_pth = (displaced_out / 'files')
    # No notebooks when input_dir not specified.
    assert not (f_pth / 'eg.ipynb').is_file()
    assert not (f_pth / 'eg2.ipynb').is_file()
    # Specify input dir - notebooks found.
    displaced_input_out = tmp_path / 'out4'
    _cli_write(displaced_input_out,
               ['--config', str(displaced_config),
                '--input-dir', str(HERE)])
    f_pth = (displaced_input_out / 'files')
    # Notebooks when input_dir specified.
    assert (f_pth / 'eg.ipynb').is_file()
    assert (f_pth / 'eg2.ipynb').is_file()


def _cli_write(out_path, args):
    with patch.object(sys, 'argv', ['', str(out_path)] + args):
        main_cli()
    assert out_path.is_dir()


def _check_support_files(out_path):
    f_pth = (out_path / 'files')
    assert (f_pth / 'src').is_dir()
    assert (f_pth / 'example__config.yml').is_file()


def _check_notebooks(out_path):
    assert (out_path / 'notebooks').is_dir()
    f_pth = (out_path / 'files')
    assert (f_pth / 'eg.ipynb').is_file()
    assert (f_pth / 'eg2.ipynb').is_file()


def check_jl_cmd(out_path, args):
    _cli_write(out_path, args)
    _check_support_files(out_path)
    _check_notebooks(out_path)
