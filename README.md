## Motivation

This project implements an lldb command called skipstep that performs a "step
in" operation but skips over any code from files that are not contained
recursively inside any whitelisted directory. So for example, if all your
non-third-party code is in the `src` directory at the root of your project, you
can whitelist that directory, and skipstep will only stop at files that belong
to your project.

## Installation

* Put the following command in `~/.lldbinit` or equivalent:
  ```
  settings set target.load-cwd-lldbinit true
  ```

* Then place `skipstep.py` in your project, and edit the whitelist variable in
  that file to contain a path or paths that you wish to whitelist (relative to
  the location of this file).

* Create a file named .lldbinit in the root of your project and add the
  following command:
  ```
  command script import ./path/to/skipstep.py
  ```

* Now you can invoke lldb from the root of your project, and the skipstep and sk
  commands should be available.

## Usage

* Run `skipstep` or `sk` to do a whitelisted "step in" operation

## Wishlist

* I'd prefer a way to set up the whitelist in `.lldbinit`. I've thought about
  either using the lldb settings or a separate command, but it doesn't seem
  like there's a way to access the settings from python, and sharing state
  between commands doesn't seem workable.
* I might want to add a blacklist and an explicitly allowed list for
  exceptions.

## Halp!

This is my first time playing with the lldb python API. Please let me know if
there are obvious mistakes or omissions. Thanks!
