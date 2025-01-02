# Learn Manim

of course, this project depend on manim library and I install it with
```bash
conda install -c conda-forge manim
```

For project `1pid-controller`,
I use `control` and `slycot` library, so I install it with

```bash
conda install -c conda-forge control slycot
```

run the manim with command, `-p` means `preview` and `-ql` means `set quality as low 854x480 15FPS`

```
manim -pql scene.py SquareAndCircle
manim render -pql scene.py SquareAndCircle
```

see more options at `manim render -h`
