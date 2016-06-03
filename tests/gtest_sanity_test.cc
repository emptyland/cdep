#include "gtest/gtest.h"
#include "glog/logging.h"

TEST(GTest, Santiy) {
    auto i = 1 + 1;
    ASSERT_EQ(2, i) << "Can not fail!";
}

TEST(GTest, Logging) {
    LOG(INFO) << "logging...";
}
