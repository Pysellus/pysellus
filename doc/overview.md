# `pysellus` — Structure overview and flow of execution

## Structure

The following is an overview of the internal structure of `pysellus`.

### Parser

`parser :: Directory -> Directory`

The parser is the first module to get executed in the application.

It receives a directory where the DSL files are located, and iterates over them, parsing them, and then dumping the result to a new file located in a new `result` (or other) folder.

It returns the directory containing these expanded files.


### Loader

`loader :: Directory -> [fn]`

The loader, executed just after the `Parser`, receives the directory of the previously expanded files, and for each one of them, collects the top-level functions declared in it.

It then stores these functions in a list and returns it.


### Registrar

`registrar :: [fn] -> { stream: [fn] }`

The registrar takes a list of functions and executes them. These functions **must** _subscribe_ some functions to a stream by using `expect`.

It returns a dictionary which maps each of these streams to a list of subscriber functions.


### Threader

`threader :: { stream: [fn] } -> [Thread]`

Receives the previous dictionary, and for each stream and subscriber function in its list, does:

`Thread(target=subscribe, args=(stream,fn))`

It then returns a list collecting all the created threads.


### Launcher

`launcher :: [Thread] -> ∞`

Runs all threads in the list returned by the `Threader`.


## Flow of execution

`parser |> loader |> registrar |> threader |> launcher`

