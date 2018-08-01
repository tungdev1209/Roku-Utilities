# Roku-Utilities

## Roku Clean script path
Clean up all script path in all xml file at project directory.   
In each xml file, this script auto fixing uri path for all <script> elements.

### Requirements
python 2.7+

### How to use
In terminal:

- Fix all xml files in project dir
```
python cleanScriptPath.py -p <path-to-roku-project>
```

*Ex:* python cleanScriptPath.py -p /Users/tungnguyen/Projects/Roku/MyFirstRokuProject

- Or just xml files in module dir
```
python cleanScriptPath.py -p <path-to-roku-project> -m <path-to-module>
```

- Or a certain xml file
```
python cleanScriptPath.py -p <path-to-roku-project> -f <path-to-xml-file>
```

- Or combine
```
python cleanScriptPath.py -p <path-to-roku-project> -m <path-to-module> -f <path-to-xml-file>
```

## Roku Install

### How to use
Open install.sh and set up configs

path="path/to/project/dir"   
rokuIP="192.168.x.x"   
rokuName="rokudev"   
rokuPass="xxxx"   

In terminal:
```
sh install.sh
```

Have fun!
