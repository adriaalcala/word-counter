# Words Counter

A dummy project to count words for a given list files in a public google storage bucket.

## Dockerized usage

For basic usage first build the project with

``` [bash]
    make build
```

and then execute the command

``` [bash]
    make run
```

to add some extra args you can execute

``` [bash]
    make run args="arg1 arg2 ..."
```

for example to execute with verbose and csv report options you can execute

``` [bash]
    make run args="--verbose --store_csv"
```


Then a file named report.pdf will be created with the report.

To get more help you can execute the command

``` [bash]
    make help
```

## Test

To run test just execute

``` [bash]
    make test
```

## Usage without docker

If you want (not recommended) you can use this project without docker. First you need to install the dependencies with

``` [bash]
    pip install -r requeriments.txt
```

and then you can execute the code with

``` [bash]
    python main.py
```

to get help, you can execute

``` [bash]
    python main.py --help
```