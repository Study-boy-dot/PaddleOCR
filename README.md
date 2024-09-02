# PaddleOCR Demo
Demo PaddleOCR on Unbuntu 22.04 bit 64

## Environment
|Environment|Version|
|-----------|----------|
|Architecture|x86_64|
|Ubuntu|22.04|
|python |3.10.12|
|cuda    |12.6    |
|nvidia driver|560.28.03|
|paddleocr    |2.8.1    |
|paddlepaddle-gpu|2.6.1  |

## Installation
reference: [Paddle Quickstart](https://paddlepaddle.github.io/PaddleOCR/ppocr/quick_start.html#11-paddlepaddle)
```
python3 -m venv [venv]
source [venv]/bin/activate
# using gpu
pip install paddlepaddle-gpu
# or
pip install paddlepaddle

pip install paddleocr
```

## Exception
If facing this Error when using GPU
```
RuntimeError: (PreconditionNotMet) Cannot load cudnn shared library. Cannot invoke method cudnnGetVersion.
  [Hint: cudnn_dso_handle should not be null.] (at /paddle/paddle/phi/backends/dynload/cudnn.cc:64)
Help me to fix this issue
```
Install cudnn to fix this issue. Refer to https://developer.nvidia.com/cudnn
