6d44220 (HEAD, origin/master, origin/HEAD, master) Update README.md
4def97e Update README.md
5244952 Update README.md
7ac8d1c Update README.md
6b3a2f0 Update README.md
e215d98 Update README.md
eac7bcf Update README.md
a938f1e Update README.md
04bc4c7 Update README.md
5ddbaf7 Update README.md
4970ccb Update README.md
5f0018e Update README.md
81f7c2c Add files via upload
eb2733b Create conio.png
396d168 Update README.md
14a5c02 Update README.md
cbe9e5f utf8 added
49e2325 pep 287 and pep8 compliance
d574200 container.py to pep8 compliant
32ee310 modified to pep8
f739f40 pylint reorg
89eefbf Pylint type fix
2c4d024 observe pylint
deb0d73 observe pylint
d43a953 observe pylint
ae773a5 passing build
b2a8792 resolving build error
8c09f8c resolving build error
e758af1 trying to resolve import errors
0615b4b trying to resolve import errors
f037de3 trying to resolve import errors
d8326f8 trying to resolve import errors
20234f1 trying to resolve import errors
f832705 trying to resolve import errors
5e611b3 trying to resolve import errors
778cb30 trying to resolve import errors
ebf2b86 trying to resolve import errors
b08b7b2 trying to resolve import errors
2d1dc40 trying to resolve import errors
984142f trying to fix import error
aa5e4f0 trying to fix import error
b9cb6b5 trying to fix import error
a80bbd9 trying to fix import error
321429a trying to fix import error
219473d trying to fix import error
737147b changed path to console script
845cb0a trying to fix module import issue
a066f5c trying to fix module import issue
0af6f78 trying to fix module import issue
bc7d095 trying to fix module import issue
0b945a6 changed path to console script
d47138d reorg conio -> src, tests
6e9866b trying to fix attempted relative import error
1a6b2ed trying to fix attempted relative import error
eccbc90 test build
4b451dd removed -m from travis script
4aee864 removed __name__
88f15cb travis change
952305a changed test to include abs import
b915c2b changed test to include abs import
0aeddc9 added __init__ for test dir
071b0f9 added test
28bd5be move examples from tests
e1c8473 (tag: v1.0.5) clean print statements
a8a7a1c cleaner prints
8cca19b major bug fix for nvme-cli, offset and size param fixed
ba3ca07 cleaner graph prints
5d82ed2 added graphs for fio
e1be666 sceleton code for ascii graphs
2868fcf removed Conio-egg
1d81e30 Update README.md
f7c37ab (tag: v1.0.4) version update
15cb637 some checks to check if any container is running
3122b0e added grep exact- grep -x
4329ebb testing conio list --running
b8e7c03 provision of listing stopped containers
8e013dd added start and stop containers
5e565ff moved container specific stuff to container.py
aae0168 remove dist and build
931a15f binaries added
c24095e removed check for num == sections in jobfile mixed jobs
334fa0f Merge branch 'master' of https://github.com/saurabh-deochake/dockerbench
f4c17da better prompts
e23acfe Update README.md
0bd642e provision for offset and size, to allow containers not to write on each other
ba0bcbd Update README.md
f530ba0 (tag: v1.0.3) Update README.md
eddd0be added note
2a374a3 added note
eead39e added functionality to change commands and image names
a268908 bug fixes for cleaning
2046bb0 no container found error
981e962 now list all eligible containers
d7927dc Added option to remove num or all containers
8754680 clean error messages
1cbfaa9 new changes
db3bb7c Update setup.py
740e9ab version updated
f2d3ea5 Merge branch 'master' of https://github.com/saurabh-deochake/dockerbench
46c2ec3 cannot run with non-root user added to all commands
b864720 Update README.md
63f1266 Merge branch 'master' of https://github.com/saurabh-deochake/dockerbench
dca0d34 tool info changed
5bb7f89 Update README.md
9c5fb4c Update README.md
065adae Update README.md
ead338b Merge branch 'master' of https://github.com/saurabh-deochake/dockerbench
687a268 change version
7b75f97 (tag: v1.0.2) Update README.md
b845f4c Update README.md
ce9d072 support for conio create subcommand
f253058 version info added
f83b412 Merge branch 'master' of https://github.com/saurabh-deochake/dockerbench
1d0e0bd check if entered disk is a block device
1adc577 Update README.md
cb98751 Update README.md
126045f (tag: v1.0.1) added run and clean commands
f48042b (tag: v1.0.0) Cannot run as non-root user
bc4369b added tests and fixed bugs
cf3ea4c Update README.md
07494b2 Update README.md
7ff3655 Update README.md
99667bc Update .travis.yml
a95682d Update .travis.yml
f612302 Update .travis.yml
bd6f6d4 Update .travis.yml
2db6810 Update .travis.yml
9d7ba95 Create requirements.txt
66331bb Update README.md
0433437 Merge branch 'master' of https://github.com/saurabh-deochake/dockerbench
e66684d testing travis
146c835 Create .travis.yml
b3de60b Merge branch 'master' of https://github.com/saurabh-deochake/dockerbench
77e8fc5 if hdd entered then run only fio
30f2430 Update HowTo.md
e352b8e Update HowTo.md
c85c363 Update HowTo.md
a1f492d Update HowTo.md
cd3569c Update HowTo.md
ee85afe Update HowTo.md
8363864 Update HowTo.md
e988b28 Update README.md
ef56112 Update and rename HowTo.txt to HowTo.md
ac32709 Update README.md
70ee9a0 Update README.md
1baa39c Update README.md
a826a72 Update README.md
c6e4152 Rename README to README.md
624a773 Update README
3ee981e better error messages
8aa98b4 added newline for first run docker pull
fd2b88c exit on exceptions
35c8426 docker not running exit
bd6a9b1 docker not running exit
4b83834 deleted egg
745e2fe exit if docker is not installed
7027017 fixed 99.99 latency print
6886665 fixed specific output printing
dd71571 mixed jobs support
5c69e3e based on tools run the job, not finished
b62dbec fixed --mixed_jobs flag error
2bbe154 Merge branch 'master' of https://github.com/saurabh-deochake/dockerbench
6bec797 added config file and code to handle it. dont run.
ede3a5f Update README
20621a8 Added option to present all drives available
8fc096e fixed after docker disaster
8e67398 Added Dockerfile
c982ee9 rolled back
ea2537e Cleaned up code
4f9bdb6 run parallel in n containers
af9e535 print the outout of files
31464ae save output in files
7884360 Update conio.py
861f054 Update conio.py
2bf148a Update __init__.py
f26d29a Delete README.md
7633997 Create README
965fb82 added documentation and README
32957e6 changed pymodule to conio in setup.py
dfa8dcd added jobfile support
a9472ff Prompt messages changes
7db3bfe added comments
4b7ed8a added consolidated output
c7db194 used nested dictionaries for storing the output
fecf45b fixed misplacing of output
b5802f5 print the summary of each container
a561528 run fio and nvme at once
00f972a added option-wise selection of tools
e9e5126 fixed to get mentioned number of container Ids
32f81f2 added runtime
39ccb5a changed mounted ssd location inside the containers
ed38bb8 basic docker exec added
3491d30 added get container ids if num is less than running containers
8c5f10e restructure and num of container built
60262e0 resolved bugs in setup
5923c6d renamed to conio -Container IO
b76b944 added dio file
54ed42c added setup and changed name to verify
85c5763 changed info for container creation
481e130 Modified error handling
844491a verify docker
07a826d Initial commit
