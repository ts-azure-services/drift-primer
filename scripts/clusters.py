from authentication import ws
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException

def create_compute_cluster(workspace=None, compute_name=None):
    """Create AML compute cluster"""
    try:
        cpu_cluster = ComputeTarget(workspace=workspace, name=compute_name)
        print('Found existing cluster, use it.')
    except ComputeTargetException:
        # To use a different region for the compute, add a location='<region>' parameter
        compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_D2_V2',
                min_nodes=0,
                max_nodes=5)
        cpu_cluster = ComputeTarget.create(workspace, compute_name, compute_config)
        print(f'Triggered the creation of {compute_name} cluster')
        cpu_cluster.wait_for_completion(show_output=True)

def main():
    """Main operational flow"""
    cluster_name='cpu-cluster'
    create_compute_cluster(
            workspace=ws, 
            compute_name=cluster_name
            )

if __name__ == "__main__":
    main()
