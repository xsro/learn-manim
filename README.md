# Learn Manim

## installation

### via uv

I use [uv](https://github.com/uv-cli/uv) to install manim and its dependencies.

```bash
brew install  cmake cairo pkg-config  # for macos users to install pycairo
uv sync
```

### via conda

of course, this project depend on manim library and I install it with
```bash
conda install -c conda-forge manim
```

For project `1pid-controller`,
I use `control` and `slycot` library, so I install it with

```bash
conda install -c conda-forge control slycot
```

## render

run the manim with command, `-p` means `preview` and `-ql` means `set quality as low 854x480 15FPS`

```
manim -pql scene.py SquareAndCircle
manim render -pql scene.py SquareAndCircle
```

see more options at `manim render -h`
