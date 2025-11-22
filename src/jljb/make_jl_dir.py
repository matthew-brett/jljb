""" Create JupyterLite directory
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
import shutil
from subprocess import check_call
import sys
import tempfile

from .process_notebooks import write_proc_nbs


def mk_jl_dir(out_dir, support_files=(), jl_dir=None, config='_config.yml'):
    tmp_jl_dir = jl_dir is None
    if tmp_jl_dir:
        tmp_dir = tempfile.TemporaryDirectory()
        jl_dir = Path(tmp_dir.name)
    else:
        jl_dir = Path(jl_dir)
        shutil.rmtree(jl_dir)
        jl_dir.mkdir()
    out_dir = Path(out_dir)
    for support_file in support_files:
        s_pth = Path(support_file)
        if s_pth.is_file():
            shutil.copy2(s_pth, jl_dir)
        elif s_pth.is_dir():
            shutil.copytree(s_pth, jl_dir / s_pth.name)
    write_proc_nbs(config, jl_dir)
    check_call([sys.executable, '-m',
                'jupyter', 'lite', 'build'
                f'--contents {jl_dir}',
                f'--output-dir {out_dir}',
                f'--lite-dir {jl_dir}'])
    if tmp_jl_dir:
        tmp_dir.cleanup()


def get_parser():
    parser = ArgumentParser(description=__doc__,  # Usage from docstring
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('out_dir',
                        help='Output directory for JL distribution')
    parser.add_argument('support_files', nargs='*',
                        help='Supporting files / dirs to copy into `out_dir`')
    parser.add_argument('--jl-tmp',
                        help='Temporary directory for JL intermediate files')
    parser.add_argument(
        "--config", default="_config.yml",
        help="Jupyter Book YaML configuration file"
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    mk_jl_dir(args.out_dir, args.support_files,
              jl_dir=args.jl_tmp,
              config=args.config)


if __name__ == '__main__':
    main()
