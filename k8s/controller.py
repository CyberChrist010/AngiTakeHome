from kubernetes import client, config, watch

config.load_kube_config() # Loads the kube config from the default location

class UriShortenerController:
    def __init__(self):
        self.api = client.CustomObjectsApi()

    def watch_uri_shorteners(self):
        resource_version = ''
        while True:
            stream = watch.Watch().stream(self.api.list_cluster_custom_object,
                                          group="mycompany.com",
                                          version="v1",
                                          plural="urishorteners",
                                          resource_version=resource_version)
            for event in stream:
                obj = event['object']
                operation = event['type']
                spec = obj['spec']
                # Process the custom resource based on the event type (ADDED, MODIFIED, DELETED)
                # and the spec (like replicaCount, resources, image, shortCodes)
                # Implement custom logic
                # For example, create/update/delete Deployments based on the CRD
                ...

controller = UriShortenerController()
controller.watch_uri_shorteners()

