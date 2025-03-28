# Tools we will use

### Table of contents

- [Why so many tools?](#why-so-many-tools)
- [Installation option 1](#installation-option-1)
- [Installation option 2](#installation-option-2)


## Why so many tools?
We want to build production ready ML software from day 1.

And for that, we need to use the right tools.

You have 2 options. You either

1. Install all the tools I will list below in your local machine.

or

2. Use the devcontainer that Marius Rugan prepared with all the tools already installed.

In either case, you will need to have

- The Docker engine installed on your machine.
    - [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
    - [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
    - [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/)

- A code editor. I use Cursor, which is a fork of VS Code, but feel free to use any other code editor you like.
    - [Cursor](https://www.cursor.com/)
    - [VS Code](https://code.visualstudio.com/)
    - [PyCharm](https://www.jetbrains.com/pycharm/)
    - ... any other code editor you like

- Git installed on your machine and an account on GitHub.


## Installation option 1 - Install all the tools in your local machine

These are the tools you will need to install. Click on each of them to see the installation instructions.

> Tip for Windows users
> 
> If you are on Windows, I recommend you first [install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) (Windows Subsystem for Linux) and then install the tools in the WSL terminal.
> With WSL you can run Linux commands from the Windows command line, so your chances of running into issues will be reduced.

Tools for development:

- [Docker](https://docs.docker.com/desktop/) to containerize each of the services of our system.

- [uv](https://docs.astral.sh/uv/) as the Python package and project manager. It's quickly becoming the de facto standard for Python, so you better get used to it. Using `uv` workspaces we build a monorepo, with all our services, and also shared libraries with code that can be reused across services.

  With `uv` we can also
    - install the exact version of the Python interpreter we want to use. In this course we will be using Python 3.12, because it is neither too old (so we can use the latest features of the language) nor too new (so we don't have to face incompatibilities with the libraries we will use).
    - tools for linting and formatting, like `ruff` or `pre-commit`.

- [make](https://www.gnu.org/software/make/) a build automation tool. In the course we will use
it as an alias for common commands, so we don't have to type/remember them all the time.

- [psql](https://www.postgresql.org/docs/current/app-psql.html) the command line interface for PostgreSQL. We will use it to interact with our Feature Store (RisingWave, which is based on PostgreSQL) from the terminal.

Tools for working with Kubernetes:

- [kind](https://kind.sigs.k8s.io/) a tool to run local Kubernetes clusters. We will use
kind to spin up a local Kubernetes cluster for development purposes.

- [kubectl](https://kubernetes.io/docs/reference/kubectl/) to interact with the Kubernetes cluster. This is the main CLI for Kubernetes, that we will use both with our local cluster and the one we will use in the cloud.

- [k9s](https://k9scli.io/) is a Terminal UI for managing your Kubernetes clusters. You will love it.

- [helm](https://helm.sh/) a package manager for Kubernetes. It will help us deploy the infrastructure services to Kubernetes, for example RisingWave, Kafka, Mlflow, etc.

- [direnv](https://direnv.net/) a tool to manage your environment variables. We will mostly use it
to load the right KUBECONFIG environment variable, so we can seamlessly switch between our local
cluster and the production environment that Marius Rugan has prepared.


## Installation option 2 - with devcontainer (recommended for Windows users)

Many of you, especially Windows users, had problems installing the tools on your system.

This is why Marius prepared a devcontainer for you, that comes with all the tools already installed.

To use this devcontainer, you will need (as I already said in the previous section):

- The Docker engine installed on your machine.
- A code editor. I use Cursor, which is a fork of VS Code, but feel free to use any other code editor you like.

Moreover, you need to install the Dev Container extension.

If you use VS Code, you can install it from the Extensions Marketplace.
Steps:
- Open the Extensions view by clicking on the Extensions icon in the Activity Bar on the left.
- Search for "Dev Containers"
- Click on the "Install" button

Once installed, you can open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P on Mac) and search for "Dev Containers: Reopen in Container".

And voila, you will have a development environment ready to go.