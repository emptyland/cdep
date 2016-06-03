#include "glog/logging.h"

int main(int argc, char *argv[]) {
    google::InitGoogleLogging(argv[0]);

    FLAGS_log_dir = "./logs";

    LOG(INFO) << "info ... ok";
    LOG(WARNING) << "warning ... ok";
    LOG(ERROR) << "error ... ok";

    return 0;
}
