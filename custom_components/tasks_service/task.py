import string


class Task:
    """Task class."""

    def __init__(self, id: int, name: string, type: string,
                 description: string, sourcePath: string, sourceType: string,
                 destinationPath: string, destinationType: string):
        """Initialize."""
        self.id = id
        self.name = name
        self.type = type
        self.description = description
        self.sourcePath = sourcePath
        self.sourceType = sourceType
        self.destinationPath = destinationPath
        self.destinationType = destinationType


