import fnmatch
import shutil
import subprocess
from pathlib import Path
from typing import Iterable

from setuptools import Command, setup
from setuptools.command.build import SubCommand, build


class build_npm(Command, SubCommand):
    """Builds npm projects for Sardine."""

    build_lib = "build/lib"

    yarn_projects: list[str]
    """A list of project paths to be built with `yarn build` and copied."""

    exclude_files: list[str] = [".svelte-kit", "node_modules"]
    """
    A list of glob patterns for excluding files or directories from each path
    in `yarn_projects` when creating the source distribution.
    """

    # SubCommand protocol

    def initialize_options(self) -> None:
        """
        Set or (reset) all options/attributes/caches used by the command
        to their default values. Note that these values may be overwritten during
        the build.
        """
        self.yarn_projects = []

    def finalize_options(self) -> None:
        """
        Set final values for all options/attributes used by the command.
        Most of the time, each option/attribute/cache should only be set if it does not
        have any value yet (e.g. ``if self.attr is None: self.attr = val``).
        """
        self.yarn_projects = ["fishery/client"]

    def run(self) -> None:
        """
        Execute the actions intended by the command.
        (Side effects **SHOULD** only take place when ``run`` is executed,
        for example, creating new files or writing to the terminal output).
        """
        if not self._has_projects():
            return

        self._validate_project_paths()

        npx = shutil.which("npx")
        if npx is None:
            raise RuntimeError(
                "Node.js must be installed in order to build this package; "
                "see installation instructions here: https://nodejs.org/en/download/"
            )

        for path in self.yarn_projects:
            kwargs = {"cwd": path, "shell": True}
            subprocess.check_call(f'"{npx}" yarn install', **kwargs)
            subprocess.check_call(f'"{npx}" yarn run build', **kwargs)

            build_path = Path(path) / "build"
            shutil.copytree(
                build_path,
                self.build_lib / build_path,
                dirs_exist_ok=True,
            )

    def get_source_files(self) -> list[str]:
        """
        Return a list of all files that are used by the command to create the expected
        outputs.
        For example, if your build command transpiles Java files into Python, you should
        list here all the Java files.
        The primary purpose of this function is to help populating the ``sdist``
        with all the files necessary to build the distribution.
        All files should be strings relative to the project root directory.
        """
        self._validate_project_paths()

        files = []
        for path_str in self.yarn_projects:
            files.extend(self._get_source_for(Path(path_str)))

        return files

    def get_outputs(self) -> list[str]:
        """
        Return a list of files intended for distribution as they would have been
        produced by the build.
        These files should be strings in the form of
        ``"{build_lib}/destination/file/path"``.

        .. note::
           The return value of ``get_output()`` should include all files used as keys
           in ``get_output_mapping()`` plus files that are generated during the build
           and don't correspond to any source file already present in the project.
        """
        build_lib = Path(self.build_lib)

        files = []
        for path_str in self.yarn_projects:
            build_path = build_lib / path_str / "build"
            assert build_path.is_dir(), f"failed to build {path_str}"

            for file in build_path.rglob("*"):
                files.append(str(file))

        return files

    def get_output_mapping(self) -> dict[str, str]:
        """
        Return a mapping between destination files as they would be produced by the
        build (dict keys) into the respective existing (source) files (dict values).
        Existing (source) files should be represented as strings relative to the project
        root directory.
        Destination files should be strings in the form of
        ``"{build_lib}/destination/file/path"``.
        """
        return {}

    # Utility methods

    def _get_source_for(self, path: Path) -> Iterable[str]:
        for file in path.iterdir():
            if any(fnmatch.fnmatch(file.name, pat) for pat in self.exclude_files):
                continue

            if file.is_dir():
                yield from self._get_source_for(file)
            else:
                yield str(file)

    def _has_projects(self) -> bool:
        if not self.yarn_projects:
            return False
        return True

    def _validate_project_paths(self) -> None:
        for path_str in self.yarn_projects:
            if not Path(path_str).is_dir():
                message = f"{path_str} must be a directory containing a yarn project"
                raise ValueError(message)

    # Subcommand registration

    build.sub_commands.append(("build_npm", None))


setup(cmdclass={"build_npm": build_npm})
