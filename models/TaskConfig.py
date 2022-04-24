import json


class TaskConfig():

    def __init__(self, compressed_package_path: str, flat_package_path: str, runtime: str, runtime_version: str) -> None:
        self.compressed_package_path = compressed_package_path
        self.flat_package_path = flat_package_path
        self.runtime = runtime
        self.runtime_version = runtime_version

    def __to_json__(self) -> json:
        return {
            "compressed_package_path": self.compressed_package_path,
            "flat_package_path": self.flat_package_path,
            "runtime": self.runtime,
            "runtime_version": self.runtime_version
        }

