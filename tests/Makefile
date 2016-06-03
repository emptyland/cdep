
TESTS=gtest_sanity_test glog_sanity_test
INCLUDE_DIR=../third-party/include
LIB_DIR=../third-party/libs
CXXFLAGS=-std=c++11 -I$(INCLUDE_DIR) -L$(LIB_DIR)

all: $(TESTS)

gtest_sanity_test: gtest_sanity_test.cc
	$(CXX) $(CXXFLAGS) -lgtest -lgtest_main -lglog gtest_sanity_test.cc -o gtest_sanity_test

glog_sanity_test: glog_sanity_test.cc
	$(CXX) $(CXXFLAGS) -lglog glog_sanity_test.cc -o glog_sanity_test

clean:
	rm -rf $(TESTS) logs
