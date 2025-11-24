""" Create JupyterLite directory
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
import shutil
from subprocess import check_call
import sys
import tempfile

from .process_notebooks import write_proc_nbs, load_config


def mk_jl_dir(out_dir,
              config,
              support_files=(),
              jl_dir=None):
    tmp_jl_dir = jl_dir is None
    if tmp_jl_dir:
        tmp_dir = tempfile.TemporaryDirectory()
        jl_dir = Path(tmp_dir.name)
    else:
        jl_dir = Path(jl_dir)
        if jl_dir.is_dir():
            shutil.rmtree(jl_dir)
        jl_dir.mkdir()
    out_dir = Path(out_dir)
    for support_file in support_files:
        s_pth = Path(support_file)
        if s_pth.is_file():
            shutil.copy2(s_pth, jl_dir)
        elif s_pth.is_dir():
            shutil.copytree(s_pth, jl_dir / s_pth.resolve().name)
    write_proc_nbs(config, jl_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, '-m',
           'jupyter', 'lite', 'build',
           '--contents', str(jl_dir),
           '--output-dir', str(out_dir),
           '--lite-dir', str(jl_dir)]
    check_call(cmd)
    if tmp_jl_dir:
        tmp_dir.cleanup()


def get_parser():
    parser = ArgumentParser(description=__doc__,  # Usage from docstring
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('output_dir',
                        help='Output directory for JL distribution')
    parser.add_argument('support_files', nargs='*',
                        help='Supporting files / dirs to copy into `out_dir`')
    parser.add_argument('--jl-tmp',
                        help='Temporary directory for JL intermediate files')
    parser.add_argument(
        "--config", default="_config.yml",
        help="Jupyter Book YaML configuration file"
    )
    parser.add_argument(
        '--input-dir',
        help=("Input directory containing notebooks "
              "(default is directory of _config.yml file)"))
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    config = load_config(Path(args.config))
    if args.input_dir:
        config['input_dir'] = Path(args.input_dir)
    mk_jl_dir(args.output_dir, config, args.support_files, jl_dir=args.jl_tmp)


if __name__ == '__main__':
    main()
