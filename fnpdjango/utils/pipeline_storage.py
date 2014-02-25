from pipeline.storage import GZIPMixin
from pipeline.storage import PipelineCachedStorage

class GzipPipelineCachedStorage(GZIPMixin, PipelineCachedStorage):
    pass

