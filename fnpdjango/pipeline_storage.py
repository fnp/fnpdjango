from pipeline.storage import GZIPMixin
from pipeline.storage import PipelineManifestStorage


class GzipPipelineManifestStorage(GZIPMixin, PipelineManifestStorage):
    pass

