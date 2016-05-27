#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys
import yaml
import os
import subprocess
import shutil

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

def updateDependency(repertoriesPath, name, version):
    versionObj = findVersionObj(repertoriesPath, name, version)
    if versionObj == None:
        raise Exception('version %s not found' % (version))

    fetchPkgScript = 'libs/fetch_package.sh'
    subprocess.check_call('bash %s %s %s %s' % (fetchPkgScript, name, \
        versionObj['packageUrl'], versionObj['workDir']), shell=True)

    os.putenv('CDEP_PKG_DIR', repertoriesPath + '/' + name)

    updatePackage(repertoriesPath, name, versionObj)

# print depObj['deps']

REPOSITORY_PATH = './repository'

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


