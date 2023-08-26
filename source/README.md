# Application Overview
This is a lightweight, local version control system designed for small-scale use cases.
Instead of tracking changes in file states like traditional VCSs (e.g., Git), our application stores
actual copies of each file iteration, providing a more straightforward backup mechanism for users.

However, it should be acknowledged that this approach does come at a cost.
- Uses exponentially more storage space than traditional git systems 
  - Future consideration: Mitigate by compressing backup files.
- No file difference comparisons 
  - Future consideration: Refactor to include this potentially.

# File Structure
The application creates copies of files following the same directory structure within a .backup folder.
Each copy is timestamped and appended to the end of the original filename in the format %Y-%m-%d_%H-%M-%S.

# File Update Mechanism
The application checks if any file's last edit date is older than the current file's true date.
This is done by comparing the file's last edit date with the operating systems timestamp.
If the file has been modified, a new copy is created in the .backup folder.
```# Python
# Check if file has been updated
if self.file_path.stat().st_mtime > last_edit_date:
    # Create a backup copy
    create_backup(self.file_path)
```
# Example Directory
To get a quick overview of how the system operates look at the `ExampleVcsDirectory` to see where sample files
and their corresponding backup versions are stored.

# Dependencies
The application does not have any external dependencies.
However, it does heavily rely upon Python's built-in `pathlib` module.

# Application Path (app_path)
The `app_path` is the directory that the application will monitor for file changes.
Default value `DEFAULT_VCS_DIR_PATH = ../VcsDirectory` (`Path(__file__).parent.parent / DEFAULT_VCS_FOLDER_NAME`)
This can be overriden by providing a `Path` or `str` argument to the main function or via CLI `--path` (See more below). 
The application traverses the `app_path`, creating backups of any files that have been modified since the last run.

# Command Line Arguments
The application supports execution via command line arguments, giving users a more flexible way to interact with the
code without having to manually modify the source code. To run the application via CLI use the following format:
```
python main.py [--path PATH_TO_DIRECTORY] [--log LOG_LEVEL]
```
## Supported Arguments:
1. `--path`:
    - **Description**: This argument specifies the path of the working directory that you want the application to monitor for file changes.
    - **Default Value**: `DEFAULT_VCS_DIR_PATH = ../VcsDirectory` (`Path(__file__).parent.parent / DEFAULT_VCS_FOLDER_NAME`)
    - **Usage Example**: If you want to set the working directory to a folder named "my_project", you'd use: `--path /path/to/my_project`.
2. `--log`:
    - **Description**: This argument allows you to set the logging level for the application. By setting the appropriate logging level, you can control the verbosity of the application's output.
    - **Default Value**: If this argument is not provided, the application uses the logging level defined in `DEFAULT_LOG_LEVEL`: `INFO`.
    - **Accepted Values**: 'DEBUG', 'INFO', 'WARNING', 'ERROR', and 'CRITICAL'.
    - **Usage Example**: If you only want to see error messages and nothing else, you'd use: `--log ERROR`.

## CLI Examples:
1. To run the application with the default settings:

    ```
    python name_of_script.py
    ```

2. To run the application on a directory named "my_project" and set the log level to "DEBUG":

    ```
    python name_of_script.py --path /path/to/my_project --log DEBUG
    ```

3. To run the application on the directory the script resides in and see only warnings and errors:

    ```
    python name_of_script.py --path . --log WARNING
    ```