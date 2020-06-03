# Conda usage

## How To create a new environment

To create an environment named "myenv" with epics-base 7, run:

```bash
conda create -n myenv epics-base=7
```

## How to activate an environment

Use the `conda activate` command followed by the environment name:

```bash
conda activate myenv
```

## How to deactivate an environment

Use `conda deactivate`:

```bash
conda deactivate
```

## How to delete an environment

Use the `conda env remove` command:

```bash
conda env remove -n myenv
```

## How to export an environment

Use the `conda env export` command:

```bash
conda env export -n myenv > environment.yml
```

## How to create an environment based on an environment file

Use the `conda env create` command:

```bash
conda env create -n myenv -f environment.yml
```

If you omit the `-n` parameter, the environment name will be taken from the `environment.yml` file.
The command will fail if the environment already exists. You can to destroy it first by using `--force`.
