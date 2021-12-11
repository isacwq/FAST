import os
import os.path, pathlib
import glob

def checkIfFilesHaveBeenModified(projectPath):

    testFilesPath = '/src/test/java'
    testFilesFullPath = projectPath + testFilesPath

    fastPrioritizedSuite = testFilesFullPath + '/fast/FASTPrioritizedSuite.java'

    if os.path.exists(fastPrioritizedSuite):
        lastModificationTime = os.path.getmtime(fastPrioritizedSuite)
    else:
        #first execution
        return True

    findModifiedFiles = False

    os.chdir(testFilesFullPath)

    #atualizar assinatura MD5
    for path in pathlib.Path(testFilesFullPath).glob("**/*"):  # Do a recursive search across all files
        if os.path.getmtime(path) > lastModificationTime and not os.path.isdir(path):
            return True

    return findModifiedFiles

def getTestFilesFromProject(projectPath):
    # https://junit.org/junit5/docs/current/user-guide/#running-tests-build-maven-filter-test-class-names
    arr = glob.glob(f'{projectPath}/**/Test*.java', recursive=True)
    arr.extend(glob.glob(f'{projectPath}/**/*Test.java', recursive=True))
    arr.extend(glob.glob(f'{projectPath}/**/*Tests.java', recursive=True))
    arr.extend(glob.glob(f'{projectPath}/**/*TestCase.java', recursive=True))
    arr.extend(glob.glob(f'{projectPath}/*Test.java', recursive=True))
    arr.extend(glob.glob(f'{projectPath}/*Tests.java', recursive=True))
    arr.extend(glob.glob(f'{projectPath}/*TestCase.java', recursive=True))
    return arr

def checkDeletedFile(projectPath):
    projectName = os.path.basename(os.path.normpath(projectPath))
    indexTestFilesPaths = "{}/.fast/input/{}-indexTestFilesPaths.txt".format(projectPath, projectName)

    if os.path.exists(indexTestFilesPaths):
        f2 = open(indexTestFilesPaths, "r")
        testFilesPaths = f2.readlines()
        f2.close()

        testFilesFromProject = getTestFilesFromProject(projectPath)

        testFileDeletedBeforeLastExecution = False

        for testFilePath in testFilesPaths:
            testFileFullPath = "{}/{}".format(projectPath, testFilePath.replace('\n',''))

            if not testFileFullPath in testFilesFromProject:
                testFileDeletedBeforeLastExecution = True
                break

        return testFileDeletedBeforeLastExecution
    else:
        return True
