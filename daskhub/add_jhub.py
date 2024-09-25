import yaml
import argparse

def generate_application(name):
    return {
        "apiVersion": "argoproj.io/v1alpha1",
        "kind": "Application",
        "metadata": {
            "name": f'{{{{ .Release.Name }}}}-{{{{ .Values.jhubs.{name}.name }}}}',
            "namespace": "argo"
        },
        "spec": {
            "project": "default",
            "sources": [
                {
                    "repoURL": "https://github.com/Gin-G/argo-k8s-stuff",
                    "path": "daskhub",
                    "targetRevision": "main",
                    "helm": {
                        "valueFiles": [
                            f"$values/daskhub/{name}-jhub-values.yaml"
                        ]
                    }
                },
                {
                    "repoURL": 'https://github.com/NicholasCote/cirrus-JupyterHubs',
                    "targetRevision": 'main',
                    "ref": "values"
                }
            ],
            "destination": {
                "server": "https://kubernetes.default.svc",
                "namespace": "gitops-jhubs"
            },
            "syncPolicy": {
                "automated": {
                    "prune": True,
                    "selfHeal": True
                },
                "syncOptions": [
                    "CreateNamespace=true"
                ]
            }
        }
    }

def generate_values(name, image, tag):
    return {
        "jupyterhub": {
          "singleuser": {
            "image": {
              "name": image,
              "tag": tag
              },
            "ingress": {
                "hosts": [
                    f"{name}-jhub.gingmachine"
                    ]
                }
            }
        }
    }

def update_values_yaml(name):
    with open('daskhub/values.yaml', 'r') as f:
        values = yaml.safe_load(f)

    values['jhubs'][name] = {"name": f"{name}-jhub"}

    with open('daskhub/values.yaml', 'w') as f:
        yaml.dump(values, f, default_flow_style=False)

def main(name, image, tag):
    app = generate_application(name)
    
    output_file = 'daskhub/templates/' f"{name}-jhub-app.yaml"
    with open(output_file, 'w') as f:
        yaml.dump(app, f, default_flow_style=False)

    # Generate values.yaml
    values = generate_values(name, image, tag)

    with open('daskhub/' + name + '-jhub-values.yaml', 'w') as f:
        yaml.dump(values, f, default_flow_style=False)
    
    update_values_yaml(name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Argo CD Application manifests")
    parser.add_argument("name", help="Name of the application, will become name-jhub.k8s.ucar.edu")
    parser.add_argument("image", help="Full path to the Jupyter container image to run")
    parser.add_argument("tag", help="Jupyter container image tag to use")
    args = parser.parse_args()
    
    main(args.name, args.image, args.tag)