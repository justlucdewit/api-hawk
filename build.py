from sys import argv

incMajor = False
incMinor = False
incPatch = False

if "--major" in argv:
    incMajor = True
    argv.remove("--major")
elif "--minor" in argv:
    incMinor = True
    argv.remove("--minor")
elif "--patch" in argv:
    incPatch = True
    argv.remove("--patch")

# Read .version file and extract major minor patch and build number
with open('.version') as version_file:
    version = version_file.read().split('.')
    major = version[0]
    minor = version[1]
    patch = version[2]
    build = version[3]

    build = int(build) + 1

    if incMajor:
        major = str(int(major) + 1)
        minor = '0'
        patch = '0'
        build = 0
    elif incMinor:
        minor = str(int(minor) + 1)
        patch = '0'
        build = 0
    elif incPatch:
        patch = str(int(patch) + 1)
        build = 0

    # write new version to .version file
    # build number must be formatted as 4 digits
    with open('.version', 'w') as version_file:
        version_file.write(f'{major}.{minor}.{patch}.{build:06d}')

# Run main .py file
import main