# - Verify Istio app
#   - deploy 2 simple app without sidecar
#   - deploy 2 simple app with sidecar
#   - test endpoints work with TLS
#   - test services level communication works
#     - with sidecar could talk to with sidecar
#     - with sidecar could talk to without sidecar
#     - without sidecar could talk to with sidecar
#     - without sidecar could talk to without sidecar
#   - Then
#       - teardown apps
