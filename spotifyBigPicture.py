import sys
import shutil
import tempfile
import zipfile
import re
import os
import _winreg

FILE_NAME = 'skin.xml'
PROPORTION = 8
PATTERN = 'size="([^"]*)"'

print '---[Spotify Big Picture]---'

def backupFile(filePath):
    backupPath = filePath + '.bak'
    print 'Creating backup of %s to %s' % (filePath, backupPath)
    try:
        with open(backupPath):
            print 'backup already exists'
    except IOError:
            shutil.copy2(filePath, backupPath)

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

def modifySkin(skinFile):
    print 'updating %s with sizes of +%s' % (skinFile, PROPORTION)
    newSkinFile = skinFile + '.new'
    reg = re.compile(PATTERN)
    with open(skinFile, 'r') as infile:
        with open(newSkinFile, 'w') as outfile:
            for line in infile:
                value = reg.search(line)
                if value is not None:
                    oldSize = value.group(1)
                    newSize = int(oldSize) + PROPORTION
                    line = re.sub(reg, 'size="' + str(newSize) + '"', line)
                outfile.write(line)
    os.remove(skinFile)
    os.rename(newSkinFile, skinFile)

if (sys.platform.startswith('linux')):
    resources = '/opt/spotify/spotify-client/Data/resources.zip'
    backupFile(resources)
    extractedDir = extractArchive(resources)
    modifySkin(extractedDir + '/' + FILE_NAME)
    compressArchive(extractedDir, resources)
elif (sys.platform == 'darwin'):
    skin = '/Applications/Spotify.app/Contents/Resources/skin.xml'
    backupFile(skin)
    modifySkin(skin)
elif (sys.platform.startswith('win')):
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Software\\Spotify")
    value = _winreg.QueryValueEx(key, "")[0]
    resources = value + '\\Data\\resources.zip'
    backupFile(resources)
    extractedDir = extractArchive(resources)
    modifySkin(extractedDir + '\\' + FILE_NAME)
    compressArchive(extractedDir, resources)
else:
    print 'OS not recognized!'
print 'Done'
