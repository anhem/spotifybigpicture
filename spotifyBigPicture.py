import sys
import shutil
import tempfile
import zipfile
import re
import os
import argparse

FILEPATH_OSX = '/Applications/Spotify.app/Contents/Resources/skin.xml'
FILEPATH_LINUX = '/opt/spotify/spotify-client/Data/resources.zip'
DEFAULT_FONT_SIZE = 8
PATTERN = 'size="([^"]*)"'

print '---[Spotify Big Picture]---'
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--restore', help='Restore Spotify to default font size', action='store_true')
parser.add_argument('-s', '--size', type=int, help='The size fonts should be changed with (positive=up, negative=down)')
parser.add_argument('-p', '--path', help='Specify path to Spotify resources.zip/skin.xml if not detected automatically')
args = parser.parse_args()

def backupFile(filePath):
    backupPath = filePath + '.bak'
    print 'Creating backup of %s to %s' % (filePath, backupPath)
    if os.path.exists(backupPath):
        print 'backup already exists'
    else:
        shutil.copy2(filePath, backupPath)

def restoreBackup(filePath):
    backupPath = filePath + '.bak'
    print 'restoring default font size from backup %s' % backupPath
    if os.path.exists(backupPath):
        os.remove(filePath)
        os.rename(backupPath, filePath)
    else:
        print 'No backup file found, restore not possible'

def extractArchive(filePath):
    extractDir = tempfile.mkdtemp()
    print 'extracting %s to %s' % (filePath, extractDir)
    zf = zipfile.ZipFile(filePath, 'r')
    try:
        for name in zf.namelist():
            zf.extract(name, extractDir)
    finally:
        zf.close()
    return extractDir

def compressArchive(srcDir, destFile):
    print 'compressing files from %s to %s' % (srcDir, destFile)
    zf = zipfile.ZipFile(destFile, mode='w')
    try:
        for root, dirs, files in os.walk(srcDir):
            for filename in files:
                absName = os.path.join(root, filename)
                arcName = absName[len(srcDir) + 1:]
                zf.write(absName, arcname=arcName)
    finally:
        zf.close()

def modifySkin(skinFile, fontSize):
    print 'updating %s with font size %s' % (skinFile, fontSize)
    newSkinFile = skinFile + '.new'
    reg = re.compile(PATTERN)
    with open(skinFile, 'r') as infile:
        with open(newSkinFile, 'w') as outfile:
            for line in infile:
                value = reg.search(line)
                if value is not None:
                    oldSize = value.group(1)
                    newSize = int(oldSize) + fontSize
                    line = re.sub(reg, 'size="' + str(newSize) + '"', line)
                outfile.write(line)
    os.remove(skinFile)
    os.rename(newSkinFile, skinFile)

def getResourcePathForWindows():
    import _winreg
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\\Spotify")
    value = _winreg.QueryValueEx(key, "")[0]
    return value + '\\Data\\resources.zip'

if args.restore:
    if args.path:
        if args.path.endswith('resources.zip') or args.path.endswith('skin.xml'):
            restoreBackup(args.path)
        else:
            print 'File not recognized, must be either resources.zip or skin.xml'
            exit(0)
    elif sys.platform.startswith('linux'):
        restoreBackup(FILEPATH_LINUX)
    elif sys.platform == 'darwin':
        restoreBackup(FILEPATH_OSX)
    elif sys.platform.startswith('win'):
        restoreBackup(getResourcePathForWindows())
    else:
        print 'OS not recognized, use --path <file path> to manually specify the resources.zip or skin.xml'
        exit(0)
else:
    fontSize = DEFAULT_FONT_SIZE
    if args.size:
        fontSize = args.size

    if args.path:
        if args.path.endswith('resources.zip'):
            backupFile(args.path)
            extractedDir = extractArchive(args.path)
            modifySkin(extractedDir + '/' + 'skin.xml', fontSize)
            compressArchive(extractedDir, args.path)
        elif args.path.endswith('skin.xml'):
            backupFile(args.path)
            modifySkin(args.path, fontSize)
        else:
            print 'File not recognized, must be either resources.zip or skin.xml'
            exit(0)
    else:
        if sys.platform.startswith('linux'):
            backupFile(FILEPATH_LINUX)
            extractedDir = extractArchive(FILEPATH_LINUX)
            modifySkin(extractedDir + '/' + 'skin.xml', fontSize)
            compressArchive(extractedDir, FILEPATH_LINUX)
        elif sys.platform == 'darwin':
            backupFile(FILEPATH_OSX)
            modifySkin(FILEPATH_OSX, fontSize)
        elif sys.platform.startswith('win'):
            filePath_windows = getResourcePathForWindows()
            backupFile(filePath_windows)
            extractedDir = extractArchive(filePath_windows)
            modifySkin(extractedDir + '\\' + 'skin.xml', fontSize)
            compressArchive(extractedDir, filePath_windows)
        else:
            print 'OS not recognized, use --path <file path> to manually specify the resources.zip or skin.xml'
            exit(0)
print 'Done'
