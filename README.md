# Repository template for application project

This is a template for an application repository. It is a simple hello-world nginx container with a complete CI/CD pipeline example. For more detailed documentation about the pipeline see [kustomize-cd](https://gitlab.met.no/k8s/tools/kustomize-cd).

#### Instructions

1. Fork this repository to desired namespace on gitlab
2. Set a new project name
    `settings > general`
3. Set project path to the same as the project name
    `settings > general > advanced > change path`
4. Enable CI/CD
    `settings > general > Visibility, project features, permissions`
    * Toggle on `Container Registry`
    * Toggle on `CI/CD`

Now you are ready to clone the new repository to your computer and start creating.

**Note**: The CI/CD pipeline is only run on commits that have a tag, the default rule follows the [Semantic Versioning 2](https://semver.org/) standard of `major, minor, patch`: `v0.0.1`

The Deploy step in the pipeline requires you to update `tjenester/PROJECTNAME` with the kubernetes projectname you want to deploy to. All active kubernetes projectnames are listed here https://gitlab.met.no/tjenester/.
> Please replace/update the contents of this README with documentation for your project when appropriate.
