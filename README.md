# pytorch-check
Check PyTorch models for unsafe code

Depends on the Python pickling decompiler and static analyzer by TrailOfBits

Install that first with:
python3 -m pip install --user fickling

This script handles the TorchScript serialization format that is generally
used for PyTorch models (generally using the .pt or .pth extension), since
that is not handled directly by the fickling command line tool that comes
with the fickling pip module.

The format is defined here:
https://github.com/pytorch/pytorch/blob/master/torch/csrc/jit/docs/serialization.md

Basically .pkl/.debug_pkl files are embedded into a Zip archive along with
data files as well as optional Python source code.

For those of you who are unaware, pkl is serialized Python bytecode, that
is executed when the model is loaded, allowing for execution of arbitrary
code. Trojanizing PyTorch model files is trivial, including by using the
fickling tool by TrailOfBits to inject code into one of the embedded .pkl
or .debug_pkl files in a model.

Stay safe!
