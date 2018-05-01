from server.resources.models.descriptor.boutiques import Boutiques
"""
SUPPORTED_DESCRIPTORS contains all decriptors that are supported by the platform.
Keys should not include characters that can cause problems for filenames and/or
paths. Stay away from '/', '\', '?', for example.
"""
SUPPORTED_DESCRIPTORS = {'boutiques': Boutiques}
