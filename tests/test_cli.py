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
    out1 = tmp_path / 'out1'
    start_args = [str(out1)] + support_files + ['--config', config_file]
    explicit_args = start_args + ['--jl-tmp', str(tmp_path / 'jl')]
    for args in start_args, explicit_args:
        with patch.object(sys, 'argv', [''] + args):
            main_cli()
        assert out1.is_dir()
        assert (out1 / 'notebooks').is_dir()
        f_pth = (out1 / 'files')
        assert (f_pth / 'src').is_dir()
        assert (f_pth / 'example__config.yml').is_file()
        assert (f_pth / 'eg.ipynb').is_file()
        assert (f_pth / 'eg2.ipynb').is_file()
