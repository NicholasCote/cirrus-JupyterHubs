import yaml
import argparse

def generate_jupyterhub_config(name, namespace, image_name, image_tag, fqdn):
    config = {
        'name': name,
        'namespace': namespace,
        'jupyterHubConfig': {
            'jupyterhub': {
                'singleuser': {
                    'image': {
                        'name': image_name,
                        'tag': image_tag,
                    },
                },
                'ingress': {
                    'enabled': True,
                    'annotations': {
                        'traefik.ingress.kubernetes.io/router.entrypoints': 'web'
                    },
                    'hosts': [fqdn]
                },
            },
            'proxy':{
                'service':{
                    'type': 'ClusterIP'
                },
            },
        },
    }
    return config

def main():
    parser = argparse.ArgumentParser(description="Generate custom JupyterHub yaml configuration")
    parser.add_argument('--name', required=True, help='Name of the JupyterHub instance')
    parser.add_argument('--namespace', required=True, help='Kubernetes namespace for the JupyterHub instance')
    parser.add_argument('--image_name', required=True, help='Docker image name for the JupyterHub instance')
    parser.add_argument('--image_tag', required=True, help='Docker image tag for the JupyterHub instance')
    parser.add_argument('--fqdn', required=True, help='Fully Qualified Domain name for the JupyterHub instance')

    args = parser.parse_args()

    config = generate_jupyterhub_config(
        args.name,
        args.namespace,
        args.image_name,
        args.image_tag,
        args.fqdn
    )

    print(yaml.dump([config], default_flow_style=False))

if __name__ == '__main__':
    main()