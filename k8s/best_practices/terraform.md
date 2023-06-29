terraform compare actual state and desired state to make changes in the infra. \
state file is a JSON file.

1. manipulate state only through TF commands
    * terraform apply
    * terraform state(for advanced state management)
2. always set up a shared remote storage for state files
terraform creates state file automatically on first "terraform apply" command,  by default, it is created locally. available remote storage are S3, Terraform Cloud, Azure Blob Storage, Google Cloud Storage etc.
3. use state locking
prevent concurrent runs to your state file, in practice you need configure in your storage backend.(Not all backends support locking. If supported, TF will lock your state for all operatings that could write state)
4. Back up your state files
in practice, enable versioning to allow state recovery
5. One state file per environment
6. Host TF files in its own git repository 
    * effective team collaboration
    * version control for your IaC code
7. Terraform code as Application Code
8. Apply infrastructure changes ONLY through CD pipeline