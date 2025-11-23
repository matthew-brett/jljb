""" Test Python interface to CLI
"""

from pathlib import Path
import sys
from unittest.mock import patch

from jljb.make_jl_dir import main as main_cli

HERE = Path(__file__).parent


def test_main(tmp_path):
    config_file = str(HERE / 'example__config.yml')
    support_files = [str(HERE / '..' / 'src'), config_file]
    start_args = support_files + ['--config', config_file]
    # Defaults to temporary JL scratch directory.
    check_jl_cmd(tmp_path / 'out1', start_args)
    # Explicit JL scratch directory.
    jl_out = tmp_path / 'jl'
    check_jl_cmd(tmp_path / 'out2', start_args + ['--jl-tmp', str(jl_out)])
    assert (jl_out / 'eg.ipynb').is_file()


def check_jl_cmd(out_path, args):
    with patch.object(sys, 'argv', ['', str(out_path)] + args):
        main_cli()
    assert out_path.is_dir()
    assert (out_path / 'notebooks').is_dir()
    f_pth = (out_path / 'files')
    assert (f_pth / 'src').is_dir()
    assert (f_pth / 'example__config.yml').is_file()
    assert (f_pth / 'eg.ipynb').is_file()
    assert (f_pth / 'eg2.ipynb').is_file()
