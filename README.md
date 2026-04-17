# VS Code IntelliSense setup for ROS workspace

This workspace uses a merged `compile_commands.json` so Visual Studio Code IntelliSense can see all package compile flags and include paths.

## 1. Configure VS Code

Make sure the workspace file `.vscode/c_cpp_properties.json` contains:

```json
{
  "configurations": [
    {
      "name": "Linux",
      "includePath": [
        "${workspaceFolder}/**"
      ],
      "defines": [],
      "cStandard": "c17",
      "cppStandard": "gnu++17",
      "intelliSenseMode": "linux-gcc-x64",
      "compileCommands": "${workspaceFolder}/build/compile_commands.json"
    }
  ],
  "version": 4
}
```

This points IntelliSense at the workspace-level build database.

## 2. Generate package compile databases

Build the packages with CMake compile command export enabled.

From the workspace root:

```bash
cd ${workspaceFolder}
colcon build --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

If you only want to rebuild one package, use:

```bash
colcon build --packages-select test_robot_move --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

## 3. Merge compile command files
Place in the root of the project and add execution perms to the script file:
```bash
chmod +x merge.py
```

Run the script:
```bash
./merge.py
```

It collects `build/*/compile_commands.json` files and writes a merged database to:

- `build/compile_commands.json`

## 4. Reload VS Code

After creating the merged file:
1. Reload the VS Code window
2. Re-open your source file
3. Wait for the C/C++ extension to finish indexing

Or:
- Command palette
- Run
- `C/C++: Reset IntelliSense Database`

## 5. When to rerun

Re-run the merge script whenever:

- you rebuild a package
- new source files are added
- compiler flags or dependencies change

## 6. Notes

- The merge file must contain the translation unit you are editing.
- If you still see `#include` errors, confirm the package build produced a `compile_commands.json` and that the file is listed in `build/compile_commands.json`.
