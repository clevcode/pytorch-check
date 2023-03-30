# pytorch-check

Check PyTorch models for (overtly) unsafe code

Depends on fickling, the Python pickling decompiler and static analyzer.

By default, this checks for common patterns used to inject malicious code
into Python bytecode, but is not a 100% guarantee against any malicious
code embedded into models.

The -t flag can be used to safely trace the execution of the bytecode to
see what's actually going on, and the -d flag can be used to print the
disassembled bytecode, for manual analysis.

This script handles the TorchScript serialization format that is used for
PyTorch models (generally using the .pt or .pth extension), since that is
not handled directly by the CLI tool that comes with the fickling package.

The format is defined here:
https://github.com/pytorch/pytorch/blob/master/torch/csrc/jit/docs/serialization.md

Basically .pkl/.debug_pkl files are embedded into a Zip archive along with
data files as well as optional Python source code.

For those of you who are unaware, pkl is serialized Python bytecode, that
is executed when the model is loaded, allowing for execution of arbitrary
code. Trojanizing PyTorch model files is trivial, including by using the
fickling tool by TrailOfBits to inject code into one of the embedded .pkl
or .debug_pkl files in a model.

Install with:
```bash
python3 -m pip install --user pytorch-check
```

Or from this directory:
```bash
python3 -m pip install --user .
```

Then use the command line tool like this:
```bash
pytorch-check /path/to/file-or-directory...
```

This will scan all of the specified files, treating .pkl/.pickle as files
containing pickled Python bytecode directly, and any other files like they
are PyTorch model files (i.e. Zip archives with embedded .pkl files).

If a directory is specified, it will be scanned for files with the .ckpt,
.pt, .pth, .pkl or .pickle file extensions where the .ckpt, .pt and .pth
file extensions will be treated as PyTorch model files.

Note that the pickled code embedded into PyTorch model files in general will
have some embedded imports from the pytorch package itself. This will emit a
warning since it's technically executing code, but is generally benign. Read
the warnings to see what is actually going on.

Stay safe!
