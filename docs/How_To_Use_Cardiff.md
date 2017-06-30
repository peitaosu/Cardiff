How-To Use Cardiff
==================

Cardiff is a version control tool for binary format files. This tool can be used to diff difference between file versions, to check what have been modified, save versions and manage versions.

# Preparations

Cardiff is written in Python and request some python modules. All required modules were listed in ```./requirements.txt```.

Before to use it, please make sure it has been able to meet your needs:
1. Currently, Cardiff use git as the VCS. You can add other VCS (such as SVN, TFS) support by yourself. 
2. You can find all supported formats under ./format folder. You can add the format which you need but not supported yet.

Well, let me assume the supported VCS and formats have met your request.

# Configurations

You need to configure ```./settings.json``` when you use Cardiff first time:
1. ```user.name``` and ```user.email``` must be set and will be used in your commit logs.
2. ```temp``` is the relative path of temp folder which store temporary files.
3. ```repo``` is the relative path of repository folder, not necessary to be set manually because it will be set after you initial your repository.
4. ```vcs``` is current VCS. If you want to switch to your VCS please change this setting.

OK. Now you finished all preparations and configurations.

# Your Workflow with Cardiff

Initial your repository. This repository will store all your versioned files, committed versions, logs, branches and other information:
```
python Cardiff.py init <repo_path>

# for example
python Cardiff.py init ./work
```

Create your file in repository folder or copy files from other locations directly. Only files which in this folder can be versioned.

Commit your file to VCS:
```
python Cardiff.py commit <file> <message>

# for example
python Cardiff.py commit my_work.psd "commit first psd file"
```

Check commits and logs:
```
python Cardiff.py log
```

Diff between commits, please make sure these 2 commits have same file.
```
python Cardiff.py diff <file> <version_1> [<version_2>]

# for example
python Cardiff.py diff my_work.psd 1 2
```

Merge between commits, please make sure these 2 commits have same file.
```
python Cardiff.py merge <file> <version_1> [<version_2>]

# for example
python Cardiff.py merge my_work.psd 1 2
```

# Robustness of Code
After you made some changes for Cardiff, we suggest you to add some check points into ```test.py``` and run it to avoid some issues and make Cardiff more robust.

Actually, we also enabled Travis CI (linux, py27) for this project. Travis CI build will be triggered while have new commits/pull requests, and ```test.py``` will be run.

We encourage everyone to contribute code, and there are measures to ensure the robustness of the code.