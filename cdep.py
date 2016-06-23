#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import yaml
import os
import subprocess
import shutil

CDEP_PATH = os.getenv('CDEP_PATH', default='.')

def loadYamlToObj(yamlFileName):
    f = open(yamlFileName, 'r')
    obj = yaml.load(f)
    f.close()
    return obj

def writeAll(fileName, content):
    f = open(fileName, 'w')
    f.write(content)
    f.close()

def readAll(fileName):
    f = open(fileName, 'r')
    content = f.read()
    f.close()
    return content

def readAllIfExist(fileName):
    if os.path.exists(fileName):
        return readAll(fileName)
    else:
        return None

def removeIfExist(filePath):
    if os.path.exists(filePath):
        if os.path.isdir(filePath):
            shutil.rmtree(filePath)
        else:
            os.unlink(filePath)

def checkVersion(repertoriesPath, name, version):
    path = repertoriesPath + '/' + name
    if not os.path.exists(path):
        return 'package: %s not found.' % (name)

    path = path + '/specs.yml'
    if not os.path.exists(path):
        return 'package: %s spces.yml file not found.' % (name)

    specObj = loadYamlToObj(path)
    versionObjs = specObj['versions']
    for versionObj in versionObjs:
        if version in versionObj:
            return None;
    return 'package: %s version: %s not found.' % (name, version)

def findVersionObj(repertoriesPath, name, version):
    specsFilePath = repertoriesPath + '/' + name + '/specs.yml'
    specObj = loadYamlToObj(specsFilePath)
    versionObjs = specObj['versions']
    for versionObj in versionObjs:
        if version in versionObj:
            return versionObj.items()[0][1]
    return None

def installFiles(dstPath, srcPath, files):
    for name in files:
        newPath = dstPath + '/' + os.path.basename(name)
        oldPath = srcPath + '/' + name
        print 'install %s -> %s' % (oldPath, newPath)
        if os.path.isdir(oldPath):
            shutil.copytree(oldPath, newPath)
        else:
            shutil.copy2(oldPath, newPath)

def updatePackage(repertoriesPath, name, versionObj):
    pkgSnapshotPath = './third-party/' + name + '/.package.snapshot'
    if readAllIfExist(pkgSnapshotPath) == name:
        return None

# pakcage lib
    cwd = os.getcwd()
    workDir = './third-party/%s/%s' % (name, versionObj['workDir'])
    os.chdir(workDir)

    print 'now packing...'
    for cmd in versionObj['pack']:
        subprocess.check_call(cmd, shell=True)
    os.chdir(cwd)

# install lib files
    installFiles('./third-party/libs', workDir, versionObj['staticLibFiles'])

# install header files
    installFiles('./third-party/include', workDir, versionObj['headerFiles'])

    writeAll(pkgSnapshotPath, name)

def cleanupIfNeed(repertoriesPath, name, version, versionObj):
    downSnapshotPath = './third-party/' + name + '/.download.snapshot'
    if not os.path.exists(downSnapshotPath):
        return True

    packedVersion = readAll(downSnapshotPath)
    if packedVersion == version:
        return False

    # cleanup all files
    shutil.rmtree('./third-party/' + name)

    packedVersionObj = findVersionObj(repertoriesPath, name, packedVersion)
    for libName in packedVersionObj['staticLibFiles']:
        removeIfExist('./third-party/libs/' + os.path.basename(libName))
    for headerName in packedVersionObj['headerFiles']:
        removeIfExist('./third-party/include/' + os.path.basename(headerName))
    return True


def updateDependency(repertoriesPath, name, version):
    global CDEP_PATH
    versionObj = findVersionObj(repertoriesPath, name, version)
    if versionObj == None:
        raise Exception('version %s not found' % (version))

    if cleanupIfNeed(repertoriesPath, name, version, versionObj):
        lib = CDEP_PATH + '/libs/fetch_package.sh'
        subprocess.check_call('bash %s %s %s %s' % (lib, name, \
            versionObj['packageUrl'], versionObj['sha256Digest']), shell=True)
        writeAll('./third-party/' + name + '/.download.snapshot', version)

        maySubDep = './third-party/' + name + '/' + versionObj['workDir'] + '/deps.yml'
        if os.path.exists(maySubDep):
            depObj = loadYamlToObj(maySubDep);
            print 'sub dep: %s' % (depObj['name'])
            lib = CDEP_PATH + '/libs/link_sub_dep.sh'
            cmd = 'bash %s %s %s' % (lib, name, versionObj['workDir'])
            print cmd
            subprocess.check_call(cmd, shell=True)

    os.putenv('CDEP_PKG_DIR', repertoriesPath + '/' + name)

    updatePackage(repertoriesPath, name, versionObj)

# print depObj['deps']

REPOSITORY_PATH = CDEP_PATH + '/repository'

depObj = loadYamlToObj('deps.yml')
if not 'deps' in depObj:
    print 'has no dependencies.'
    exit(1)

for dep in depObj['deps']:
    result = checkVersion(REPOSITORY_PATH, dep.items()[0][0], dep.items()[0][1]['version'])
    if result != None:
        print result
        exit(1)
print 'all dependencies clear.'

for dep in depObj['deps']:
    updateDependency(REPOSITORY_PATH, dep.items()[0][0], dep.items()[0][1]['version'])


