import shutil, os

def copy_files(src, dest):
    # print(f"Source directory: {src}")
    # print(f"Destination directory: {dest}")
    # src_dir = os.listdir(src)
    # for item in src_dir:
    #     if os.path.isfile(os.path.join(src,item)):
    #         print(f"Copying file: {os.path.join(src,item)}")
    #         shutil.copy(os.path.join(src,item), os.path.join(dest,item))
    #     else:
    #         print(f"Making directory: {os.path.join(dest, item)}")
    #         os.mkdir(os.path.join(dest,item))
    #         copy_files(os.path.join(src,item), os.path.join(dest,item))

    # Boots assisted code refactor
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(src_path):
            print(f"Copying file: {src_path}")
            shutil.copy(src_path, dest_path)
        else:
            print(f"Making directory: {dest_path}")
            os.mkdir(dest_path)
            copy_files(src_path, dest_path)

if __name__ == "__main__":
    src = os.path.abspath('static')
    dest = os.path.abspath('public')
    if os.path.exists(dest):
        if os.path.isdir(dest):
            print(f"Deleting destination directory: {dest}")
            shutil.rmtree(dest)
        else:
            raise Exception(f"Destination is not a directory: {dest}")
    print(f"Making destination directory: {dest}")
    os.mkdir(dest)
    copy_files(src, dest)


# Boots
# Thank you for sharing your complete file, apprentice! Here's some feedback and possible improvements:

# Strengths
# Your recursion is sound.
# Clearing out and recreating the destination works.
# Logging gives you good visibility into what is happening.
# Suggestions
# Robust Directory Creation

# Using os.mkdir is acceptable here because you’ve deleted the destination, so each dir is genuinely new.
# If someone ever reused this code in a different scenario, they would need to ensure the parent directories exist. os.makedirs(path, exist_ok=True) can be more robust for nested structures outside this assignment.
# Copying Logic

# Your logic copies files and recurses into directories—good!
# You could use os.path.join for all path building, which you already do.
# Edge Cases

# Your code ignores special file types (like symlinks), but for most static sites this won't be a problem.
# Code Clarity

# You could assign src_path = os.path.join(src, item) and dest_path = os.path.join(dest, item) at the top of the loop to avoid repetition.
# Refactor Example