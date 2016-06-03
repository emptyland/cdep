#!/bin/bash

for test in tests/*_test; do
    ${test}
done
