# Scripts Directory

## FOR IZABELLE

The instructions below are good general purpose guidelines that you should consider following. That said it's good to have a specific example of how to run a script particular to your tasks. 

To this end I have done two things:

1. First I've copied your `src.py` script to this folder and edited it to be "damply-fied". Specifically it now saves the figs to the results folder. The change is on lines 86 and 87 of `produce_slepian_plots.py`. I also recommend you read through `example_script.py` to see how the `damply` library's `dirs` module gets used. 

2. Second, I've written a  little script that shows you how to use config files, command line arguments, and type hinting to write cleaner code. I am not sure if you've seen this before so sorry if you have. I tend to use these as standard practice. 

In order to run these scripts go to the main directory of this project and run the following commands: 

1. `pixi add python`. This will allow you run python3 in the local environment and also gives this pixi environemnt access to `pip` for package management. 
2. Run `pixi add networkx numpy scipy matplotlib --pypi`. This will add the packages you used in your script to the environment. The `--pypi` tag at the end tells pixi to look at `pip` instead of `conda-forge`. This is *optional* for the packages here. That is `pixi add networkx numpy scipy matplotlib pyyaml` would be fine. In cases where a package isn't on `conda-forge`, for example, then you need to tell pixi where to look. 

I've already done this steps so this should be done quickly. As you need additional libraries in the future this is how you will add them to the pixi environment. 


Once you've run the pixi commands,  navigate back to `workflow/scripts` and then run: 

`pixi run "python3 produce_slepian_plots.py"`

This is the general format for pixi calls:  `pixi run "<some_stuff>"`. `pixi run` tells the machine to run the code in the environment specified in the `pixi.toml` file in the main project directory. `"<some_stuff>"` needs to be in quotes so that pixi knows exactly what to run in the environment. If you forget the quotes then pixi will interpret `<some_stuff>` as pixi options, not code to run. 

This will generate the plots you have made of the Slepians of the barbell graph and put them in the results folder. 

The other script to read over is `generate_random_graph.py`. I've provided two config files that show you how these things work. 

You should read through the `generate_random_graph.py` script and the different config files and then run 

`pixi run "python3 generate_random_graph.py - config config1.yaml"`

and 
`pixi run "python3 generate_random_graph.py - config config2.yaml"`

Look at the different plots and understand how the different config files work through your project.  Your experiments should be driven by config files as much as possible. 

Evenutally your work should be a [*pixi task*](https://pixi.prefix.dev/latest/workspace/advanced_tasks/). For reproducibility someone should only have to:

1. Install pixi on their machine. 
2. Clone your repo from github
3. Run a relatively small number of pixi tasks. 



# GENERIC INSTRUCTIONS BELOW

## Purpose

This directory contains **reusable code scripts** for:

- Data processing pipelines
- Analysis workflows
- Utility functions
- Automation tasks

## Best Practices for Scripts

For maximum usability, scripts should:

- Include a detailed docstring/header explaining purpose, inputs, outputs
- Contain inline comments for complex logic
- Be modular and follow the single responsibility principle
- Include proper error handling and logging
- Have command-line interfaces when appropriate

## Git Synchronization

Scripts **ARE tracked in Git** and represent the core reproducible components of your analysis. Ensure scripts:

- Are well-tested before committing
- Have clear versioning (consider semantic versioning)
- Include usage examples in comments or separate documentation

## Organization Recommendations

Consider organizing scripts by their function:

```console
/scripts/preprocessing/
/scripts/analysis/
/scripts/visualization/
/scripts/utilities/
```

## Data References

When scripts access data:

- Use command-line arguments or configuration files for file paths
- Document in `docs/data_sources.md` which scripts use which data sources
- Consider using symbolic links for consistent references across environments

## Documentation Requirement

It is **highly recommended** to convert scripts to CLI tools using popular libraries
like `click` or `typer`, which can make them more user-friendly and easier to document.

```console
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
script_name.py
Usage: script_name.py [options] <input> <output>

Arguments:
    input     Description of input
    output    Description of output




Options:
    -h --help     Show this help
    -v --verbose  Verbose output
"""
```

Remember that well-documented scripts are essential for reproducible research and enable others to understand and build upon your work!
