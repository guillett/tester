#!/bin/bash

set -ev

NAME=$1
REPOSITORY_URL=$2
TEST_COMMAND=$3
NO_UV=$4
CORE_PATH=../next/core

if ! [ -d tmp ]
then
    mkdir tmp
fi
cd tmp

if ! [ -d $NAME ]
then
    mkdir $NAME
fi
cd $NAME

if ! [ -d repository ]
then
    git clone --depth 1 $REPOSITORY_URL repository
fi
cd repository

pwd
git fetch --depth 1

if [ $NO_UV ]
then
    uv pip install .
    uv pip install --editable $CORE_PATH
else
    uv sync --frozen
    uv add --editable $CORE_PATH --frozen
fi

uv pip list

echo $TEST_COMMAND
$TEST_COMMAND

