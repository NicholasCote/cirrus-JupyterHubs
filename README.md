# cirrus-JupyterHubs
Deploy a JupyterHub to NSF NCAR cirrus on-prem infrastructure

## Argo CD Application Generator for JupyterHub Instances

This Python script generates an Argo CD Application manifest and a values file for a new JupyterHub instance. It's designed to work within an existing app of apps pattern in Argo CD.

### Prerequisites

- Python 3.6+
- PyYAML library (`pip install pyyaml`)

### Usage

Run the script with the following command:

```
python daskhub/add_jhub.py <name> <image> <tag>
```

Arguments:
- `name`: Name of the application. This will be used in the application name and ingress host (e.g., `<name>-jhub.gingmachine`).
- `image`: Full path to the Jupyter container image to run.
- `tag`: Jupyter container image tag to use.

For example:
```
python daskhub/add_jhub.py my-hub docker.io/myorg/jupyter-image v1.2.3
```

### File Changes

The script will generate the following files:

1. `daskhub/templates/<name>-jhub-app.yaml`: Application manifest for the new JupyterHub instance.
2. `daskhub/<name>-jhub-values.yaml`: Values file for the new JupyterHub instance.

The script will append to the following file:

1. `daskhub/values.yaml`: Values file for all the deployed JupyterHubs

### File Structure

The changed files will be placed in the following structure:

```
daskhub/
├── templates/
│   └── <name>-jhub-app.yaml
└── <name>-jhub-values.yaml
└── values.yaml
```

### Application Manifest

The generated Application manifest includes:
- Application name based on the provided name
- Source repositories for the Helm chart and values
- Destination namespace
- Sync policy for automated management

## Values File

The generated values file includes:
- Jupyter single-user image configuration
- Ingress host configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Notes

- The script assumes a specific repository structure and naming convention. Make sure your Argo CD setup matches these assumptions.
- The ingress host is set to `<name>-jhub.gingmachine`. Adjust this in the script if you need a different domain.

Remember to commit the generated files to your repository after running the script.