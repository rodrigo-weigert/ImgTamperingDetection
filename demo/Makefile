FLAGS=-Wall -O2

.PHONY: clear all

all: test run runall

test: perceptron.cpp perceptron.h test.cpp
	g++ perceptron.cpp test.cpp $(FLAGS) -o test

run:
	@echo "#!/bin/bash\n\
data=\`./image.py \$$1\`\n\
status=\$$?\n\
if [ \$$status -eq 1 ]\n\
then\n\
\techo \"Error: missing argument (image file).\"\n\
elif [ \$$status -eq 2 ]\n\
then\n\
\techo \"Error: image file not found or couldn't be read.\"\n\
else\n\
\techo \$$data | ./test\n\
fi" > run
	chmod +x run

runall:
	@echo "#!/bin/bash\n\
yes=0\n\
no=0\n\
for i in \`ls \$$1\`\n\
do\n\
\tresult=\`./run \$$1/\$$i\`\n\
\techo \"\$$i --> \$$result\"\n\
\tif [ \$${result:0:1} = \"N\" ]\n\
\tthen\n\
\t\tno=\$$((no + 1))\n\
\telse\n\
\t\tyes=\$$((yes + 1))\n\
\tfi\n\
\techo YES: \$$yes, NO: \$$no\n\
done" > runall
	chmod +x runall

clear:
	rm -rf test run runall
